# model_management_api
# Description : ไฟล์สำหรับการพัฒนา API ของการจัดการเพิ่ม แก้ไข และลบ
# ข้อมูลต้นอบบของวัตถุ
# Author : Athiruj Poositaporn
from flask import Flask, request, Blueprint ,make_response,jsonify
import logging.config
from pymongo import MongoClient
from bson.json_util import dumps
from .. import db_config
# from .. import logging_config

from .model import Model
from .model_manager import MLManagement, RefManagement

model_management_api = Blueprint('model_management_api', __name__)
logger = logging.getLogger("model_management_api")
logger_user = logging.getLogger("user_management")
# logging.config.dictConfig(logging_config)

# add_ml_model
# Description : เพิ่มข้อมูลของชื่อและไฟล์ .weights ของข้อมูลต้นแบบของวัตถุ 
# Author : Athiruj Poositaporn
@model_management_api.route("/add_model", methods=['post'])
def add_model():
    try:
        model_type = request.form.get('type')
        username = request.form.get('username')
        # logger_user.info("[{}] This is user".format(username))
        if(model_type == "ml"):
            logger.info("[{}] Use add ML model API.".format(username))
            file = request.files['file']
            name = request.form.get('name')
            data = Model(name = name , file=file,username=username)
            ml_manager = MLManagement().create_manager()
            logger.info("[{}] Created MLManagement object.".format(username))
            logger.info("[{}] Call add_model function.".format(username))
            result = ml_manager.add_model(data=data)
            del ml_manager
            return result

        elif(model_type == "ref"):
            logger.info("[{}] Use add Ref model API.".format(username))
            file = request.files['file']
            name = request.form.get('name')
            width = request.form.get('width')
            height = request.form.get('height')
            unit = request.form.get('unit')
            data = Model(name=name, file=file, width=width, height=height, un_id=unit,username=username)
            ref_manager = RefManagement().create_manager()
            logger.info("[{}] Created MLManagement object.".format(username))
            logger.info("[{}] Call add_model function.".format(username))
            result = ref_manager.add_model(data=data)
            del ref_manager
            return result
        else:
            result = { 'mes' : "wrong_type" }
            return result
    except Exception as identifier:
        logger.error("[{}] Error {}".format(username,identifier))
        error = { 'mes' : str(identifier) }
        return jsonify(error)

# edit_model
# Description : เปลี่ยนข้อมูลของข้อมูลต้นแบบของวัตถุ หรือข้อมูลต้นแบบของวัตถุอ้างอิง
# Author : Athiruj Poositaporn
@model_management_api.route("/edit_model", methods=['post'])
def edit_model():
    model_type = request.form.get('type')
    model_id = request.form.get('model_id')
    file = request.files['file']
    name = request.form.get('name')
    username = request.form.get('username')
    if(model_type == "ml"):
        logger.info("[{}] Use edit ML model API.".format(username))
        data = Model(id=model_id,name=name,file=file,username=username)
        ml_manager = MLManagement().create_manager()
        logger.info("[{}] Created MLManagement object.".format(username))
        logger.info("[{}] Call edit_model function.".format(username))
        result = ml_manager.edit_model(data)
        del ml_manager
        logger.info("[{}] Deleted MLManagement object.".format(username))
    elif(model_type == "ref"):
        logger.info("[{}] Use edit Ref model API.".format(username))
        width = request.form.get('width')
        height = request.form.get('height')
        unit = request.form.get('unit')
        data = Model(id=model_id,name=name,file=file,width=width,height=height,un_id=unit,username=username)
        ref_manager = RefManagement().create_manager()
        logger.info("[{}] Created RefManagement object.".format(username))
        logger.info("[{}] Call edit_model function.".format(username))
        result = ref_manager.edit_model(data)
        del ref_manager
        logger.info("[{}] Deleted RefManagement object.".format(username))
    logger.info("[{}] Response data from change_active_model API".format(username))
    return result

# change_active_model
# Description : เปลี่ยนข้อมูลของข้อมูลต้นแบบของวัตถุ หรือข้อมูลต้นแบบของวัตถุอ้างอิงที่จะเปิดการใช้งานตาม id
# Author : Athiruj Poositaporn
@model_management_api.route("/change_active_model", methods=['post'])
def change_active_model():
    model_type = request.form.get('type')
    model_id = request.form.get('model_id')
    username = request.form.get('username')
    data = Model(id=model_id,username=username)
    if(model_type == "ml"):
        logger.info("[{}] Use change active ML model API.".format(username))
        ml_manager = MLManagement().create_manager()
        logger.info("[{}] Created MLManagement object.".format(username))
        logger.info("[{}] Call change_active_model function.".format(username))
        result = ml_manager.change_active_model(data)
        del ml_manager
        logger.info("[{}] Deleted MLManagement object.".format(username))
    elif(model_type == "ref"):
        logger.info("[{}] Use change active Ref model API.".format(username))
        ref_manager = RefManagement().create_manager()
        logger.info("[{}] Created RefManagement object.".format(username))
        logger.info("[{}] Call change_active_model function.".format(username))
        result = ref_manager.change_active_model(data)
        del ref_manager
        logger.info("[{}] Deleted RefManagement object.".format(username))
    
    logger.info("[{}] Response data from change_active_model API".format(username))
    return result


