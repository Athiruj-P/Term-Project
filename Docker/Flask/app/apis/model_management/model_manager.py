# model_management
# Description : คลาสของการจัดการข้อมูลต้นแบบของวัตถุและวัตถุอ้างอิง
# โดยใช้ Design pattern "Factory Method"
# Author : Athiruj Poositaporn
from __future__ import annotations
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
        URI = "mongodb://"+db_config.item["db_username"]+":" + \
        db_config.item["db_password"]+"@"+db_config.item["db_host"]
        self.db_connect = MongoClient(URI)
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

            return jsonify(arr)
        except Exception as identifier:
            error = {
                'mes' : str(identifier)
            }
            return jsonify(error)

    def get_model_by_id(self , data = Model()):
        query_result = self.DPML_db[self.collection].find_one({
            db_config.item['fld_mlmo_id']: data.id
        })
        query_result.pop('_id')
        return jsonify(query_result)

    def add_model(self , data = Model()):
        try:
            file_extension = data.file.filename.split('.')[-1]
            result_regex = re.search(self.name_regex, data.name)
            query_result = self.DPML_db[self.collection].find_one({
                db_config.item['fld_mlmo_name']: data.name,
                db_config.item['fld_mlmo_status']: {
                    "$not": { "$in": [0] }
                }
            })

            if((not result_regex) or len(data.name) < 5 or len(data.name) > 30):
                raise TypeError("wrong_name")
            elif(not re.search("weights",file_extension)):
                raise TypeError("wrong_extension")
            elif(query_result):
                raise TypeError("duplicate_name")
            else:
                gen_file_name = uuid.uuid4().hex + "." + data.file.filename.split('.')[-1]
                file_storage_path = os.path.join(self.storage_path,gen_file_name)
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
                result = { 'mes' : "added_model"}
                return jsonify(result)

        except Exception as identifier:
            error = { 'mes' : str(identifier) }
            return jsonify(error)

    def edit_model(self , data = Model()):
        try:
            if (self.is_int(data.id)): 
                data.id = int(data.id)
                query_model = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_mlmo_id']: data.id
                })
            else: 
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
                raise TypeError("wrong_name")
            
            file_extension = None
            if((not result_regex) or len(data.name) < 5 or len(data.name) > 30):
                raise TypeError("wrong_name")
            elif(query_name):
                raise TypeError("duplicate_name")
            elif(not query_model):
                raise TypeError("wrong_mlmo_id")
            elif(data.file):
                file_extension = data.file.filename.split('.')[-1]
                if(not re.search("weights",file_extension)):
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

            result = { 'mes' : "edited_model"}       
            return jsonify(result)
        except Exception as identifier:
            error = { 'mes' : str(identifier) }
            return jsonify(error)

    def change_active_model(self , data = Model()):
        try:
            if(self.is_int(data.id)):
                data.id = int(data.id)
                query_model = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_mlmo_id']: data.id
                })
            else: 
                raise TypeError("wrong_mlmo_id")

            query = {db_config.item['fld_mlmo_id']: data.id}
            query_result = self.DPML_db[self.collection].find_one(query)

            if(not query_result):
                raise TypeError("wrong_mlmo_id")
            else:
                query = {db_config.item['fld_mlmo_status'] : db_config.item['fld_mlmo_status_active']}
                new_value = {"$set": {db_config.item['fld_mlmo_status'] : db_config.item['fld_mlmo_status_disable']}}
                self.DPML_db[self.collection].update(query,new_value)

                # เปิดการใช้งาน model ที่ต้องการตาม id
                query = {db_config.item['fld_mlmo_id'] : data.id}
                new_value = {"$set": {db_config.item['fld_mlmo_status'] : db_config.item['fld_mlmo_status_active']}}
                query_result = self.DPML_db[self.collection].update(query,new_value)

                result = { 'mes' : query_result }  
            return jsonify(result)
        except Exception as identifier:
            error = { 'mes' : str(identifier) }
            return jsonify(error)

    def delete_model(self , data = Model()):
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
        result = {
            'mes' : query_result
        }
        return jsonify(result)

    def __del__(self): 
        self.db_connect.close()

