# ml_management_api
# Description : ไฟล์สำหรับการพัฒนา API ของการจัดการเพิ่ม แก้ไข และลบ
# ข้อมูลต้นอบบของวัตถุ
# Author : Athiruj Poositaporn

from flask import Flask, request, Blueprint ,make_response
from .. import db_config
# from pymongo import MongoClient
# from bson.json_util import dumps

from ..model_management.model import Model
from ..model_management.model_manager import MLManagement, RefManagement

# add_ml_model
# Description : เพิ่มข้อมูลของชื่อและไฟล์ .weights ของข้อมูลต้นแบบของวัตถุ 
# Author : Athiruj Poositaporn
@ml_management_api.route("/add_model", methods=['post'])
def add_model():
    model_type = request.form.get('type')
    if(model_type == "ml"):
        file = request.files['file']
        name = request.form.get('mlmo_name')
        data = Model(name = name , file=file)
        ml_manager = MLManagement().create_manager()
        result = ml_manager.add_model(data=data)
        del ml_manager
        return result
    elif(model_type == "ref"):
        file = request.files['file']
        name = request.form.get('remo_name')
        width = request.form.get('width')
        height = request.form.get('height')
        unit = request.form.get('unit')

        data = Model(name=name, file=file, width=width, height=height, un_id=unit)
        ref_manager = RefManagement().create_manager()
        result = ref_manager.add_model(data=data)
        del ref_manager
        return result
        