# delete_model
# Description : เปลี่ยนสถานะข้อมูลต้นแบบของวัตถุ หรือข้อมูลต้นแบบของวัตถุอ้างอิงเป็นถูกลบ
# Author : Athiruj Poositaporn
@model_management_api.route("/delete_model", methods=['post'])
def delete_model():
    model_type = request.form.get('type')
    model_id = request.form.get('model_id')
    username = request.form.get('username')
    data = Model(id=model_id,username=username)
    if(model_type == "ml"):
        logger.info("[{}] Use delete ML model API.".format(username))
        ml_manager = MLManagement().create_manager()
        logger.info("[{}] Created MLManagement object.".format(username))
        logger.info("[{}] Call delete_model function.".format(username))
        result = ml_manager.delete_model(data)
        del ml_manager
        logger.info("[{}] Deleted MLManagement object.".format(username))
    elif(model_type == "ref"):
        logger.info("[{}] Use delete Ref model API.".format(username))
        ref_manager = RefManagement().create_manager()
        logger.info("[{}] Created RefManagement object.".format(username))
        logger.info("[{}] Call delete_model function.".format(username))
        result = ref_manager.delete_model(data)
        del ref_manager
        logger.info("[{}] Deleted RefManagement object.".format(username))

    logger.info("[{}] Response data from delete_model API".format(username))
    return result
# get_all_model
# Description : เรียกข้อมูลต้นแบบของวัตถุ หรือ ข้อมูลต้นแบบของวัตถุอ้างอิงทั้งหมดที่ไม่มีสถานะถูกลบ
# Author : Athiruj Poositaporn
@model_management_api.route("/get_all_model", methods=['post'])
def get_all_model():
    model_type = request.form.get('type')
    username = request.form.get('username')
    if(model_type == "ml"):
        logger.info("[{}] Use get all ML model API.".format(username))
        ml_manager = MLManagement().create_manager()
        logger.info("[{}] Created MLManagement object.".format(username))
        logger.info("[{}] Call get_all_model function.".format(username))
        result = ml_manager.get_all_model()
        del ml_manager
        logger.info("[{}] Deleted MLManagement object.".format(username))
    elif(model_type == "ref"):
        logger.info("[{}] Use get all ML model API.".format(username))
        ref_manager = RefManagement().create_manager()
        logger.info("[{}] Created RefManagement object.".format(username))
        logger.info("[{}] Call get_all_model function.".format(username))
        result = ref_manager.get_all_model()
        del ref_manager
        logger.info("[{}] Deleted RefManagement object.".format(username))
    
    logger.info("[{}] Response data from get_all_model API".format(username))
    return result
    

# get_model_by_id
# Description : เรียกข้อมูลต้นแบบของวัตถุ หรือข้อมูลต้นแบบของวัตถุอ้างอิงที่ไม่มีสถานะถูกลบตาม id
# Author : Athiruj Poositaporn
@model_management_api.route("/get_model_by_id", methods=['post'])
def get_model_by_id():
    model_type = request.form.get('type')
    model_id = int(request.form.get('model_id'))
    username = request.form.get('username')
    data = Model(id=model_id,username=username)
    if(model_type == "ml"):
        logger.info("[{}] Use get ML model by id API.".format(username))
        ml_manager = MLManagement().create_manager()
        logger.info("[{}] Created MLManagement object.".format(username))
        logger.info("[{}] Call get_model_by_id function.".format(username))
        result = ml_manager.get_model_by_id(data)
        del ml_manager
        logger.info("[{}] Deleted MLManagement object.".format(username))
    elif(model_type == "ref"):
        logger.info("[{}] Use get Ref model by id API.".format(username))
        ref_manager = RefManagement().create_manager()
        logger.info("[{}] Created RefManagement object.".format(username))
        logger.info("[{}] Call get_model_by_id function.".format(username))
        result = ref_manager.get_model_by_id(data)
        del ref_manager
        logger.info("[{}] Deleted RefManagement object.".format(username))
    else:
        result = {
            "mes" : "Wrong model type ! : {}".format(model_type)
        }
    
    logger.info("[{}] Response data from get_model_by_id API".format(username))
    return result
    
