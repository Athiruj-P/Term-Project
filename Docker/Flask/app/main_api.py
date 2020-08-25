from flask import Flask, request, jsonify
import logging.config
from apis.login.user_api import user_api
from apis.image_processing.image_processing_api import image_processing_api
from apis.model_management.model_management_api import model_management_api
from apis.log_management.log_management_api import log_management_api
from logging_config import dict_config

logger = logging.getLogger("main")
logging.config.dictConfig(dict_config)

app = Flask(__name__)
logger.info("Created flask app.")
app.register_blueprint(user_api)
logger.info('Registered image_processing_api blueprint ')
app.register_blueprint(image_processing_api)
logger.info('Registered user_api blueprint ')
app.register_blueprint(model_management_api)
logger.info('Registered model_management_api blueprint ')
app.register_blueprint(log_management_api)
logger.info('Registered log_management_api blueprint ')

@app.route("/")
def hello():
    app.logger.info('Processing default request')
    return "Hello World!"

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

if __name__ == "__main__":
     app.run(host='0.0.0.0', debug=True, port=5001)