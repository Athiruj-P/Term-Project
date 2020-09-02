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

@model_management_api.route("/check_duplicate_name", methods=['post'])
def check_duplicate_name():
    try:
        model_type = request.form.get('type',None)
        name = request.form.get('name',None)
        model_id = request.form.get('model_id',None)
        data = Model(name = name , id=model_id)

        if(model_type == "ml"):
            ml_manager = MLManagement().create_manager()
            result = ml_manager.is_duplicate_name(data)
            result = {'is_duplicate':result}
            return result
        elif(model_type == "ref"):
            ref_manager = RefManagement().create_manager()
            result = ref_manager.is_duplicate_name(data)
            result = {'is_duplicate':result}
            return result
        else:
            result = { 'mes' : "wrong_type" , 'status' : "error"}
            return result , 400
    except Exception as identifier:
        logger.error("Error {}".format(identifier))
        error = { 'mes' : str(identifier) , 'status' : "system_error"}
        return jsonify(error) , 400


# add_ml_model
# Description : เพิ่มข้อมูลของชื่อและไฟล์ .weights ของข้อมูลต้นแบบของวัตถุ 
# Author : Athiruj Poositaporn
@model_management_api.route("/add_model", methods=['put'])
def add_model():
    try:
        model_type = request.form.get('type',None)
        username = request.form.get('username',None)
        # logger_user.info("[{}] This is user".format(username))
        if(model_type == "ml"):
            logger.info("[{}] Use add ML model API.".format(username))
            file = request.files.get('file' , None)
            # file = request.files['file']
            name = request.form.get('name',None)
            data = Model(name = name , file=file,username=username)
            ml_manager = MLManagement().create_manager()
            logger.info("[{}] Created MLManagement object.".format(username))
            logger.info("[{}] Call add_model function.".format(username))
            result = ml_manager.add_model(data=data)
            del ml_manager
            # logger.debug("[] : {}".format(result))

            # logger.debug("Line 41")
            if(result['status'] == "error"):
                return result , 400 
            elif(result['status'] == "system_error"):
                return result , 400 

            # logger.debug("Line 47")
            logger.info("[{}] Response data from delete_model API".format(username))
            return result , 200

        elif(model_type == "ref"):
            logger.info("[{}] Use add Ref model API.".format(username))
            file = request.files.get('file' , None)
            name = request.form.get('name',None)
            width = request.form.get('width',None)
            height = request.form.get('height',None)
            un_id = request.form.get('un_id',None)
            data = Model(name=name, file=file, width=width, height=height, un_id=un_id,username=username)
            ref_manager = RefManagement().create_manager()
            logger.info("[{}] Created MLManagement object.".format(username))
            logger.info("[{}] Call add_model function.".format(username))
            result = ref_manager.add_model(data=data)
            del ref_manager

            if(result['status'] == "error"):
                return result , 400 
            elif(result['status'] == "system_error"):
                return result , 400 

            logger.info("[{}] Response data from delete_model API".format(username))
            return result , 200
        else:
            result = { 'mes' : "wrong_type" }
            return result , 400
    except Exception as identifier:
        logger.error("[{}] Error {}".format(username,identifier))
        error = { 'mes' : str(identifier) }
        return jsonify(error) , 400

# edit_model
# Description : เปลี่ยนข้อมูลของข้อมูลต้นแบบของวัตถุ หรือข้อมูลต้นแบบของวัตถุอ้างอิง
# Author : Athiruj Poositaporn
@model_management_api.route("/edit_model", methods=['put'])
def edit_model():
    try:
        model_type = request.form.get('type',None)
        model_id = request.form.get('model_id',None)
        file = request.files.get('file',None)
        name = request.form.get('name',None)
        username = request.form.get('username',None)
        # logger.debug("model id (API): {}".format(int(model_id)))
        if(model_type == "ml"):
            logger.info("[{}] Use edit ML model API.".format(username))
            data = Model(id=model_id,name=name,file=file,username=username)
            ml_manager = MLManagement().create_manager()
            logger.info("[{}] Created MLManagement object.".format(username))
            logger.info("[{}] Call edit_model function.".format(username))
            result = ml_manager.edit_model(data)
            del ml_manager

            if(result['status'] == "error"):
                return result , 400
            elif(result['status'] == "system_error"):
                return result , 400


            logger.info("[{}] Edited MLManagement object.".format(username))
            logger.info("[{}] Response data from edit_model API".format(username))
            return result , 200
        elif(model_type == "ref"):
            logger.info("[{}] Use edit Ref model API.".format(username))
            width = request.form.get('width',None)
            height = request.form.get('height',None)
            unit = request.form.get('unit',None)
            data = Model(id=model_id,name=name,file=file,width=width,height=height,un_id=unit,username=username)
            ref_manager = RefManagement().create_manager()
            logger.info("[{}] Created RefManagement object.".format(username))
            logger.info("[{}] Call edit_model function.".format(username))
            result = ref_manager.edit_model(data)
            del ref_manager
            logger.info("[{}] Edited Reference Management object.".format(username))
            logger.info("[{}] Response data from edit_model API".format(username))
            return result , 200
    except Exception as identifier:
        pass

