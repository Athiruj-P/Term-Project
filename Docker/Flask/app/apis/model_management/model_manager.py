from __future__ import annotations
from flask import jsonify
from abc import ABC, abstractmethod
from pymongo import MongoClient
import uuid 
import os
from .model import Model
from .. import db_config

class ModelManagement(ABC):
    @abstractmethod
    def create_manager(self):
        return ""

class MLManagement(ModelManagement):
    def create_manager(self) -> MLManager:
        return MLManager()


class RefManagement(ModelManagement):
    def create_manager(self) -> RefManager:
        return RefManager()


class Manager(ABC):
    @abstractmethod
    def add_model(self , data = Model()):
        pass

    @abstractmethod
    def edit_model(self , data = Model()):
        pass

    @abstractmethod
    def delete_model(self , data = Model()):
        pass

class MLManager(Manager):
    def __init__(self): 
        URI = "mongodb://"+db_config.item["db_username"]+":" + \
        db_config.item["db_password"]+"@"+db_config.item["db_host"]
        self.db_connect = MongoClient(URI)
        self.DPML_db = self.db_connect[db_config.item["db_name"]]
        self.collection = db_config.item["db_col_mlmo"]

        parent = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) 
        self.storage_path = os.path.join(parent, db_config.item["db_file_path"], db_config.item["ml_path"])

    def add_model(self , data = Model()):
        try:
            gen_file_name = uuid.uuid4().hex + "." + data.file.filename.split('.')[-1]
            file_storage_path = os.path.join(self.storage_path,gen_file_name)
            data.file.save(file_storage_path)
            
            query_result = self.DPML_db[self.collection].find_one({
                    "mlmo_name": data.name,
                    "mlmo_status": {
                        "$not": {
                            "$in": [0]
                    }
                }
            })

            if not query_result:
                last_mlmo = self.DPML_db[self.collection].find_one(
                                sort=[(db_config.item["fld_mlmo_id"], -1)]
                            )
                last_id = last_mlmo['mlmo_id'] + 1

                new_model = {
                    db_config.item["fld_mlmo_id"] : last_id,
                    db_config.item["fld_mlmo_name"] : data.name,
                    db_config.item["fld_mlmo_path"] : file_storage_path,
                    db_config.item["fld_mlmo_status"] : db_config.item["fld_mlmo_status_disable"]
                }
                # db_connect.close()
                new_insert = self.DPML_db[self.collection].insert_one(new_model)

                return jsonify(gen_file_name,file_storage_path)
            
            else:
                # db_connect.close()
                message = {
                    "mes" : "duplicate_name"
                }
                return jsonify(message)

        except Exception as identifier:
        # db_connect.close()
            error = {
                "mes" : str(identifier)
            }
            return jsonify(error)


    def edit_model(self , data = Model()):
        pass

    def delete_model(self , data = Model()):
        pass

    def __del__(self): 
        self.db_connect.close()


class RefManager(Manager):
    def __init__(self): 
        URI = "mongodb://"+db_config.item["db_username"]+":" + \
        db_config.item["db_password"]+"@"+db_config.item["db_host"]
        self.db_connect = MongoClient(URI)
        self.DPML_db = self.db_connect[db_config.item["db_name"]]
        self.collection = db_config.item["db_col_remo"]

        parent = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) 
        self.storage_path = os.path.join(parent, db_config.item["db_file_path"], db_config.item["ref_path"])

    def add_model(self , data = Model()):
        try:
            gen_file_name = uuid.uuid4().hex + "." + data.file.filename.split('.')[-1]
            file_storage_path = os.path.join(self.storage_path,gen_file_name)
            data.file.save(file_storage_path)
            
            query_result = self.DPML_db[self.collection].find_one({
                    "mlmo_name": data.name,
                    "mlmo_status": {
                        "$not": {
                            "$in": [0]
                    }
                }
            })

            if not query_result:
                last_mlmo = self.DPML_db[self.collection].find_one(
                                sort=[(db_config.item["fld_remo_id"], -1)]
                            )
                last_id = last_mlmo['remo_id'] + 1

                new_model = {
                    db_config.item["fld_remo_id"] : last_id,
                    db_config.item["fld_remo_name"] : data.name,
                    db_config.item["fld_remo_width"] : data.width,
                    db_config.item["fld_remo_height"] : data.height,
                    db_config.item["fld_remo_path"] : file_storage_path,
                    db_config.item["fld_remo_unit"] : data.un_id,
                    db_config.item["fld_remo_status"] : db_config.item["fld_remo_status_disable"]
                }
                # db_connect.close()
                new_insert = self.DPML_db[self.collection].insert_one(new_model)

                return jsonify(gen_file_name,file_storage_path)
            
            else:
                # db_connect.close()
                message = {
                    "mes" : "duplicate_name_ref"
                }
                return jsonify(message)

        except Exception as identifier:
        # db_connect.close()
            error = {
                "mes" : str(identifier)
            }
            return jsonify(error)

    def edit_model(self , data = Model()):
        pass

    def delete_model(self , data = Model()):
        pass

    def __del__(self): 
        self.db_connect.close()