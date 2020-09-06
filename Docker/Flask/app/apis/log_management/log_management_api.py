# model_management_api
# Description : ไฟล์สำหรับการพัฒนา API ของการจัดการเพิ่ม แก้ไข และลบ
# ข้อมูลต้นอบบของวัตถุ
# Author : Athiruj Poositaporn
from flask import Flask, request, Blueprint ,make_response,jsonify
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
def get_log():
    try:
        # logger.info("[{}] .".format(username))
        date_type = request.form.get('date_type')
        group = request.form.get('group')
        username = request.form.get('username')
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
            return result
        else:
            result = { 'mes' : "wrong_type" , 'status' : 'system_error'}
            return result , 400
                    
    except Exception as identifier:
        logger.error("[{}] Error {}".format(username,identifier))
        result = { 'mes' : str(identifier) , 'status' : "system_error"}
        return result , 400