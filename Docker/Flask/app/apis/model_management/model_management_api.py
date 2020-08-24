# model_management_api
# Description : ไฟล์สำหรับการพัฒนา API ของการจัดการเพิ่ม แก้ไข และลบ
# ข้อมูลต้นอบบของวัตถุ
# Author : Athiruj Poositaporn
from flask import Flask, request, Blueprint ,make_response
from pymongo import MongoClient
from bson.json_util import dumps
from .. import db_config

from .model import Model
from .model_manager import MLManagement, RefManagement

model_management_api = Blueprint('model_management_api', __name__)

# add_ml_model
# Description : เพิ่มข้อมูลของชื่อและไฟล์ .weights ของข้อมูลต้นแบบของวัตถุ 
# Author : Athiruj Poositaporn
@model_management_api.route("/add_model", methods=['post'])
def add_model():
    model_type = request.form.get('type')
    if(model_type == "ml"):
        file = request.files['file']
        name = request.form.get('name')
        data = Model(name = name , file=file)
        ml_manager = MLManagement().create_manager()
        result = ml_manager.add_model(data=data)
        del ml_manager
        return result

    elif(model_type == "ref"):
        file = request.files['file']
        name = request.form.get('name')
        width = request.form.get('width')
        height = request.form.get('height')
        unit = request.form.get('unit')
        # isinstance(c, int) or isinstance(c, float)
        data = Model(name=name, file=file, width=width, height=height, un_id=unit)
        ref_manager = RefManagement().create_manager()
        result = ref_manager.add_model(data=data)
        del ref_manager
        return result
    else:
        result = {
            'mes' : "wrong_type"
        }
        return result

# edit_model
# Description : เปลี่ยนข้อมูลของข้อมูลต้นแบบของวัตถุ หรือข้อมูลต้นแบบของวัตถุอ้างอิง
# Author : Athiruj Poositaporn
@model_management_api.route("/edit_model", methods=['post'])
def edit_model():
    model_type = request.form.get('type')
    model_id = request.form.get('model_id')
    file = request.files['file']
    name = request.form.get('name')
    if(model_type == "ml"):
        data = Model(id=model_id,name=name,file=file)
        ml_manager = MLManagement().create_manager()
        result = ml_manager.edit_model(data)
        del ml_manager
        return result
    elif(model_type == "ref"):
        width = request.form.get('width')
        height = request.form.get('height')
        unit = request.form.get('unit')
        data = Model(id=model_id,name=name,file=file,width=width,height=height,un_id=unit)
        ref_manager = RefManagement().create_manager()
        result = ref_manager.edit_model(data)
        del ref_manager
        return result

# change_active_model
# Description : เปลี่ยนข้อมูลของข้อมูลต้นแบบของวัตถุ หรือข้อมูลต้นแบบของวัตถุอ้างอิงที่จะเปิดการใช้งานตาม id
# Author : Athiruj Poositaporn
@model_management_api.route("/change_active_model", methods=['post'])
def change_active_model():
    model_type = request.form.get('type')
    model_id = request.form.get('model_id')
    data = Model(id=model_id)
    if(model_type == "ml"):
        ml_manager = MLManagement().create_manager()
        result = ml_manager.change_active_model(data)
        del ml_manager
        return result
    elif(model_type == "ref"):
        ref_manager = RefManagement().create_manager()
        result = ref_manager.change_active_model(data)
        del ref_manager
        return result


# delete_model
# Description : เปลี่ยนสถานะข้อมูลต้นแบบของวัตถุ หรือข้อมูลต้นแบบของวัตถุอ้างอิงเป็นถูกลบ
# Author : Athiruj Poositaporn
@model_management_api.route("/delete_model", methods=['post'])
def delete_model():
    model_type = request.form.get('type')
    model_id = int(request.form.get('model_id'))
    data = Model(id=model_id)
    if(model_type == "ml"):
        ml_manager = MLManagement().create_manager()
        result = ml_manager.delete_model(data)
        del ml_manager
        return result
    elif(model_type == "ref"):
        ref_manager = RefManagement().create_manager()
        result = ref_manager.delete_model(data)
        del ref_manager
        return result

# get_all_model
# Description : เรียกข้อมูลต้นแบบของวัตถุ หรือ ข้อมูลต้นแบบของวัตถุอ้างอิงทั้งหมดที่ไม่มีสถานะถูกลบ
# Author : Athiruj Poositaporn
@model_management_api.route("/get_all_model", methods=['post'])
def get_all_model():
    model_type = request.form.get('type')
    if(model_type == "ml"):
        ml_manager = MLManagement().create_manager()
        result = ml_manager.get_all_model()
        del ml_manager
        return result
    elif(model_type == "ref"):
        ref_manager = RefManagement().create_manager()
        result = ref_manager.get_all_model()
        del ref_manager
        return result

# get_model_by_id
# Description : เรียกข้อมูลต้นแบบของวัตถุ หรือข้อมูลต้นแบบของวัตถุอ้างอิงที่ไม่มีสถานะถูกลบตาม id
# Author : Athiruj Poositaporn
@model_management_api.route("/get_model_by_id", methods=['post'])
def get_model_by_id():
    model_type = request.form.get('type')
    model_id = int(request.form.get('model_id'))
    data = Model(id=model_id)
    if(model_type == "ml"):
        ml_manager = MLManagement().create_manager()
        result = ml_manager.get_model_by_id(data)
        del ml_manager
    elif(model_type == "ref"):
        ref_manager = RefManagement().create_manager()
        result = ref_manager.get_model_by_id(data)
        del ref_manager
    else:
        result = {
            "mes" : "Wrong model type ! : {}".format(model_type)
        }
    
    return result
    
