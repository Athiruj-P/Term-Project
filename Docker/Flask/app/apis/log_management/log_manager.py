from flask import jsonify
from bson.json_util import dumps
from datetime import date , datetime
import logging.config
import re
import os

class LogManager():
    def __init__(self,today_date='',group='',username='',start_date='',end_date='',start_time='',end_time=''):
        self.logger = logging.getLogger("LogManager")
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

        self.logger.info("parent : {}".format(parent))
    
    def get_today_log(self):
        try:
            self.logger.info("[{}] Prepair date data to query.".format(self.username))
            log_file_name = self.today_date + ".log"
            log_file_path = os.path.join(self.log_path,log_file_name)
            log_file = open(log_file_path, "r")
            self.logger.info("[{}] Read log file.".format(self.username))
            result_date=[]
            filter_condition = False
            if(self.group == 'all'):
                filter_condition = True

            today_date_obj = datetime.strptime(self.today_date, '%Y-%m-%d')
            for line in log_file:
                line_date_obj = datetime.strptime(line[:10], '%Y-%m-%d')
                if (today_date_obj == line_date_obj and ((re.search(self.group, line), True)[filter_condition]) ):
                    result_date.append(line)
                elif(today_date_obj < line_date_obj):
                    break
                else:
                    continue
            log_file.close()
            self.logger.info("[{}] Close log file.".format(self.username))
            self.logger.info("[{}] Got all today logs.".format(self.username))
            return jsonify(result_date)
        except Exception as identifier:
            self.logger.error("[{}] Error {}".format(self.username,identifier))
            error = { 'mes' : str(identifier) }
            return jsonify(error)
    def get_log_by_date(self):
        try:
            self.logger.info("[{}] Prepair date data to query.".format(self.username))
            start_date = datetime.strptime(self.start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(self.end_date, '%Y-%m-%d').date()
            result_date = []
            file_list = []
            for file in os.listdir(self.log_path):
                file_name = datetime.strptime(file[:10], '%Y-%m-%d').date()
                self.logger.debug("file_name : {} - {}".format(start_date >= file_name , end_date <= file_name))
                if (file.endswith(".log") and start_date >= file_name and end_date <= file_name ):
                    file_list.append(file)
            
            return jsonify(file_list)
        except Exception as identifier:
            self.logger.error("[{}] Error {}".format(self.username,identifier))
            error = { 'mes' : str(identifier) }
            return jsonify(error)
    def __del__(self):
        pass