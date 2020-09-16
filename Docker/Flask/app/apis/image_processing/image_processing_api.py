# image_processing_api
# Description : API ของการประมวลผลรูปภาพ
# Author : Athiruj Poositaporn

from flask import Flask, request, jsonify ,Blueprint ,make_response
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,jwt_refresh_token_required,
    create_refresh_token
)
from pymongo import MongoClient
import logging.config
import numpy as np
from bson.json_util import dumps
import cv2
import base64
from . import image_measurement
from . import image
from .. import db_config
from .. import err_msg

image_processing_api = Blueprint('image_processing_api', __name__)

# นามสกุลไฟล์ที่ระบบรองระบ
extension = ["bmp","jpg","jpe","png"]

# กำหนดชื่อ logger
logger = logging.getLogger("image_processing_api")


logger.info("Connecting to database")
# เชื่อมต่อกับฐานข้อมูล
URI = "mongodb://"+db_config.item["db_username"]+":" + \
db_config.item["db_password"]+"@"+db_config.item["db_host"]
db_connect = MongoClient(URI)
logger.info("Connected to database")

# กำหนดชื่อของ DB 
DPML_db = db_connect[db_config.item["db_name"]]
# กำหนด collection ที่ใช้งาน 
unit_collection = db_config.item['db_col_unit']

# is_int
# Description : ตรวจสอบว่า number เป็น int ได้หรือไม่
# Author : Athiruj Poositaporn
def is_int(number):
        try:
            temp = int(number)
            if(temp <= 0):
                return False
            return True
        except:
            return False

# upload_image
# Description : Service ของการอัปโหลดรูปภาพและวัดขนาดของวัตถุ
# Author : Athiruj Poositaporn
@image_processing_api.route("/upload_image", methods=['put'])
@jwt_required
def upload_image():
    try:
        file = request.files.get('file',None)
        username = get_jwt_identity()

        query_unit = None
        logger.info("[{}] Prepair image data to be measure.".format(username))
        if(not file):
            logger.warning("[{}] File is empty.".format(username))
            raise TypeError(err_msg.msg['file_empty'])
        else:
            file_extension = (file.filename.split('.')[-1]).lower()

        if file_extension not in extension:
            logger.warning("[{}] Wrong file extension.".format(username))
            raise TypeError(err_msg.msg['file_extension'])

        logger.info("[{}] Processing image...".format(username))
        nparr = np.fromstring(request.files['file'].read(), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) 

        image_processor = image_measurement.ImageMeasurement()
        input_image = image.Image(image=img)
        
        logger.info("[{}] Got measurement result".format(username))
        result_img = image_processor.measure_obj_size(input_image)

        logger.info("[{}] Prepair image date to be response.".format(username))
        retval, buffer = cv2.imencode('.png', result_img['img'])
        data = base64.b64encode(buffer)
        data = data.decode('utf-8')

        if(result_img['status'] == "system_error"):
            return result_img , 400
        elif(result_img['status'] == "ml_not_found"):
            result = {'mes' : "Object not detected." ,'img' : data, 'status' : "ml_not_found"}
            return result , 400
        elif(result_img['status'] == "ref_not_found"):
            result = {'mes' : "Reference object not detected.",'img' : data, 'status' : "ref_not_found"}
            return result , 400
        response = {
            'img' : data,
            'img_data' : result_img['img_data'],
        }
        del image_processor
        logger.info("[{}] Responsed measurement result.".format(username))
        return response , 200
    except Exception  as identifier:
        try:
            # ใช้เพื่อค้นหาว่าค่า identifier มีใน err_msg.msg หรือไม่ ถ้าไม่มีการทำงานจะ error และเข้าสู่ except
            list(err_msg.msg.keys())[list(err_msg.msg.values()).index(identifier)]
            result = {'mes' : str(identifier), 'status' : "error"}
        except:
            logger.error("{}.".format(str(identifier)))
            result = {'mes' : str(identifier), 'status' : "system_error"}
            # result = {'mes' : err_msg.msg['other_err']}
        return result , 400
    finally:
        db_connect.close()

# get_all_unit
# Description : Service ของการเรียกข้อมูลหน่วยในการวัดขนาดทั้งหมด
# Author : Athiruj Poositaporn
@image_processing_api.route("/get_all_unit", methods=['get'])
@jwt_required
def get_all_unit():
    try:
        query_unit = DPML_db[unit_collection].find()
        arr = []
        for item in query_unit:
            item.pop('_id')
            arr.append(item)
        return jsonify(arr) , 200
    except Exception as identifier:
        result = {'mes' : str(identifier), 'status' : "system_error"}
        return result , 400
