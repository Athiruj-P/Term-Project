from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
import db_config

URI = "mongodb://"+db_config.item["db_username"]+":" + \
    db_config.item["db_password"]+"@"+db_config.item["db_host"]
db_connect = MongoClient(URI)
DPML_db = db_connect["DPML_db"]
user_collection = db_config.item["db_col_user"]
role_collection = db_config.item["db_col_role"]
mlmo_collection = db_config.item["db_col_mlmo"]
remo_collection = db_config.item["db_col_remo"]
unit_collection = db_config.item["db_col_unit"]

app = Flask(__name__)

username = "Athiruj"

@app.route("/")
def hello():
    return "Hello" + username

# Get all user
@app.route('/get_all_user', methods=['get'])
def get_all_user():
    users = []
    for i in DPML_db[user_collection].find():
        i.pop('_id')
        users.append(i)
    db_connect.close()
    result = jsonify(users)
    return result

# Get by username
@app.route('/get_user', methods=['post'])
def get_user():
    username = request.form.get('username')
    query = {"username": username}
    res_list = DPML_db[user_collection].find_one(query)
    db_connect.close()
    return dumps(res_list)

# Add new user
@app.route('/add_new_user', methods=['post'])
def add_new_user():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    status = request.form.get('status')

    new_user = {
        "username": username,
        "password": password,
        "role": int(role),
        "status": int(status)
    }

    new_insert = DPML_db[user_collection].insert_one(new_user)
    db_connect.close()
    return dumps(new_insert.inserted_id)

# Update by username
@app.route('/edit_password_by_user', methods=['post'])
def edit_password_by_user():
    username = request.form.get('username')
    password = request.form.get('password')
    query = {"username": username}
    edit_data = {"$set" : {"password" : password} }
    DPML_db[user_collection].update_one(query,edit_data)
    db_connect.close()
    return jsonify({"result" : "A document has been updated."})

# Remove by username
@app.route('/remove_user', methods=['post'])
def remove_user():
    username = request.form.get('username')
    query = {"username": username}
    res_list = DPML_db[user_collection].delete_one(query)
    db_connect.close()
    return jsonify({"result" : "A document has been deleted."})

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=5001)
