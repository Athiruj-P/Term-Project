# ml_management_api
# Description : ไฟล์สำหรับการพัฒนา API ของการจัดการเพิ่ม แก้ไข และลบ
# ข้อมูลต้นอบบของวัตถุ
# Author : Athiruj Poositaporn

from flask import Flask, request, jsonify ,Blueprint ,make_response
from pymongo import MongoClient
from bson.json_util import dumps
import uuid 
import os
from .. import db_config

# Database connection
URI = "mongodb://"+db_config.item["db_username"]+":" + \
    db_config.item["db_password"]+"@"+db_config.item["db_host"]
db_connect = MongoClient(URI)
DPML_db = db_connect[db_config.item["db_name"]]
mlmo_collection = db_config.item["db_col_mlmo"]

# Set const variable (path)
parent = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) 
ml_path = os.path.join(parent, db_config.item["db_file_path"], db_config.item["ml_path"])
ml_management_api = Blueprint('ml_management_api', __name__)

# add_ml_model
# Description : เพิ่มข้อมูลของชื่อและไฟล์ .weights ของข้อมูลต้นแบบของวัตถุ 
# Author : Athiruj Poositaporn
@ml_management_api.route("/add_ml_model", methods=['post' , 'get'])
def add_ml_model():
    try:
        mlmo_name = request.form.get('mlmo_name')
        ml_model = request.files['file']
        file_name = uuid.uuid4().hex + "." + ml_model.filename.split('.')[-1]
        file_path = os.path.join(ml_path,file_name)
        ml_model.save(file_path)

        result = DPML_db[mlmo_collection].find_one({
                "mlmo_name": mlmo_name,
                "mlmo_status": {
                    "$not": {
                        "$in": [0]
                }
            }
        })

        if not result:
            last_mlmo = DPML_db[mlmo_collection].find_one(sort=[(db_config.item["fld_mlmo_id"], -1)])
            last_id = last_mlmo['mlmo_id'] + 1
            new_model = {
                db_config.item["fld_mlmo_id"] : last_id,
                db_config.item["fld_mlmo_name"] : mlmo_name,
                db_config.item["fld_mlmo_path"] : file_path,
                db_config.item["fld_mlmo_status"] : db_config.item["fld_mlmo_status_disable"]
            }
            db_connect.close()
            new_insert = DPML_db[mlmo_collection].insert_one(new_model)
            return jsonify(file_name,file_path)
        
        else:
            db_connect.close()
            return jsonify("duplicate_name")

    except Exception as identifier:
        db_connect.close()
        error = {
            "mes" : str(identifier)
        }
        return jsonify(error)
    