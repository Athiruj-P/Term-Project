# model_management_api
# Description : ไฟล์สำหรับการพัฒนา API ของการจัดการเพิ่ม แก้ไข และลบ
# ข้อมูลต้นอบบของวัตถุ
# Author : Athiruj Poositaporn
from flask import Flask, request, Blueprint ,make_response,jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,jwt_refresh_token_required,
    create_refresh_token
)
from datetime import date , datetime
import logging.config
from pymongo import MongoClient
from bson.json_util import dumps
from .. import db_config
from .log_manager import LogManager
from .. import err_msg

log_management_api = Blueprint('log_management_api', __name__)
logger = logging.getLogger("log_management_api")

# log_management_api
# Description : เรียกข้อมูลประวัติการใช้งานระบบตามช่วงของวันที่และเวลาที่กำหนด
# Author : Athiruj Poositaporn
@log_management_api.route("/get_log", methods=['post'])
@jwt_required
def get_log():
    try:
        # logger.info("[{}] .".format(username))
        date_type = request.form.get('date_type')
        group = request.form.get('group')
        # username = request.form.get('username')
        username = get_jwt_identity()
        if(date_type == "today"):
            today = date.today().strftime("%Y-%m-%d") # Date in YYYY-MM-DD (2020-01-10)
            log_manager = LogManager(today_date=today,group=group,username=username)
            result = log_manager.get_today_log()

            if(result['status'] == "error"):
                    return result , 400
            elif(result['status'] == "system_error"):
                return result , 400

            return result , 200
        elif (date_type == "date_picker"):
            # datetime_object = datetime.strptime(date_type, '%Y-%m-%d %H:%M:%S')
            # datetime_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')
            log_manager = LogManager(start_date=start_date,end_date=end_date,start_time=start_time,end_time=end_time,group=group,username=username)
            result = log_manager.get_log_by_date()
            
            if(result['status'] == "error"):
                    return result , 400
            elif(result['status'] == "system_error"):
                return result , 400
            return result , 200
        else:
            result = { 'mes' : "wrong_type" , 'status' : 'system_error'}
            return result , 400
                    
    except Exception as identifier:
        logger.error("Error {}".format(identifier))
        result = { 'mes' : str(identifier) , 'status' : "system_error"}
        return result , 400

# get_min_max_date
# Description : เรียกข้อมูลวันที่แรกและวันที่ล่าสุดของไฟล์ประวัติการใช้งาน
# Author : Athiruj Poositaporn
@log_management_api.route("/get_min_max_date", methods=['post'])
@jwt_required
def get_min_max_date():
    try:
        # logger.info("[{}] .".format(username))
        username = get_jwt_identity()
        today = date.today().strftime("%Y-%m-%d") # Date in YYYY-MM-DD (2020-01-10)
        log_manager = LogManager(username=username)
        result = log_manager.get_min_max_date()

        if(result['status'] == "error"):
                return result , 400
        elif(result['status'] == "system_error"):
            return result , 400
        
        return result , 200
    except Exception as identifier:
        logger.error("[{}] Error {}".format(username,identifier))
        result = { 'mes' : str(identifier) , 'status' : "system_error"}
        return result , 400

# add_log
# Description : บันทึกการกระทำของผู้ใช้งานระบบ
# Author : Athiruj Poositaporn
@log_management_api.route("/add_log", methods=['post'])
@jwt_required
def add_log():
    try:
        username = get_jwt_identity()
        action = request.form.get('action' , None)
        today = date.today().strftime("%Y-%m-%d") # Date in YYYY-MM-DD (eg. 2020-01-10)
        log_manager = LogManager(username=username,action=action)
        log_manager.add_log()
        result= {
            'status':'success'
        }
        return result , 200
    except Exception as identifier:
        logger.error("[{}] Error {}".format(username,identifier))
        result = { 'mes' : str(identifier) , 'status' : "system_error"}
        return result , 400