# change_active_model
# Description : เปลี่ยนข้อมูลของข้อมูลต้นแบบของวัตถุ หรือข้อมูลต้นแบบของวัตถุอ้างอิงที่จะเปิดการใช้งานตาม id
# Author : Athiruj Poositaporn
@model_management_api.route("/change_active_model", methods=['post'])
def change_active_model():
    model_type = request.form.get('type',None)
    model_id = request.form.get('model_id',None)
    username = request.form.get('username',None)
    data = Model(id=model_id,username=username)
    if(model_type == "ml"):
        logger.info("[{}] Use change active ML model API.".format(username))
        ml_manager = MLManagement().create_manager()
        logger.info("[{}] Created MLManagement object.".format(username))
        logger.info("[{}] Call change_active_model function.".format(username))
        result = ml_manager.change_active_model(data)
        del ml_manager
        if(result['status'] == "error"):
                    return result , 400
        elif(result['status'] == "system_error"):
            return result , 400
        logger.info("[{}] Deleted MLManagement object.".format(username))
        logger.info("[{}] Response data from change_active_model API".format(username))
        return result , 200
    elif(model_type == "ref"):
        logger.info("[{}] Use change active Ref model API.".format(username))
        ref_manager = RefManagement().create_manager()
        logger.info("[{}] Created RefManagement object.".format(username))
        logger.info("[{}] Call change_active_model function.".format(username))
        result = ref_manager.change_active_model(data)
        del ref_manager
        if(result['status'] == "error"):
                    return result , 400
        elif(result['status'] == "system_error"):
            return result , 400
        logger.info("[{}] Deleted RefManagement object.".format(username))
        logger.info("[{}] Response data from change_active_model API".format(username))
        return result , 200
    


# delete_model
# Description : เปลี่ยนสถานะข้อมูลต้นแบบของวัตถุ หรือข้อมูลต้นแบบของวัตถุอ้างอิงเป็นถูกลบ
# Author : Athiruj Poositaporn
@model_management_api.route("/delete_model", methods=['post'])
def delete_model():
    model_type = request.form.get('type',None)
    model_id = request.form.get('model_id',None)
    username = request.form.get('username',None)
    data = Model(id=model_id,username=username)
    if(model_type == "ml"):
        logger.info("[{}] Use delete ML model API.".format(username))
        ml_manager = MLManagement().create_manager()
        logger.info("[{}] Created MLManagement object.".format(username))
        logger.info("[{}] Call delete_model function.".format(username))
        result = ml_manager.delete_model(data)
        del ml_manager
        if(result['status'] == "error"):
                    return result , 400
        elif(result['status'] == "system_error"):
            return result , 400
        logger.info("[{}] Deleted MLManagement object.".format(username))
        logger.info("[{}] Response data from delete_model API".format(username))
        return result , 200

    elif(model_type == "ref"):
        logger.info("[{}] Use delete Ref model API.".format(username))
        ref_manager = RefManagement().create_manager()
        logger.info("[{}] Created RefManagement object.".format(username))
        logger.info("[{}] Call delete_model function.".format(username))
        result = ref_manager.delete_model(data)
        del ref_manager
        if(result['status'] == "error"):
                    return result , 400
        elif(result['status'] == "system_error"):
            return result , 400
        logger.info("[{}] Deleted RefManagement object.".format(username))
        logger.info("[{}] Response data from delete_model API".format(username))
        return result , 200


# get_all_model
# Description : เรียกข้อมูลต้นแบบของวัตถุ หรือ ข้อมูลต้นแบบของวัตถุอ้างอิงทั้งหมดที่ไม่มีสถานะถูกลบ
# Author : Athiruj Poositaporn
@model_management_api.route("/get_all_model", methods=['post'])
def get_all_model():
    try:
        model_type = request.form.get('type',None)
        username = request.form.get('username',None)
        if(model_type == "ml"):
            logger.info("[{}] Use get all ML model API.".format(username))
            ml_manager = MLManagement().create_manager()
            logger.info("[{}] Created MLManagement object.".format(username))
            logger.info("[{}] Call get_all_model function.".format(username))
            result = ml_manager.get_all_model(username)
            del ml_manager
            logger.info("[{}] Deleted MLManagement object.".format(username))
        elif(model_type == "ref"):
            logger.info("[{}] Use get all ML model API.".format(username))
            ref_manager = RefManagement().create_manager()
            logger.info("[{}] Created RefManagement object.".format(username))
            logger.info("[{}] Call get_all_model function.".format(username))
            result = ref_manager.get_all_model(username)
            del ref_manager

            if(result['status'] == "system_error"):
                return result , 400

            logger.info("[{}] Deleted RefManagement object.".format(username))
        
        logger.info("[{}] Response data from get_all_model API".format(username))
        return result , 200
    except Exception as identifier:
        return result , 400

# get_all_unit
# Description : เรียกข้อมูลหน่วยในการวัดขนาดววัตถุทั้งหมด
# Author : Athiruj Poositaporn
@model_management_api.route("/get_all_unit", methods=['post'])
def get_all_unit():
    try:
        username = request.form.get('username',None)

        logger.info("[{}] Use get all units API.".format(username))
        ref_manager = RefManagement().create_manager()
        logger.info("[{}] Created RefManagement object.".format(username))
        logger.info("[{}] Call get_all_model function.".format(username))
        result = ref_manager.get_all_unit(username)
        del ref_manager

        if(result['status'] == "system_error"):
            return result , 400

        logger.info("[{}] Deleted RefManagement object.".format(username))
        
        logger.info("[{}] Response data from get_all_model API".format(username))
        return result , 200
    except Exception as identifier:
        return result , 400


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
    
