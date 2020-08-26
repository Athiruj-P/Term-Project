from flask import Flask, request, jsonify ,Blueprint ,make_response
from pymongo import MongoClient
import numpy as np
from bson.json_util import dumps
import cv2
import base64
from . import image_measurement
from . import image
from .. import db_config

image_processing_api = Blueprint('image_processing_api', __name__)

@image_processing_api.route("/upload_image", methods=['post'])
def upload_image():
    try:
        nparr = np.fromstring(request.files['file'].read(), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR) 

        image_processor = image_measurement.ImageMeasurement()
        input_image = image.Image(image=img)

        result_img = image_processor.measure_obj_size(input_image)

        retval, buffer = cv2.imencode('.png', result_img)
        data = base64.b64encode(buffer)
        response = make_response(data)
        return response
        pass
    except Exception  as identifier:
        result = dumps(str(identifier))
        return result
        pass
