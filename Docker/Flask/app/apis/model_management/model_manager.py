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

    def get_all_model(self):
        try:
            self.logger.info("[{}] Getting all ML models.".format(data.username))
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
                    (db_config.item['fld_mlmo_id'], 1)
                ]
            )
            
            arr = []
            for item in query_result:
                item.pop('_id')
                arr.append(item)

            self.logger.info("[{}] Got all ML models.".format(data.username))
            return jsonify(arr)
        except Exception as identifier:
            error = { 'mes' : str(identifier) }
            return jsonify(error)

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
                self.logger.warning("[{}] File is empty.".format(data.username))
                raise TypeError("file_empty")
            file_extension = data.file.filename.split('.')[-1]
            result_regex = re.search(self.name_regex, data.name)
            query_result = self.DPML_db[self.collection].find_one({
                db_config.item['fld_mlmo_name']: data.name,
                db_config.item['fld_mlmo_status']: {
                    "$not": { "$in": [0] }
                }
            })

            if((not result_regex) or len(data.name) < 3 or len(data.name) > 30):
                self.logger.warning("[{}] Wrong ML name. The ML name must have minimum 5 characters or maximum 30 characters and written in English or Thai".format(data.username))
                raise TypeError("wrong_name")
            elif(not re.search("weights",file_extension)):
                self.logger.warning("[{}] Wrong file extension. The model file must be *.weights".format(data.username))
                raise TypeError("wrong_extension")
            elif(query_result):
                self.logger.warning("[{}] Duplicate ML name. Please re-enter ML name.".format(data.username))
                raise TypeError("duplicate_name")
            else:
                gen_file_name = uuid.uuid4().hex + "." + data.file.filename.split('.')[-1]
                file_storage_path = os.path.join(self.storage_path,gen_file_name)
                self.logger.info("[{}] Saved a ML model file to storage.".format(data.username))
                data.file.save(file_storage_path)
                last_mlmo = self.DPML_db[self.collection].find_one(
                                sort=[(db_config.item["fld_mlmo_id"], -1)]
                            )
                last_id = last_mlmo[db_config.item["fld_mlmo_id"]] + 1

                new_model = {
                    db_config.item["fld_mlmo_id"] : last_id,
                    db_config.item["fld_mlmo_name"] : data.name,
                    db_config.item["fld_mlmo_path"] : file_storage_path,
                    db_config.item["fld_mlmo_status"] : db_config.item["fld_mlmo_status_disable"]
                }
                self.DPML_db[self.collection].insert_one(new_model)
                self.logger.info("[{}] Added a ML model details to database.".format(data.username))
                result = { 'mes' : "added_model"}
                return jsonify(result)

        except Exception as identifier:
            # self.logger.error("[{}] Error {}".format(data.username,identifier))
            error = { 'mes' : str(identifier) }
            return jsonify(error)

    def edit_model(self , data = Model()):
        try:
            self.logger.info("[{}] Prepair ML model data to be edit.".format(data.username))
            if (self.is_int(data.id)): 
                data.id = int(data.id)
                query_model = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_mlmo_id']: data.id
                })
            else: 
                self.logger.warning("[{}] Wrong model id. This ID dose not match any unit id on dpml_ml_model".format(data.username))
                raise TypeError("wrong_mlmo_id")
            
            query_name = None
            if(data.name):
                query_name = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_mlmo_name']: data.name,
                    db_config.item['fld_mlmo_id']:{ "$ne": data.id },
                    db_config.item['fld_mlmo_status']: { "$ne": 0 }
                })
                result_regex = re.search(self.name_regex, data.name)
            else:
                self.logger.warning("[{}] Wrong ML name. The ML name must have minimum 5 characters or maximum 30 characters and written in English or Thai".format(data.username))
                raise TypeError("wrong_name")
            
            file_extension = None
            if((not result_regex) or len(data.name) < 3 or len(data.name) > 30):
                self.logger.warning("[{}] Wrong ML name. The ML name must have minimum 5 characters or maximum 30 characters and written in English or Thai".format(data.username))
                raise TypeError("wrong_name")
            elif(query_name):
                self.logger.warning("[{}] Duplicate ML name. Please re-enter ML name.".format(data.username))
                raise TypeError("duplicate_name")
            elif(not query_model):
                self.logger.warning("[{}] Wrong model id. This ID dose not match any unit id on dpml_ml_model".format(data.username))
                raise TypeError("wrong_mlmo_id")
            elif(data.file):
                file_extension = data.file.filename.split('.')[-1]
                if(not re.search("weights",file_extension)):
                    self.logger.warning("[{}] Wrong file extension. The model file must be *.weights".format(data.username))
                    raise TypeError("wrong_extension")

            if(data.file):
                gen_file_name = uuid.uuid4().hex + "." + data.file.filename.split('.')[-1]
                file_storage_path = os.path.join(self.storage_path,gen_file_name)
                data.file.save(file_storage_path)
                self.DPML_db[self.collection].update(
                    { db_config.item['fld_mlmo_id']:data.id },
                    { "$set":{ db_config.item['fld_mlmo_path']:file_storage_path }}
                )

            self.DPML_db[self.collection].update(
                { db_config.item['fld_mlmo_id']:data.id },
                { "$set":{ db_config.item['fld_mlmo_name']:data.name }}
            )

            self.logger.info("[{}] Edited a ML model details.".format(data.username))
            result = { 'mes' : "edited_model"}       
            return jsonify(result)
        except Exception as identifier:
            # self.logger.error("[{}] Error {}".format(data.username,identifier))
            error = { 'mes' : str(identifier) }
            return jsonify(error)

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

                result = { 'mes' : "changed_active_model" }  
            return jsonify(result)
        except Exception as identifier:
            error = { 'mes' : str(identifier) }
            return jsonify(error)

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
                result = { 'mes' : "deleted_model" }
                return jsonify(result)

        except Exception as identifier:
            error = { 'mes' : str(identifier) }
            return jsonify(error)

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

        parent = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) 
        self.storage_path = os.path.join(parent, db_config.item["db_file_path"], db_config.item["ref_path"])
        self.name_regex = "^([\wก-๙]+ )+[\wก-๙]+$|^[\wก-๙]+$"

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

    def get_all_model(self):
        try:
            self.logger.info("[{}] Getting all Ref models.".format(data.username))
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
                    (db_config.item["fld_remo_id"], 1)
                ]
            )
            
            arr = []
            for item in query_result:
                item.pop('_id')
                arr.append(item)

            self.logger.info("[{}] Got all Ref models.".format(data.username))
            return jsonify(arr)
        except Exception as identifier:
            error = {
                'mes' : str(identifier)
            }
            return jsonify(error)

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
                self.logger.warning("[{}] File is empty.".format(data.username))
                raise TypeError("file_empty")
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
                self.logger.warning("[{}] Wrong ML name. The Ref name must have minimum 5 characters or maximum 30 characters and written in English or Thai".format(data.username))
                raise TypeError("wrong_name")

            query_unit = None
            if(self.is_int(data.un_id)):
                query_unit = self.DPML_db[db_config.item['db_col_unit']].find_one({
                    db_config.item['fld_un_id']: int(data.un_id)
                })
            else:
                self.logger.warning("[{}] Wrong unit id. This ID dose not match any unit id on dpml_unit".format(data.username))
                raise TypeError("wrong_unit_id")

            if((not result_regex) or len(data.name) < 3 or len(data.name) > 30):
                self.logger.warning("[{}] Wrong Ref name. The Ref name must have minimum 5 characters or maximum 30 characters and written in English or Thai".format(data.username))
                raise TypeError("wrong_name")
            elif(not self.is_float(data.width) ):
                self.logger.warning("[{}] Wrong width. Width must be either int or float.".format(data.username))
                raise TypeError("wrong_width")
            elif(not self.is_float(data.height) ):
                self.logger.warning("[{}] Wrong height. Height must be either int or float.".format(data.username))
                raise TypeError("wrong_height")
            elif(not re.search("weights",file_extension)):
                self.logger.warning("[{}] Wrong file extension. The model file must be *.weights".format(data.username))
                raise TypeError("wrong_extension")
            elif(query_result):
                self.logger.warning("[{}] Duplicate Ref name. Please re-enter Ref name.".format(data.username))
                raise TypeError("duplicate_name")
            elif(not query_unit):
                self.logger.warning("[{}] Wrong unit id. This ID dose not match any unit id on dpml_unit".format(data.username))
                raise TypeError("wrong_unit_id")
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
                result = { 'mes' : "added_model"}
                return jsonify(result)
        except Exception as identifier:
            # self.logger.error("[{}] Error {}".format(data.username,identifier))
            error = { 'mes' : str(identifier) }
            return jsonify(error)

    #ตอนเรียกใช้ต้องส่งค่าทุกอย่างกลับมา แต่เว้น file ได้ ถ้าไม่ได้อัปอันใหม่มาให้ 
    def edit_model(self , data = Model()):
        try:
            self.logger.info("[{}] Prepair Ref model data to be edit.".format(data.username))
            if (self.is_int(data.id)): 
                data.id = int(data.id)
                query_model = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_remo_id']: data.id
                })
            else: 
                self.logger.warning("[{}] Wrong model id. This ID dose not match any unit id on dpml_ref_model".format(data.username))
                raise TypeError("wrong_mlmo_id")
            
            query_name = None
            if(data.name):
                query_name = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_remo_name']: data.name,
                    db_config.item['fld_remo_id']:{ "$ne": data.id },
                    db_config.item['fld_remo_status']: { "$ne": 0 }
                })
                result_regex = re.search(self.name_regex, data.name)
            else:
                self.logger.warning("[{}] Wrong Ref name. The Ref name must have minimum 5 characters or maximum 30 characters and written in English or Thai".format(data.username))
                raise TypeError("wrong_name")

            query_unit = None
            if(self.is_int(data.un_id)):
                data.un_id = int(data.un_id)
                query_unit = self.DPML_db[db_config.item['db_col_unit']].find_one({
                    db_config.item['fld_un_id']: data.un_id
                })
            else:
                self.logger.warning("[{}] Wrong unit id. This ID dose not match any unit id on dpml_unit".format(data.username))
                raise TypeError("wrong_unit_id")
            
            file_extension = None
            if((not result_regex) or len(data.name) < 3 or len(data.name) > 30):
                self.logger.warning("[{}] Wrong Ref name. The Ref name must have minimum 5 characters or maximum 30 characters and written in English or Thai".format(data.username))
                raise TypeError("wrong_name")
            elif(not self.is_float(data.width) ):
                self.logger.warning("[{}] Wrong width. Width must be either int or float.".format(data.username))
                raise TypeError("wrong_width")
            elif(not self.is_float(data.height) ):
                self.logger.warning("[{}] Wrong height. Height must be either int or float.".format(data.username))
                raise TypeError("wrong_height")
            elif(query_name):
                self.logger.warning("[{}] Duplicate Ref name. Please re-enter Ref name.".format(data.username))
                raise TypeError("duplicate_name")
            elif(not query_unit):
                self.logger.warning("[{}] Wrong unit id. This ID dose not match any unit id on dpml_unit".format(data.username))
                raise TypeError("wrong_unit_id")
            elif(data.file):
                file_extension = data.file.filename.split('.')[-1]
                if(not re.search("weights",file_extension)):
                    self.logger.warning("[{}] Wrong file extension. The model file must be *.weights".format(data.username))
                    raise TypeError("wrong_extension")

            if(data.file):
                gen_file_name = uuid.uuid4().hex + "." + data.file.filename.split('.')[-1]
                file_storage_path = os.path.join(self.storage_path,gen_file_name)
                data.file.save(file_storage_path)
                self.logger.info("[{}] Saved a Ref model file to storage.".format(data.username))
                self.DPML_db[self.collection].update(
                    { db_config.item['fld_remo_id']:data.id },
                    { "$set":{ db_config.item['fld_remo_path']:file_storage_path }}
                )

            self.DPML_db[self.collection].update(
                { db_config.item['fld_remo_id']:data.id },
                {   
                    "$set":{
                        db_config.item['fld_remo_name']:data.name,
                        db_config.item['fld_remo_width']:float(data.width),
                        db_config.item['fld_remo_height']:float(data.height),
                        db_config.item['fld_remo_unit']:data.un_id
                    }
                }
            )

            self.logger.info("[{}] Edited a Ref model details to database.".format(data.username))
            result = { 'mes' : "edited_model"}       
            return jsonify(result)
        except Exception as identifier:
            error = { 'mes' : str(identifier) }
            return jsonify(error)

    def change_active_model(self , data = Model()):
        try:
            self.logger.info("[{}] Prepair Ref model data to be activate.".format(data.username))
            if(self.is_int(data.id)):
                data.id = int(data.id)
                query_model = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_remo_id']: data.id
                })
            else: 
                self.logger.warning("[{}] Wrong model id. This ID dose not match any unit id on dpml_ref_model".format(data.username))
                raise TypeError("wrong_remo_id")

            query = {db_config.item['fld_remo_id']: data.id}
            query_result = self.DPML_db[self.collection].find_one(query)

            if(not query_result):
                self.logger.warning("[{}] Wrong model id. This ID dose not match any unit id on dpml_ref_model".format(data.username))
                raise TypeError("wrong_remo_id")
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

                result = { 'mes' : "changed_active_model" }  
            return jsonify(result)
        except Exception as identifier:
            error = { 'mes' : str(identifier) }
            return jsonify(error)

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
                self.logger.warning("[{}] Wrong model id. This ID dose not match any unit id on dpml_ref_model".format(data.username))
                raise TypeError("wrong_remo_id")

            if(not query_model):
                self.logger.warning("[{}] Wrong model id. This ID dose not match any unit id on dpml_ref_model".format(data.username))
                raise TypeError("wrong_remo_id")
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
                result = { 'mes' : "deleted_model" }
                return jsonify(result)

        except Exception as identifier:
            error = { 'mes' : str(identifier) }
            return jsonify(error)

    def __del__(self): 
        self.db_connect.close()