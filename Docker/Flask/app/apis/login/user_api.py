from flask import Flask, request, jsonify ,Blueprint
from pymongo import MongoClient
from bson.json_util import dumps
import ..db_config

user_api = Blueprint('user_api', __name__)

@user_api.route("/user_test")
def user_test():
    return "this is user"