# RefManager
# Description :คลาสของ object การจัดการข้อมูลต้นแบบของวัตถุอ้างอิง
# Author : Athiruj Poositaporn
class RefManager(Manager):
    def __init__(self): 
        URI = "mongodb://"+db_config.item["db_username"]+":" + \
        db_config.item["db_password"]+"@"+db_config.item["db_host"]
        self.db_connect = MongoClient(URI)
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

            return jsonify(arr)
        except Exception as identifier:
            error = {
                'mes' : str(identifier)
            }
            return jsonify(error)

    def get_model_by_id(self , data = Model()):
        query_result = self.DPML_db[self.collection].find_one({
            db_config.item["fld_remo_id"]: data.id
        })
        query_result.pop('_id')
        return jsonify(query_result)

    def add_model(self , data = Model()):
        try:
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
                raise TypeError("wrong_name")

            query_unit = None
            if(self.is_int(data.un_id)):
                query_unit = self.DPML_db[db_config.item['db_col_unit']].find_one({
                    db_config.item['fld_un_id']: int(data.un_id)
                })
            else:
                raise TypeError("wrong_unit_id")

            if((not result_regex) or len(data.name) < 5 or len(data.name) > 30):
                raise TypeError("wrong_name")
            elif(not self.is_float(data.width) ):
                raise TypeError("wrong_width")
            elif(not self.is_float(data.height) ):
                raise TypeError("wrong_height")
            elif(not re.search("weights",file_extension)):
                raise TypeError("wrong_extension")
            elif(query_result):
                raise TypeError("duplicate_name")
            elif(not query_unit):
                raise TypeError("wrong_unit_id")
            else:
                gen_file_name = uuid.uuid4().hex + "." + data.file.filename.split('.')[-1]
                file_storage_path = os.path.join(self.storage_path,gen_file_name)
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
                result = { 'mes' : "added_model"}
                return jsonify(result)
        except Exception as identifier:
            error = { 'mes' : str(identifier) }
            return jsonify(error)

    #ตอนเรียกใช้ต้องส่งค่าทุกอย่างกลับมา แต่เว้น file ได้ ถ้าไม่ได้อัปอันใหม่มาให้ 
    def edit_model(self , data = Model()):
        try:
            if (self.is_int(data.id)): 
                data.id = int(data.id)
                query_model = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_remo_id']: data.id
                })
            else: 
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
                raise TypeError("wrong_name")

            query_unit = None
            if(self.is_int(data.un_id)):
                data.un_id = int(data.un_id)
                query_unit = self.DPML_db[db_config.item['db_col_unit']].find_one({
                    db_config.item['fld_un_id']: data.un_id
                })
            else:
                raise TypeError("wrong_unit_id")
            
            file_extension = None
            if((not result_regex) or len(data.name) < 5 or len(data.name) > 30):
                raise TypeError("wrong_name")
            elif(not self.is_float(data.width) ):
                raise TypeError("wrong_width")
            elif(not self.is_float(data.height) ):
                raise TypeError("wrong_height")
            elif(query_name):
                raise TypeError("duplicate_name")
            elif(not query_unit):
                raise TypeError("wrong_unit_id")
            elif(data.file):
                file_extension = data.file.filename.split('.')[-1]
                if(not re.search("weights",file_extension)):
                    raise TypeError("wrong_extension")

            if(data.file):
                gen_file_name = uuid.uuid4().hex + "." + data.file.filename.split('.')[-1]
                file_storage_path = os.path.join(self.storage_path,gen_file_name)
                data.file.save(file_storage_path)
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

            result = { 'mes' : "edited_model"}       
            return jsonify(result)
        except Exception as identifier:
            error = { 'mes' : str(identifier) }
            return jsonify(error)

    def change_active_model(self , data = Model()):
        try:
            if(self.is_int(data.id)):
                data.id = int(data.id)
                query_model = self.DPML_db[self.collection].find_one({
                    db_config.item['fld_remo_id']: data.id
                })
            else: 
                raise TypeError("wrong_remo_id")

            query = {db_config.item['fld_remo_id']: data.id}
            query_result = self.DPML_db[self.collection].find_one(query)

            if(not query_result):
                raise TypeError("wrong_remo_id")
            else:
                query = {db_config.item['fld_remo_status'] : db_config.item['fld_remo_status_active']}
                new_value = {"$set": {db_config.item['fld_remo_status'] : db_config.item['fld_remo_status_disable']}}
                self.DPML_db[self.collection].update(query,new_value)

                # เปิดการใช้งาน model ที่ต้องการตาม id
                query = {db_config.item['fld_remo_id'] : data.id}
                new_value = {"$set": {db_config.item['fld_remo_status'] : db_config.item['fld_remo_status_active']}}
                query_result = self.DPML_db[self.collection].update(query,new_value)

                result = { 'mes' : query_result }  
            return jsonify(result)
        except Exception as identifier:
            error = { 'mes' : str(identifier) }
            return jsonify(error)

    def delete_model(self , data = Model()):
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
        result = {
            'mes' : query_result
        }
        return jsonify(result)

    def __del__(self): 
        self.db_connect.close()