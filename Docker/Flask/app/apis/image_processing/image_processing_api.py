from flask import Flask, request, jsonify ,Blueprint ,make_response
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
extension = ["bmp","pbm","pgm","ppm","sr","ras","jpeg","jpg","jpe","jp2","tiff","tif","png"]
logger = logging.getLogger("image_processing")

URI = "mongodb://"+db_config.item["db_username"]+":" + \
db_config.item["db_password"]+"@"+db_config.item["db_host"]
logger.info("Connecting to database")

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# ต้องแก้ไขให้ดึงข้อมูลจาก DB
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# db_connect = MongoClient(URI)
# logger.info("Connected to database")
# DPML_db = db_connect[db_config.item["db_name"]]
# unit_collection = db_config.item['db_col_unit']
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

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
def upload_image():
    try:
        file = request.files.get('file',None)
        un_id = request.form.get('unit',None)

        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # ต้องแก้ไขให้ดึงข้อมูลการส่งค่าชื่อผู้ใช้งาน
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        username = "Debug_user"
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

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
        elif(not is_int(un_id)):
            logger.warning("[{}] Wrong unit id. This ID dose not match any unit id on dpml_unit".format(username))
            raise TypeError(err_msg.msg['unit_id'])

        # @@@@@@@@@@@@@@@@@@@@@@
        # ต้องแก้ไขให้ดึงข้อมูลจาก DB
        # @@@@@@@@@@@@@@@@@@@@@@
        # un_id = int(un_id)
        # query_unit = DPML_db[unit_collection].find_one({
        #     db_config.item['fld_un_id']: un_id
        # })

        # if(not query_unit):
        #     logger.warning("[{}] Wrong unit id. This ID dose not match any unit id on dpml_unit".format(username))
        # raise TypeError(err_msg.msg['unit_id'])
        # @@@@@@@@@@@@@@@@@@@@@@


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

        if(result_img['status'] == "ml_not_found"):
            result = {'mes' : "Object not detected." ,'img' : data, 'status' : "ml_not_found"}
            return result , 400
        elif(result_img['status'] == "ref_not_found"):
            result = {'mes' : "Reference object not detected.",'img' : data, 'status' : "ref_not_found"}
            return result , 400

        response = {
            'img' : data,
            'img_data' : result_img['img_data'],
        }
        logger.info("[{}] Responsed measurement result.".format(username))
        return response , 200
    except Exception  as identifier:
        try:
            # ใช้เพื่อค้นหาว่าค่า identifier มีใน err_msg.msg หรือไม่ ถ้าไม่มีการทำงานจะ error และเข้าสู่ except
            list(err_msg.msg.keys())[list(err_msg.msg.values()).index(identifier)]
            result = {'mes' : str(identifier), 'status' : "error"}
        except:
            result = {'mes' : str(identifier), 'status' : "system_error"}
            # result = {'mes' : err_msg.msg['other_err']}
        return result , 400
    finally:
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # ต้องแก้ไขให้ดึงข้อมูลจาก DB
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        # db_connect.close()
        pass
        # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

