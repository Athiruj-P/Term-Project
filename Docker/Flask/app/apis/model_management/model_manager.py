# model_management
# Description : คลาสของการจัดการข้อมูลต้นแบบของวัตถุและวัตถุอ้างอิง
# โดยใช้ Design pattern "Factory Method"
# Author : Athiruj Poositaporn
from __future__ import annotations
import logging.config
from flask import jsonify
from bson.json_util import dumps
from abc import ABC, abstractmethod
from pymongo import MongoClient
import uuid 
import re
import os
from .model import Model
from .. import db_config
from .. import err_msg

# ModelManagement
# Description : Abstract class สำหรับการสร้าง object ของการจัดการข้อมูลต้นแบบของวัตถุและวัตถุอ้างอิง
# Author : Athiruj Poositaporn
class ModelManagement(ABC):
    @abstractmethod
    def create_manager(self):
        return ""

# MLManagement
# Description :คลาสสำหรับการสร้าง object ของการจัดการข้อมูลต้นแบบของวัตถุ
# Author : Athiruj Poositaporn
class MLManagement(ModelManagement):
    def create_manager(self) -> MLManager:
        return MLManager()

# RefManagement
# Description :คลาสสำหรับการสร้าง object ของการจัดการข้อมูลต้นแบบของวัตถุอ้างอิง
# Author : Athiruj Poositaporn
class RefManagement(ModelManagement):
    def create_manager(self) -> RefManager:
        return RefManager()

# Manager
# Description :Abstract class สำหรับกำหนดการทำงานของ object การจัดการข้อมูลต้นแบบของวัตถุและวัตถุอ้างอิง
# Author : Athiruj Poositaporn
class Manager(ABC):
    @abstractmethod
    def get_all_model(self):
        pass

    @abstractmethod
    def get_model_by_id(self , data = Model()):
        pass

    @abstractmethod
    def add_model(self , data = Model()):
        pass

    @abstractmethod
    def edit_model(self , data = Model()):
        pass

    @abstractmethod
    def change_active_model(self , data = Model()):
        pass

    @abstractmethod
    def delete_model(self , data = Model()):
        pass

