# log_management
# Description : คลาส LogManager ใช้จัดการเพิ่มและดึงข้อมูลของ log
# Author : Athiruj Poositaporn

from flask import jsonify
from bson.json_util import dumps
from datetime import date , datetime
import logging.config
import re
import os

class LogManager():
    def __init__(self,today_date='',group='',username='' ,action='' ,start_date='',end_date='',start_time='',end_time=''):
        self.logger = logging.getLogger("LogManager")
        self.logger_user = logging.getLogger("user_management")

        self.logger.info("Set log variable")
        parent = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) 
        self.log_path = os.path.join(parent,"log")
        self.today_date = today_date
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.group = group
        self.username = username
        self.action = action

        self.group_list = ['all' , 'USER' , 'SYSTEM']
    # is_date_obj
    # Description : ตรวจสอบว่า str_date เป็น date ได้หรือไม่
    # Author : Athiruj Poositaporn
    def is_date_obj(self,str_date):
        try:
            datetime.strptime(str_date, '%Y-%m-%d')
            return True
        except:
            return False

    # is_datetime_obj
    # Description : ตรวจสอบว่า str_date_time เป็น datetime ได้หรือไม่
    # Author : Athiruj Poositaporn
    def is_datetime_obj(self,str_date_time):
        try:
            datetime.strptime(str_date_time, '%Y-%m-%d %H:%M:%S')
            return True
        except:
            return False

    # is_file_exist
    # Description : ตรวจสอบว่า str_file_path สามารถเข้าถึงไฟล์ได้หรือไม่
    # Author : Athiruj Poositaporn
    def is_file_exist(self,str_file_path):
        try:
            file_read = open(str_file_path, "r")
            return True
        except:
            return False
        finally:
            file_read.close()

    # get_today_log
    # Description : ดึงข้อมูล log ในวันที่ปัจจุบัน
    # Author : Athiruj Poositaporn    
    def get_today_log(self):
        try:
            self.logger.info("[{}] Prepair date data to query.".format(self.username))

            if not self.is_date_obj(self.today_date):
                self.logger.warning("[{}] {}".format(self.username,err_msg.msg['wrong_date']))
                raise TypeError(err_msg.msg['wrong_date'])
            elif self.group not in self.group_list:
                self.logger.warning("[{}] {}".format(self.username,err_msg.msg['wrong_group']))
                raise TypeError(err_msg.msg['wrong_group'])
                
            log_file_name = self.today_date + ".log"
            log_file_path = os.path.join(self.log_path,log_file_name)
            if not self.is_file_exist(log_file_path):
                self.logger.warning("[{}] {}".format(self.username,err_msg.msg['file_not_exist']))
                raise TypeError(err_msg.msg['file_not_exist'])

            log_file = open(log_file_path, "r")
            self.logger.info("[{}] Read log {} .".format(self.username,log_file_name))
            result_date=[]
            filter_condition = False
            if(self.group == 'all'):
                filter_condition = True
            
            today_date_obj = datetime.strptime(self.today_date, '%Y-%m-%d')
            for line in log_file:
                if(self.is_date_obj(line[:10])):
                    line_date_obj = datetime.strptime(line[:10], '%Y-%m-%d')
                else:
                    continue

                if (today_date_obj == line_date_obj and ((re.search(self.group, line), True)[filter_condition]) ):
                    result_date.append(line)
                elif(today_date_obj < line_date_obj):
                    break
                else:
                    continue
            log_file.close()
            self.logger.info("[{}] Close log file.".format(self.username))
            self.logger.info("[{}] Got all today logs.".format(self.username))
            
            result = {'log':result_date , 'status':'success'}
            return result
        except Exception as identifier:
            try:
                list(err_msg.msg.keys())[list(err_msg.msg.values()).index(str(identifier))]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                self.logger.warning("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    # get_log_by_date
    # Description : ดึงข้อมูล log ตามวันที่และเวลาที่กำหนด
    # Author : Athiruj Poositaporn   
    def get_log_by_date(self):
        try:
            self.logger.info("[{}] Prepair date data to query.".format(self.username))
            result_date = []
            file_list = []
            filter_condition = False
            str_start_datetime = self.start_date + " "+ self.start_time
            str_end_datetime = self.end_date + " "+ self.end_time

            if(not self.is_date_obj(self.start_date)):
                self.logger.warning("[{}] {}".format(self.username,err_msg.msg['wrong_start_date']))
                raise TypeError(err_msg.msg['wrong_start_date'])
            elif(not self.is_date_obj(self.end_date)):
                self.logger.warning("[{}] {}".format(self.username,err_msg.msg['wrong_end_date']))
                raise TypeError(err_msg.msg['wrong_end_date'])
            elif(not self.is_datetime_obj(str_start_datetime)):
                self.logger.warning("[{}] {}".format(self.username,err_msg.msg['wrong_start_datetime']))
                raise TypeError(err_msg.msg['wrong_start_datetime'])
            elif(not self.is_datetime_obj(str_end_datetime)):
                self.logger.warning("[{}] {}".format(self.username,err_msg.msg['wrong_end_datetime']))
                raise TypeError(err_msg.msg['wrong_end_datetime'])
            elif self.group not in self.group_list:
                self.logger.warning("[{}] {}".format(self.username,err_msg.msg['wrong_group']))
                raise TypeError(err_msg.msg['wrong_group'])
            
            start_date_obj = datetime.strptime(self.start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(self.end_date, '%Y-%m-%d').date()
            start_datetime_obj = datetime.strptime(str_start_datetime, '%Y-%m-%d %H:%M:%S')
            end_datetime_obj = datetime.strptime(str_end_datetime, '%Y-%m-%d %H:%M:%S')

            for file in sorted(os.listdir(self.log_path)):
                if not self.is_date_obj(file[:10]):
                    self.logger.warning("[{}] Wrong file format.".format(self.username))
                    continue
                file_name = datetime.strptime(file[:10], '%Y-%m-%d').date()
                if (file.endswith(".log") and start_date_obj <= file_name and end_date_obj >= file_name ):
                    log_file_path = os.path.join(self.log_path,file)
                    if not self.is_file_exist(log_file_path):
                        self.logger.warning("[{}] File dose not exist.".format(self.username))
                        continue
                    file_list.append(log_file_path)
            
            if(self.group == 'all'):
                filter_condition = True
            
            for file in file_list:
                log_file_path = os.path.join(self.log_path,file)
                log_file = open(log_file_path, "r")
                self.logger.info("[{}] Read log {} .".format(self.username,file))
                for line in log_file:
                    if(self.is_datetime_obj(line[:19])):
                        line_datetime_obj = datetime.strptime(line[:19], '%Y-%m-%d %H:%M:%S')
                    else:
                        continue

                    if (start_datetime_obj <= line_datetime_obj and end_datetime_obj >= line_datetime_obj and ((re.search(self.group, line), True)[filter_condition]) ):
                        result_date.append(line)
                    elif(end_datetime_obj < line_datetime_obj):
                        break
                    else:
                        continue
                log_file.close()

            self.logger.info("[{}] Close log file.".format(self.username))
            self.logger.info("[{}] Got all log data.".format(self.username))
            result = {'log':result_date , 'status':'success'}
            return result
        except Exception as identifier:
            try:
                list(err_msg.msg.keys())[list(err_msg.msg.values()).index(str(identifier))]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                self.logger.warning("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    # get_min_max_date
    # Description : ดึงข้อมูลวันที่ของ log ที่เคยบันทึกวันแรก และวันที่ของ log ที่บันทึกล่าสุด
    # Author : Athiruj Poositaporn   
    def get_min_max_date(self):
        try:
            self.logger.info("[{}] Prepair date data to query.".format(self.username))
            file_list = []
            filter_condition = False
            
            for file in sorted(os.listdir(self.log_path)):
                # self.logger.debug("file name : [{}]".format(file))
                if not self.is_date_obj(file[:10]):
                    self.logger.warning("[{}] Wrong file format.".format(self.username))
                    continue
                file_name = datetime.strptime(file[:10], '%Y-%m-%d').date()
                if (file.endswith(".log")):
                    file_list.append(file[:10])

            result_date = {
                'minDate' : file_list[0],
                'maxDate' : file_list[-1],
            }
            self.logger.info("[{}] Close log file.".format(self.username))
            self.logger.info("[{}] Got min and max date.".format(self.username))
            result = {'min_max_date':result_date , 'status':'success'}
            return result
        except Exception as identifier:
            try:
                list(err_msg.msg.keys())[list(err_msg.msg.values()).index(str(identifier))]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                self.logger.warning("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    # add_log
    # Description : เพิ่มข้อมูลการกระทำของผู้ใช้งาน (Admin , User)
    # Author : Athiruj Poositaporn   
    def add_log(self):
        self.logger_user.info("[{}] {}".format(self.username,self.action))

    def __del__(self):
        pass