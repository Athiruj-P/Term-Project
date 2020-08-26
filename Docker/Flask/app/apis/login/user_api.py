from flask import Flask, request, jsonify ,Blueprint
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity,jwt_refresh_token_required,
    create_refresh_token
)
from pymongo import MongoClient
import hashlib
from bson.json_util import dumps
import logging.config
from .. import db_config

jwt = JWTManager()
user_api = Blueprint('user_api', __name__)

logger = logging.getLogger("Login_api")
URI = "mongodb://"+db_config.item["db_username"]+":" + \
db_config.item["db_password"]+"@"+db_config.item["db_host"]
logger.info("Connecting to database")
db_connect = MongoClient(URI)
logger.info("Connected to database")
DPML_db = db_connect[db_config.item["db_name"]]
collection = db_config.item["db_col_user"]

@user_api.route("/login", methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"mes": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"mes": "Missing username parameter"}), 400
    if not password:
        return jsonify({"mes": "Missing password parameter"}), 400

    # sha_signature = hashlib.sha256(password.encode()).hexdigest()   
    # logger.info("pass : {}".format(sha_signature))

    query_result = DPML_db[collection].find_one({
        db_config.item['fld_user_name']: username ,
        db_config.item['fld_user_password']: password
    })
    db_connect.close()
    logger.info("query_result : {}".format(query_result))

    if not query_result:
        return jsonify({"login" : False}), 401
    else:
        DPML_db[collection].update(
            { db_config.item['fld_user_id']:query_result['user_id'] },
            { "$set":{ db_config.item['fld_user_login_status']:db_config.item['fld_user_status_login'] }}
        )
    
    access_token = create_access_token(identity=username)
    tokens = {
        'access_token': create_access_token(identity=username),
        'refresh_token': create_refresh_token(identity=username) 
    }
    return jsonify(tokens), 200

@user_api.route('/logout', methods=['POST'])
def logout():
    username = request.json.get('username', None)
    if not username:
        return jsonify({"mes": "Missing username parameter"}), 400

    DPML_db[collection].update(
        { db_config.item['fld_user_name']:username },
        { "$set":{ db_config.item['fld_user_login_status']:db_config.item['fld_user_status_logout'] }}
    )

    return jsonify({"logout" : True}), 200

@user_api.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {
        'refresh_token': create_access_token(identity=current_user)
    }
    return jsonify(ret), 200

@user_api.route('/protected', methods=['POST'])
@jwt_required
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200