# MLManager
# Description :คลาสของ object การจัดการข้อมูลต้นแบบของวัตถุ
# Author : Athiruj Poositaporn
class MLManager(Manager):
    def __init__(self): 
        self.logger = logging.getLogger("MLManager_obj")
        URI = "mongodb://"+db_config.item["db_username"]+":" + \
        db_config.item["db_password"]+"@"+db_config.item["db_host"]
        self.logger.info("Connecting to database")
        self.db_connect = MongoClient(URI)
        self.logger.info("Connected to database")
        self.DPML_db = self.db_connect[db_config.item["db_name"]]
        self.collection = db_config.item["db_col_mlmo"]

        parent = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) 
        self.storage_path = os.path.join(parent, db_config.item["db_file_path"], db_config.item["ml_path"])
        self.name_regex = "^([\wก-๙]+ )+[\wก-๙]+$|^[\wก-๙]+$"

    def is_int(self,number):
        try:
            temp = int(number)
            if(temp <= 0):
                return False
            return True
        except:
            return False

    def is_duplicate_name(self,data):
        if(self.is_int(data.id)):
            query_result = self.DPML_db[self.collection].find_one({
                db_config.item['fld_mlmo_name']: data.name,
                db_config.item['fld_mlmo_status']: {
                    "$ne": 0
                },
                db_config.item['fld_mlmo_id']: {
                    "$ne": int(data.id)
                },
            })
        else:
            query_result = self.DPML_db[self.collection].find_one({
                db_config.item['fld_mlmo_name']: data.name,
                db_config.item['fld_mlmo_status']: {
                    "$ne": 0
                }
            })
        # self.logger.debug("query_result : {}".format(query_result))
        
        if(query_result):
            return True
        else:
            return False

    def get_all_model(self,username):
        try:
            self.logger.info("[{}] Getting all ML models.".format(username))
            query_result = self.DPML_db[self.collection].find(
                {
                    db_config.item['fld_mlmo_status']: {"$ne": 0}
                },
                {
                    db_config.item['fld_mlmo_id']: 1,
                    db_config.item['fld_mlmo_name']: 1,
                    db_config.item['fld_mlmo_status']: 1
                }
            ).sort(
                [
                    (db_config.item['fld_mlmo_status'], 1),
                    (db_config.item['fld_mlmo_id'], -1)
                ]
            )
            
            arr = []
            for item in query_result:
                item.pop('_id')
                arr.append(item)

            self.logger.info("[{}] Got all ML models.".format(username))
            result = {
                'data':arr,
                'status':'success',
            }
            return result
        except Exception as identifier:
            result = { 'mes' : str(identifier) , 'status' : "system_error"}
            return result

    def get_model_by_id(self , data = Model()):
        try:
            self.logger.info("[{}] Prepair ML model id to be query.".format(data.username))
            if(self.is_int(data.id)):
                data.id = int(data.id)
                query_model = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_mlmo_id']: data.id
                })
            else: 
                self.logger.warning("[{}] Wrong model id. This ID dose not match any unit id on dpml_ml_model".format(data.username))
                raise TypeError("wrong_mlmo_id")

            self.logger.info("[{}] Got a ML model.".format(data.username))
            query_model.pop('_id')
            result = {
                'mes' : "ok",
                'result': query_model
            }
            return jsonify(result)
        except Exception as identifier:
            error = { 'mes' : str(identifier) }
            return jsonify(error)

    def add_model(self , data = Model()):
        try:
            self.logger.info("[{}] Prepair ML model data to be save.".format(data.username))
            if(not data.file):
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['ml_file_empty']))
                raise TypeError(err_msg.msg['ml_file_empty'])
            file_extension = data.file.filename.split('.')[-1]
            result_regex = re.search(self.name_regex, data.name)

            if(data.name):
                query_result = self.is_duplicate_name(data)
            else:
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_ml_name']))
                raise TypeError(err_msg.msg['wrong_ml_name'])

            if((not result_regex) or len(data.name) < 3 or len(data.name) > 30):
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_ml_name']))
                raise TypeError(err_msg.msg['wrong_ml_name'])
            elif(not re.search("weights",file_extension)):
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_extension']))
                raise TypeError(err_msg.msg['wrong_extension'])
            elif(query_result):
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['duplicate_name']))
                raise TypeError(err_msg.msg['duplicate_name'])
            else:
                gen_file_name = uuid.uuid4().hex + "." + data.file.filename.split('.')[-1]
                file_storage_path = os.path.join(self.storage_path,gen_file_name)
                self.logger.info("[{}] Saved a ML model file to storage.".format(data.username))
                data.file.save(file_storage_path)
                last_mlmo = self.DPML_db[self.collection].find_one(
                                sort=[(db_config.item["fld_mlmo_id"], -1)]
                            )
                if(last_mlmo):
                    last_id = last_mlmo[db_config.item["fld_mlmo_id"]] + 1
                else:
                    last_id = 1

                new_model = {
                    db_config.item["fld_mlmo_id"] : last_id,
                    db_config.item["fld_mlmo_name"] : data.name,
                    db_config.item["fld_mlmo_path"] : file_storage_path,
                    db_config.item["fld_mlmo_status"] : db_config.item["fld_mlmo_status_disable"]
                }
                self.DPML_db[self.collection].insert_one(new_model)
                self.logger.info("[{}] Added a ML model details to database.".format(data.username))
                result = { 'mes' : "added_model", 'status' : "success"}
                return result

        except Exception as identifier:
            try:
                list(err_msg.msg.keys())[list(err_msg.msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                self.logger.warning("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    def edit_model(self , data = Model()):
        try:
            self.logger.info("[{}] Prepair ML model data to be edit.".format(data.username))
            if (self.is_int(data.id)): 
                data.id = int(data.id)
                query_model = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_mlmo_id']: data.id
                })
                if(not query_model):
                    self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_mlmo_id']))
                    raise TypeError(err_msg.msg['wrong_mlmo_id'])
            else: 
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_mlmo_id']))
                raise TypeError(err_msg.msg['wrong_mlmo_id'])
            
            query_name = None
            if(data.name):
                query_name = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_mlmo_name']: data.name,
                    db_config.item['fld_mlmo_id']:{ "$ne": data.id },
                    db_config.item['fld_mlmo_status']: { "$ne": 0 }
                })

                result_regex = re.search(self.name_regex, data.name)
                if((not result_regex) or len(data.name) < 3 or len(data.name) > 30):
                    self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_ml_name']))
                    raise TypeError(err_msg.msg['wrong_ml_name'])
                elif(query_name):
                    self.logger.warning("[{}] {}".format(data.username,err_msg.msg['duplicate_name']))
                    raise TypeError(err_msg.msg['duplicate_name'])

                self.DPML_db[self.collection].update(
                    { db_config.item['fld_mlmo_id']:data.id },
                    { "$set":{ db_config.item['fld_mlmo_name']:data.name }}
                )
            # else:
            #     self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_ml_name']))
            #     raise TypeError(err_msg.msg['wrong_ml_name'])
            
            file_extension = None
            if(data.file):
                file_extension = data.file.filename.split('.')[-1]
                if(not re.search("weights",file_extension)):
                    self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_extension']))
                    raise TypeError(err_msg.msg['wrong_extension'])

                gen_file_name = uuid.uuid4().hex + "." + data.file.filename.split('.')[-1]
                file_storage_path = os.path.join(self.storage_path,gen_file_name)
                data.file.save(file_storage_path)
                self.DPML_db[self.collection].update(
                    { db_config.item['fld_mlmo_id']:data.id },
                    { "$set":{ db_config.item['fld_mlmo_path']:file_storage_path }}
                )


            self.logger.info("[{}] Edited a ML model details.".format(data.username))
            result = { 'mes' : "edited_model" , 'status' : 'success'}       
            return result
        except Exception as identifier:
            try:
                list(err_msg.msg.keys())[list(err_msg.msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                self.logger.warning("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    def change_active_model(self , data = Model()):
        try:
            self.logger.info("[{}] Prepair ML model data to be activate.".format(data.username))
            if(self.is_int(data.id)):
                data.id = int(data.id)
                query_model = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_mlmo_id']: data.id
                })
            else: 
                self.logger.warning("[{}] Wrong model id. This ID dose not match any unit id on dpml_ml_model".format(data.username))
                raise TypeError("wrong_mlmo_id")

            query = {db_config.item['fld_mlmo_id']: data.id}
            query_result = self.DPML_db[self.collection].find_one(query)

            if(not query_result):
                self.logger.warning("[{}] Wrong model id. This ID dose not match any unit id on dpml_ml_model".format(data.username))
                raise TypeError("wrong_mlmo_id")
            else:
                # ปิดการใช้งาน model ที่เปิดอยู่
                query = {db_config.item['fld_mlmo_status'] : db_config.item['fld_mlmo_status_active']}
                new_value = {"$set": {db_config.item['fld_mlmo_status'] : db_config.item['fld_mlmo_status_disable']}}
                self.DPML_db[self.collection].update(query,new_value)
                self.logger.info("[{}] Disable an active model.".format(data.username))

                # เปิดการใช้งาน model ที่ต้องการตาม id
                query = {db_config.item['fld_mlmo_id'] : data.id}
                new_value = {"$set": {db_config.item['fld_mlmo_status'] : db_config.item['fld_mlmo_status_active']}}
                query_result = self.DPML_db[self.collection].update(query,new_value)
                self.logger.info("[{}] Activate a selected model.".format(data.username))

                result = { 'mes' : "changed_active_model" , 'status' : 'success'}  
            return result
        except Exception as identifier:
            try:
                list(err_msg.msg.keys())[list(err_msg.msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                self.logger.warning("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    def delete_model(self , data = Model()):
        try:
            self.logger.info("[{}] Prepair ML model data to be delete.".format(data.username))
            if(self.is_int(data.id)):
                data.id = int(data.id)
                query_model = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_mlmo_id']: data.id,
                    db_config.item['fld_mlmo_status']: {"$ne": db_config.item['fld_mlmo_status_active']}
                })
            else: 
                self.logger.warning("[{}] Wrong model id. This ID dose not match any unit id on dpml_ml_model".format(data.username))
                raise TypeError("wrong_mlmo_id")

            if(not query_model):
                self.logger.warning("[{}] Wrong model id. This ID dose not match any unit id on dpml_ml_model".format(data.username))
                raise TypeError("wrong_mlmo_id")
            else:
                query_result = self.DPML_db[self.collection].update(
                    {
                        db_config.item['fld_mlmo_id']:data.id
                    },
                    {   
                        "$set":{
                            db_config.item['fld_mlmo_status']:db_config.item['fld_mlmo_status_delete']
                        }
                    }
                )
                self.logger.info("[{}] Deleted a selected model.".format(data.username))
                result = { 'mes' : "deleted_model"  , 'status' : 'success'}
                return result

        except Exception as identifier:
            try:
                list(err_msg.msg.keys())[list(err_msg.msg.values()).index(identifier)]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                self.logger.warning("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    def __del__(self): 
        self.db_connect.close()

# RefManager
# Description :คลาสของ object การจัดการข้อมูลต้นแบบของวัตถุอ้างอิง
# Author : Athiruj Poositaporn
class RefManager(Manager):
    def __init__(self): 
        self.logger = logging.getLogger("RefManager_obj")
        URI = "mongodb://"+db_config.item["db_username"]+":" + \
        db_config.item["db_password"]+"@"+db_config.item["db_host"]
        self.logger.info("Connecting to database")
        self.db_connect = MongoClient(URI)
        self.logger.info("Connected to database")
        self.DPML_db = self.db_connect[db_config.item["db_name"]]
        self.collection = db_config.item["db_col_remo"]
        self.unit_collection = db_config.item["db_col_unit"]

        parent = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) 
        self.storage_path = os.path.join(parent, db_config.item["db_file_path"], db_config.item["ref_path"])
        self.name_regex = "^([\wก-๙]+ )+[\wก-๙]+$|^[\wก-๙]+$"

    def is_duplicate_name(self,data):
        if(self.is_int(data.id)):
            query_result = self.DPML_db[self.collection].find_one({
                db_config.item['fld_remo_name']: data.name,
                db_config.item['fld_remo_status']: {
                    "$ne": 0
                },
                db_config.item['fld_remo_id']: {
                    "$ne": int(data.id)
                },
            })
        else:
            query_result = self.DPML_db[self.collection].find_one({
                db_config.item['fld_remo_name']: data.name,
                db_config.item['fld_remo_status']: {
                    "$ne": 0
                }
            })
        
        if(query_result):
            return True
        else:
            return False

    def is_float(self,number):
        try:
            if(re.search("\s",number)):
                return False            
            temp = float(number)  
            if(temp <= 0):
                return False
            return True
        except:
            return False

    def is_int(self,number):
        try:
            temp = int(number)
            if(temp <= 0):
                return False
            return True
        except:
            return False

    def get_all_model(self,username):
        try:
            self.logger.info("[{}] Getting all Ref models.".format(username))
            query_result = self.DPML_db[self.collection].find(
                {
                    db_config.item["fld_remo_status"]: {"$ne": 0}
                },
                {
                    db_config.item["fld_remo_id"]: 1,
                    db_config.item["fld_remo_name"]: 1,
                    db_config.item["fld_remo_width"]: 1,
                    db_config.item["fld_remo_height"]: 1,
                    db_config.item["fld_remo_status"]: 1,
                    db_config.item["fld_remo_unit"]: 1
                }
            ).sort(
                [
                    (db_config.item["fld_remo_status"], 1),
                    (db_config.item["fld_remo_id"], -1)
                ]
            )
            
            arr = []
            for item in query_result:
                item.pop('_id')
                query_result = self.DPML_db[self.unit_collection].find_one(
                    {
                        db_config.item['fld_un_id']: item['remo_un_id']
                    },
                    {
                        db_config.item['fld_un_name']: 1,
                        db_config.item['fld_un_abb_name']: 1,
                    }
                )
                query_result.pop('_id')
                item['un_name'] = query_result['un_name']
                item['un_abb_name'] = query_result['un_abb_name']
                arr.append(item)

            self.logger.info("[{}] Got all Ref models.".format(username))
            result = {
                'data':arr,
                'status':'success',
            }
            return result
        except Exception as identifier:
            result = {'mes' : str(identifier) , 'status' : "system_error"}
            return result

    def get_all_unit(self,username):
        try:
            self.logger.info("[{}] Getting all units.".format(username))
            query_result = self.DPML_db[self.unit_collection].find(
                {},
                {
                    db_config.item["fld_un_id"]: 1,
                    db_config.item["fld_un_name"]: 1,
                    db_config.item["fld_un_abb_name"]: 1,
                }
            )
            
            arr = []
            for item in query_result:
                item.pop('_id')
                arr.append(item)

            self.logger.info("[{}] Got all units.".format(username))
            result = {
                'data':arr,
                'status':'success',
            }
            return result
        except Exception as identifier:
            result = {'mes' : str(identifier) , 'status' : "system_error"}
            return result

    def get_model_by_id(self , data = Model()):
        try:
            self.logger.info("[{}] Prepair Ref model id to be query.".format(data.username))
            if(self.is_int(data.id)):
                data.id = int(data.id)
                query_model = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_remo_id']: data.id
                })
            else: 
                self.logger.warning("[{}] Wrong model id. This ID dose not match any unit id on dpml_ref_model".format(data.username))
                raise TypeError("wrong_remo_id")
            
            self.logger.info("[{}] Got a Ref model.".format(data.username))
            query_model.pop('_id')
            result = {
                'mes' : "ok",
                'result': query_model
            }
            return jsonify(result)
        except Exception as identifier:
            error = { 'mes' : str(identifier) }
            return jsonify(error)

    def add_model(self , data = Model()):
        try:
            self.logger.info("[{}] Prepair Ref model data to be save.".format(data.username))
            if(not data.file):
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['ref_file_empty']))
                raise TypeError(err_msg.msg['ref_file_empty'])
            file_extension = data.file.filename.split('.')[-1]
            result_regex = re.search(self.name_regex, data.name)

            query_result = None
            if(data.name):
                query_result = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_remo_name']: data.name,
                    db_config.item['fld_remo_status']: {
                        "$not": { "$in": [0] }
                    }
                })
            else:
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_ref_name']))
                raise TypeError(err_msg.msg['wrong_ref_name'])

            query_unit = None
            if(self.is_int(data.un_id)):
                query_unit = self.DPML_db[db_config.item['db_col_unit']].find_one({
                    db_config.item['fld_un_id']: int(data.un_id)
                })
            else:
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_unit_id']))
                raise TypeError(err_msg.msg['wrong_unit_id'])

            if((not result_regex) or len(data.name) < 3 or len(data.name) > 30):
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_ref_name']))
                raise TypeError(err_msg.msg['wrong_ref_name'])
            elif(not self.is_float(data.width) ):
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_width']))
                raise TypeError(err_msg.msg['wrong_width'])
            elif(not self.is_float(data.height) ):
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_height']))
                raise TypeError(err_msg.msg['wrong_height'])
            elif(not re.search("weights",file_extension)):
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_extension']))
                raise TypeError(err_msg.msg['wrong_extension'])
            elif(query_result):
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['duplicate_name']))
                raise TypeError(err_msg.msg['duplicate_name'])
            elif(not query_unit):
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_unit_id']))
                raise TypeError(err_msg.msg['wrong_unit_id'])
            else:
                gen_file_name = uuid.uuid4().hex + "." + data.file.filename.split('.')[-1]
                file_storage_path = os.path.join(self.storage_path,gen_file_name)
                self.logger.info("[{}] Saved a Ref model file to storage.".format(data.username))
                data.file.save(file_storage_path)
                
                last_remo = self.DPML_db[self.collection].find_one(
                                sort=[(db_config.item["fld_remo_id"], -1)]
                            )
                if(last_remo):
                    last_id = last_remo[db_config.item["fld_remo_id"]] + 1
                else:
                    last_id = 1

                new_model = {
                    db_config.item["fld_remo_id"] : last_id,
                    db_config.item["fld_remo_name"] : data.name,
                    db_config.item["fld_remo_width"] : float(data.width),
                    db_config.item["fld_remo_height"] : float(data.height),
                    db_config.item["fld_remo_path"] : file_storage_path,
                    db_config.item["fld_remo_status"] : db_config.item["fld_remo_status_disable"],
                    db_config.item["fld_remo_unit"] : int(data.un_id)
                }
                self.DPML_db[self.collection].insert_one(new_model)
                self.logger.info("[{}] Added a Ref model details to database.".format(data.username))
                result = { 'mes' : "added_model", 'status' : "success"}
                return result
        except Exception as identifier:
            try:
                list(err_msg.msg.keys())[list(err_msg.msg.values()).index(str(identifier))]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                self.logger.warning("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    #ตอนเรียกใช้ต้องส่งค่าทุกอย่างกลับมา แต่เว้น file ได้ ถ้าไม่ได้อัปอันใหม่มาให้ 
    def edit_model(self , data = Model()):
        try:
            self.logger.info("[{}] Prepair Ref model data to be edit.".format(data.username))
            # Set ref model id validation
            if (self.is_int(data.id)): 
                data.id = int(data.id)
                query_model = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_remo_id']: data.id
                })
                if(not query_model):
                    self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_mlmo_id']))
                    raise TypeError(err_msg.msg['wrong_remo_id'])
            else: 
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_remo_id']))
                raise TypeError(err_msg.msg['wrong_remo_id'])
            # Set ref model id validation
            
            # Set ref model name
            query_name = None
            if(data.name):
                query_name = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_remo_name']: data.name,
                    db_config.item['fld_remo_id']:{ "$ne": data.id },
                    db_config.item['fld_remo_status']: { "$ne": 0 }
                })
                result_regex = re.search(self.name_regex, data.name)
                if((not result_regex) or len(data.name) < 3 or len(data.name) > 30):
                    self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_ref_name']))
                    raise TypeError(err_msg.msg['wrong_ref_name'])
                elif(query_name):
                    self.logger.warning("[{}] {}".format(data.username,err_msg.msg['duplicate_name']))
                    raise TypeError(err_msg.msg['duplicate_name'])
                self.DPML_db[self.collection].update(
                    { db_config.item['fld_remo_id']:data.id },
                    { "$set":{db_config.item['fld_remo_name']:data.name}}
                )
            # Set ref model name

            # Set ref model measurement unit
            query_unit = None
            if(self.is_int(data.un_id)):
                data.un_id = int(data.un_id)
                query_unit = self.DPML_db[db_config.item['db_col_unit']].find_one({
                    db_config.item['fld_un_id']: data.un_id
                })
                if(not query_unit):
                    self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_unit_id']))
                    raise TypeError(err_msg.msg['wrong_unit_id'])
                self.DPML_db[self.collection].update(
                    { db_config.item['fld_remo_id']:data.id },
                    { "$set":{db_config.item['fld_remo_unit']:data.un_id}}
                )
            # Set ref model measurement unit
            
            # Set width of ref model
            if(data.width):
                if(not self.is_float(data.width) ):
                    self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_width']))
                    raise TypeError(err_msg.msg['wrong_width'])
                self.DPML_db[self.collection].update(
                    { db_config.item['fld_remo_id']:data.id },
                    { "$set":{ db_config.item['fld_remo_width']:data.width }}
                )
            # Set width of ref model

            # Set height of ref model
            if(data.height):
                if(not self.is_float(data.height) ):
                    self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_height']))
                    raise TypeError(err_msg.msg['wrong_height'])
                self.DPML_db[self.collection].update(
                    { db_config.item['fld_remo_id']:data.id },
                    { "$set":{ db_config.item['fld_remo_height']:data.height }}
                )
            # Set height of ref model

            # Set ref model file
            file_extension = None
            if(data.file):
                file_extension = data.file.filename.split('.')[-1]
                if(not re.search("weights",file_extension)):
                    self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_extension']))
                    raise TypeError(err_msg.msg['wrong_extension'])

                gen_file_name = uuid.uuid4().hex + "." + data.file.filename.split('.')[-1]
                file_storage_path = os.path.join(self.storage_path,gen_file_name)
                data.file.save(file_storage_path)
                self.logger.info("[{}] Saved a Ref model file to storage.".format(data.username))
                self.DPML_db[self.collection].update(
                    { db_config.item['fld_remo_id']:data.id },
                    { "$set":{ db_config.item['fld_remo_path']:file_storage_path }}
                )
            # Set ref model file

            self.logger.info("[{}] Edited a Ref model details to database.".format(data.username))
            result = { 'mes' : "edited_model" , 'status' : 'success'}       
            return result
        except Exception as identifier:
            try:
                list(err_msg.msg.keys())[list(err_msg.msg.values()).index(str(identifier))]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                self.logger.warning("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    def change_active_model(self , data = Model()):
        try:
            self.logger.info("[{}] Prepair Ref model data to be activate.".format(data.username))
            if(self.is_int(data.id)):
                data.id = int(data.id)
                query_model = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_remo_id']: data.id
                })
            else: 
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_remo_id']))
                raise TypeError(err_msg.msg['wrong_remo_id'])

            query = {db_config.item['fld_remo_id']: data.id}
            query_result = self.DPML_db[self.collection].find_one(query)

            if(not query_result):
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_remo_id']))
                raise TypeError(err_msg.msg['wrong_remo_id'])
            else:
                query = {db_config.item['fld_remo_status'] : db_config.item['fld_remo_status_active']}
                new_value = {"$set": {db_config.item['fld_remo_status'] : db_config.item['fld_remo_status_disable']}}
                self.DPML_db[self.collection].update(query,new_value)
                self.logger.info("[{}] Disable an active model.".format(data.username))

                # เปิดการใช้งาน model ที่ต้องการตาม id
                query = {db_config.item['fld_remo_id'] : data.id}
                new_value = {"$set": {db_config.item['fld_remo_status'] : db_config.item['fld_remo_status_active']}}
                query_result = self.DPML_db[self.collection].update(query,new_value)
                self.logger.info("[{}] Activate a selected model.".format(data.username))

                result = { 'mes' : "changed_active_model" , 'status' : 'success'}  
            return result
        except Exception as identifier:
            try:
                list(err_msg.msg.keys())[list(err_msg.msg.values()).index(str(identifier))]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                self.logger.warning("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    def delete_model(self , data = Model()):
        try:
            self.logger.info("[{}] Prepair Ref model data to be delete.".format(data.username))
            if(self.is_int(data.id)):
                data.id = int(data.id)
                query_model = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_remo_id']: data.id,
                    db_config.item['fld_remo_status']: {"$ne": db_config.item['fld_remo_status_active']}
                })
            else: 
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_remo_id']))
                raise TypeError(err_msg.msg['wrong_remo_id'])

            if(not query_model):
                self.logger.warning("[{}] {}".format(data.username,err_msg.msg['wrong_remo_id']))
                raise TypeError(err_msg.msg['wrong_remo_id'])
            else:
                query_result = self.DPML_db[self.collection].update(
                    {
                        db_config.item['fld_remo_id']:data.id
                    },
                    {   
                        "$set":{
                            db_config.item['fld_remo_status']:db_config.item['fld_remo_status_delete']
                        }
                    }
                )
                self.logger.info("[{}] Deleted a selected model.".format(data.username))
                result = { 'mes' : "deleted_model" , 'status' : 'success'}
                return result

        except Exception as identifier:
            try:
                list(err_msg.msg.keys())[list(err_msg.msg.values()).index(str(identifier))]
                result = {'mes' : str(identifier), 'status' : "error"}
            except:
                self.logger.warning("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
            return result

    def __del__(self): 
        self.db_connect.close()