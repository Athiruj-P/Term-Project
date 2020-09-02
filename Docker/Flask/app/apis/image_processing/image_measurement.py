from scipy.spatial import distance as dist
import logging.config
import imutils
from imutils import perspective
from imutils import contours
import glob
import random
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import os
from pymongo import MongoClient
import sys
from .. import err_msg
from .. import db_config
logger = logging.getLogger("image_measurement")

URI = "mongodb://"+db_config.item["db_username"]+":" + \
db_config.item["db_password"]+"@"+db_config.item["db_host"]
db_connect = MongoClient(URI)
logger.info("Connected to database")
DPML_db = db_connect[db_config.item["db_name"]]
unit_collection = db_config.item['db_col_unit']
ml_model_collection = db_config.item['db_col_mlmo']
ref_model_collection = db_config.item['db_col_remo']

parent = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
thai_font_path = os.path.join(parent, db_config.item["db_file_path"], "thai_font","THSarabunNewBold.ttf")
class ImageMeasurement:
    def __init__(self):
        parent = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

        query_mlmo = DPML_db[ml_model_collection].find_one({
            db_config.item['fld_mlmo_status']: db_config.item['fld_mlmo_status_active']
        }, {
            db_config.item['fld_mlmo_name']: 1,
            db_config.item['fld_mlmo_path']: 1,
        })

        if(not query_mlmo):
            logger.warning(err_msg.msg['no_active_ml_model'])
            raise TypeError(err_msg.msg['no_active_ml_model'])
        else:
            query_mlmo.pop('_id')

        query_remo = DPML_db[ref_model_collection].find_one({
            db_config.item['fld_remo_status']: db_config.item['fld_remo_status_active']
        })

        if(not query_remo):
            logger.warning(err_msg.msg['no_active_ref_model'])
            raise TypeError(err_msg.msg['no_active_ref_model'])
        else:
            query_remo.pop('_id')
        
        query_unit = DPML_db[unit_collection].find_one({
            db_config.item['fld_un_id']: query_remo[db_config.item['fld_remo_unit']]
        })
        query_unit.pop('_id')
        # logger.debug("mlmo_name: {}".format(query_mlmo[db_config.item['fld_mlmo_name']]))
        # logger.debug("mlmo_path: {}".format(query_mlmo[db_config.item['fld_mlmo_path']]))

        self.ml_model_path = query_mlmo[db_config.item['fld_mlmo_path']]
        self.ml_model_name = query_mlmo[db_config.item['fld_mlmo_name']]

        self.ref_model_path = query_remo[db_config.item['fld_remo_path']]
        self.ref_model_name = query_remo[db_config.item['fld_remo_name']]
        self.ref_model_width = query_remo[db_config.item['fld_remo_width']]
        self.ref_model_unit = query_unit[db_config.item['fld_un_abb_name']]

        self.ml_config_path = os.path.join(parent, db_config.item["db_file_path"], db_config.item["ml_path"],"ml_model_config.cfg")
        self.ref_config_path = os.path.join(parent, db_config.item["db_file_path"], db_config.item["ref_path"],"ref_model_config.cfg")

    # find_midpoint
    # Description : ฟังก์ชันสำหรับหาจุดกึงกลางจากจุด 2 จุด
    # Author : Athiruj Poositaporn
    def find_midpoint(self,ptA, ptB):
        return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

    # resize_with_aspect_ratio
    # Description : ฟังก์ชันปรับขนาดรูปภาพตามพารามิเตอร์ที่ส่งค่ามาเป็น Pixel
    # Author : Athiruj Poositaporn
    def resize_with_aspect_ratio(self, image, width=None, height=None, inter=cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]

        if width is None and height is None:
            return image
        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        return cv2.resize(image, dim, interpolation=inter)

    # detect_object
    # Description : ฟังก์ชันตรวจจับวัตถุที่ใสใจในการวัดขนาดซึ่งใช้ ML model โดยเป็นการหาตำแหน่งจุดกึ่งกลางของวัตถุ
    # Author : Athiruj Poositaporn
    def detect_object(self,image):
        height, width = image.shape[:2]
        # อ่านไฟล์ weights และ config
        net = cv2.dnn.readNet(self.ml_model_path, self.ml_config_path) 

        #ค่าที่ได้จากฐานข้อมูลของ ML model เป็นชื่อของวัตถุที่สนใจวัดขนาด
        classes = [self.ml_model_name]

        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        # Store center point of detected object
        arr_center_point = []

        height, width, channels = image.shape
        # Detecting objects
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        # loop over each of the layer outputs
        for out in outs:
            # loop over each of the detections
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.3:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    arr_center_point.append([center_x,center_y])
                    pass
        return arr_center_point

    # detect_ref_object
    # Description : ฟังก์ชันตรวจจับวัตถุอ้างอิงซึ่งใช้ Ref model โดยเป็นการหาตำแหน่งจุดกึ่งกลางของวัตถุอ้างอิง
    # Author : Athiruj Poositaporn
    def detect_ref_object(self,image):
        height, width = image.shape[:2]
        net = cv2.dnn.readNet(self.ref_model_path, self.ref_config_path)
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        # Store center point of detected object
        arr_center_point = None

        height, width, channels = image.shape
        # Detecting objects
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        # loop over each of the layer outputs
        for out in outs:
            # loop over each of the detections
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.3:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    arr_center_point = [center_x,center_y]
        return arr_center_point

    # get_background_mask
    # Description : ฟังก์ชันมาร์กช่วงของสี 3 สีคือสีแดง น้ำเงิน และสีเขียว เพื่อเป็นการตัดสีพื้นหลังของภาพที่มีสีดังกล่าวออก
    # Author : Athiruj Poositaporn
    def get_background_mask(self,image, color):
        if color == "red":
            # คาบของสีแดงมี 2 ช่วง จึงจะครอบคลุม
            mask01 = cv2.inRange( image, np.array([0, 49, 19]), np.array([5, 255, 255]) )
            mask02 = cv2.inRange( image, np.array([175, 50, 20]), np.array([180, 255, 255]) )
            return cv2.bitwise_or(mask01, mask02)
        elif color == "green":
            return cv2.inRange( image, np.array([39, 23, 111]), np.array([104, 255, 255]) )
        elif color == "blue":
            return cv2.inRange( image, np.array([94, 80, 2]), np.array([126, 255, 255]) )
        else:
            return False

    # measure_obj_size
    # Description : ฟังก์ชันการวัดขนาดของวัตถุ
    # Author : Athiruj Poositaporn
    def measure_obj_size(self,image):
        # @@@@@@@@@@@@@@@@@@@@@@@@@
        # ต้องแก้ไขให้ดึงข้อมูลจาก DB
        # @@@@@@@@@@@@@@@@@@@@@@@@@
        # อ่านไฟล์ weights และ config
        # ต้องเปลี่ยนเป็นดึงข้อมูลจาก DB 2 ค่าคือ path ของ ML และ Ref
        parent = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        # self.ml_model_path = os.path.join(parent, db_config.item["db_file_path"], db_config.item["ml_path"],"box_model.weights")
        # self.ref_model_path = os.path.join(parent, db_config.item["db_file_path"], db_config.item["ref_path"],"dpml_logo_model.weights")
        # @@@@@@@@@@@@@@@@@@@@@@@@@

        input_image = image.image
        input_image = self.resize_with_aspect_ratio(image.image,width=1080)
        hsv=cv2.cvtColor(cv2.GaussianBlur(input_image, (7, 7), 0), cv2.COLOR_BGR2HSV)

        # @@@@@@@@@@@@@@@@@@@@@@@@@
        # ต้องแก้ไขให้ดึงข้อมูลจาก DB
        # @@@@@@@@@@@@@@@@@@@@@@@@@
        #ได้จากข้อมูลความกว้างหรือยาวจาก DB ของ Ref model
        width_of_ref_obj = self.ref_model_width
        # @@@@@@@@@@@@@@@@@@@@@@@@@

        arr_center_point = self.detect_object(input_image)
        ref_center_point = self.detect_ref_object(input_image)

        try:
            # หากไม่พบวัตถุอ้างอิงจะไม่วัดขนาด
            if(not ref_center_point):
                logger.warning("Reference object not detected")
                return {'mes' : err_msg.msg['ref_model_not_found'],'img' : input_image , 'status' : "ref_not_found"}
            # หากไม่พบวัตถุที่สนใจจะไม่วัดขนาด
            elif(not arr_center_point):
                logger.warning("Object not detected")
                return {'mes' : err_msg.msg['ml_model_not_found'],'img' : input_image , 'status' : "ml_not_found"}
            
            ##############################
            # Image size measure section #
            ##############################
            center_contour_list = []
            # เปลี่ยนสีของรูปภาพให้เป็นสีเทา (grayscale)
            gray = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
            # เบลอรูปภาพเพื่่อให้ภาพ Smooth ขึ้นเล็กน้อย
            gray = cv2.GaussianBlur(gray, (5, 7), 0)

            # cv2.Canny => การตีกรอบให้กับภาพ
            edged = cv2.Canny(gray, 50, 200)
            # dilate => ขยายเส้นขอบให้ใหญ่ขึ้น
            edged = cv2.dilate(edged, None, iterations=1)
            # dilate => ลบ Noise สีขาวออกจากรูปภาพ
            edged = cv2.erode(edged, None, iterations=1)

            ##########################################
            # Mask Red Geen Blue and merge all result
            ##########################################
            mask_r=self.get_background_mask(hsv, "red")
            edged_r=cv2.Canny(mask_r, 10, 100)
            edged_r=cv2.dilate(edged_r, None, iterations=1)
            edged_r=cv2.erode(edged_r, None, iterations=1)
            
            mask_g=self.get_background_mask(hsv, "green")
            edged_g=cv2.Canny(mask_g, 10, 100)
            edged_g=cv2.dilate(edged_g, None, iterations=1)
            edged_g=cv2.erode(edged_g, None, iterations=1)

            mask_b=self.get_background_mask(hsv, "blue")
            edged_b=cv2.Canny(mask_b, 10, 100)
            edged_b=cv2.dilate(edged_b, None, iterations=1)
            edged_b=cv2.erode(edged_b, None, iterations=1)

            merge_rg = cv2.addWeighted(edged_r, 1, edged_g, 1, 0)
            merge_rgb = cv2.addWeighted(merge_rg, 1, edged_b, 1, 0)
            merge_rgb_edged = cv2.addWeighted(merge_rgb, 1, edged, 1, 0)
            ##########################################
            ##########################################

            # ค้นหารูปร่างของวัตถุ
            # cv2.findContours(รุูปภาพ,ดึงเส้นขอบของวัตถุ,การประมาณการรูปร่างของวัตถุ)
            cnts = cv2.findContours(merge_rgb_edged.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            # เรียงลำดับเส้นขอบของวัตถุ เพื่อสามารถเข้าถึงวัตถุอ้างอิงได้ และสามารถ
            # หาค่าของ pixelsPerMetric จากวัตถุอ้างอิงดังกล่าว
            (cnts, _) = contours.sort_contours(cnts)

            # กำหนดให้ pixelsPerMetric เป็น None ซึ่งใช้ในการคำนวณอัตราส่วนของรูปภาพอ้างอิง
            # เพื่อใช้ค้นหาความยาวด้านของวัตถุเป้าหมาย
            pixelsPerMetric = None
            origin = input_image.copy()

            # loop เพื่อคำนวณความยาวด้านของแต่ละรูปทรงที่ค้นหาได้จากรูปภาพ
            for c in cnts:
                # cv2.contourArea => คืนค่าพื้นที่ของรูปทรงที่ c มีหน่วยคือ pixel
                # ถ้าพื้นที่มีขนาดที่เล็กเกินไป จะข้ามไปยังรูปทรงถัดไป
                # (cv2.contourArea(c)/args["width"]*args["width"]) คือการแปลงหน่วยจาก pixel^2 เป็น MM^2
                if cv2.contourArea(c) < 1000:
                    continue
                # คำนวณหาเส้นรอบรูปรางของวัตถุที่มีความเอียง
                box = cv2.minAreaRect(c)
                box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
                box = np.array(box, dtype="int")

                # วางเส้นรอบรูปของวัตถุโดยมีลำดับคือ บนซ้าย บนขวา ล่างซ้าย ล่างขวา
                box = perspective.order_points(box)
                # นำจุดทั้ง 4 จุด เก็บไว้ใน (tl, tr, br, bl) เพื่อคำนวณหาจุดกึ่งกลาง
                # ระหว่างจุดด้านบน (บนซ้าย บนขวา) และระหว่างจุดด้านล่าง (่ล่างซ้าน ล่างขวา)
                (tl, tr, br, bl) = box
                (tltrX, tltrY) = self.find_midpoint(tl, tr)
                (blbrX, blbrY) = self.find_midpoint(bl, br)
                # หาจุดกึ่งกลางของกล่องปิดล้อมวัตถุ
                (center_x1, center_y1) = self.find_midpoint([tltrX, tltrY], [blbrX, blbrY])
                contour_data = { "center_point":[center_x1, center_y1] , "box" : (tl, tr, br, bl) }
                center_contour_list.append(contour_data)
            
            # หาตำแหน่งของจุดกึ่งกลางที่ตรวจจับได้ เพื่อหาจุดกึ่งหลางของวัตถุที่สนใจในระยะที่สั้นที่สุด
            distance_list_of_ml_obj = []
            for center_point in arr_center_point:
                sub_list = []
                for data in center_contour_list:
                    distance = dist.euclidean(center_point, data['center_point'])
                    sub_list.append({
                        "data" : data,
                        "distance" : distance
                    })
                distance_list_of_ml_obj.append(sorted(sub_list, key = lambda i: i['distance'])[0])

            ##########################################
            # หาตำแหน่งของจุดกึ่งกลางของวัตถุอ้างอิงที่ตรวจจับได้
            ##########################################
            distance_list_of_ref_obj = []
            sub_list = []
            for data in center_contour_list:
                distance = dist.euclidean(ref_center_point, data['center_point'])
                sub_list.append({
                    "data" : data,
                    "distance" : distance
                })
            distance_list_of_ref_obj.append(sorted(sub_list, key = lambda i: i['distance'])[0])
            ##########################################
            ##########################################

            #############################################################
            # เทียบจุดกึ่งกลางของวัตถุอ้างอิงกับกล่องปิดล้อมวัตถุทั้งหมดเพื่อหาจุดที่ใกล้ที่สุด
            # แล้วทำการวาดกรอบปิดล้อมวัตถุอ้างอิง พร้อมบอกขนาด
            #############################################################
            for obj_list in distance_list_of_ref_obj:
                (tl, tr, br, bl) = obj_list['data']['box']
                (tltrX, tltrY) = self.find_midpoint(tl,tr)
                (blbrX, blbrY) = self.find_midpoint(bl,br)
                (tlblX, tlblY) = self.find_midpoint(tl,bl)
                (trbrX, trbrY) = self.find_midpoint(tr,br)

                cv2.line(origin,(int(tl[0]), int(tl[1])) ,(int(tr[0]), int(tr[1])) , (0, 255, 0), 2)
                cv2.line(origin,(int(bl[0]), int(bl[1])) ,(int(br[0]), int(br[1])) , (0, 255, 0), 2)
                cv2.line(origin,(int(tl[0]), int(tl[1])) ,(int(bl[0]), int(bl[1])) , (0, 255, 0), 2)
                cv2.line(origin,(int(tr[0]), int(tr[1])) ,(int(br[0]), int(br[1])) , (0, 255, 0), 2)

                dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
                dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                pixelsPerMetric = dB / width_of_ref_obj

                dimA = dA / pixelsPerMetric
                dimB = dB / pixelsPerMetric
                # logger.debug("self.ref_model_name : {}".format(self.ref_model_name))
                font = ImageFont.truetype(thai_font_path, 40)
                img_pil = Image.fromarray(origin)
                draw = ImageDraw.Draw(img_pil)
                draw.text( (int(tl[0]), int(tl[1] - 50)),"[{}]".format(self.ref_model_name), font = font, fill = (255, 255, 255 , 0))
                origin = np.array(img_pil)

                # cv2.putText(origin, "[{}]".format(self.ref_model_name),
                #     (int(tl[0]), int(tl[1] - 30)), cv2.FONT_HERSHEY_SIMPLEX,
                #     0.65, (255, 255, 255), 2)

                # cv2.putText(
                #     origin, 
                #     "{:.2f}mm".format(dimB),
                #     (int(tltrX - 15), int(tltrY - 10)), 
                #     cv2.FONT_HERSHEY_SIMPLEX,
                #     1, 
                #     (255, 255, 255), 
                #     2
                # )

                # cv2.putText(
                #     origin, 
                #     "{:.2f}mm".format(dimA),
                #     (int(trbrX  + 10), int(trbrY)), 
                #     cv2.FONT_HERSHEY_SIMPLEX,
                #     1, 
                #     (255, 255, 255), 
                #     2
                # )
            #############################################################
            #############################################################
            
            #############################################################
            # เทียบจุดกึ่งกลางของวัตถุกับกล่องปิดล้อมวัตถุทั้งหมดเพื่อหาจุดที่ใกล้ที่สุด
            # แล้วทำการวาดกรอบปิดล้อมวัตถุ พร้อมบอกขนาด
            #############################################################
            object_lable_number = 1
            result_object_list = []

            # Loop สำหรับวาดภาพกล่องปิดล้อมวัตถุที่สนใน และคำนวณขนาด
            for obj_list in distance_list_of_ml_obj:
                (tl, tr, br, bl) = obj_list['data']['box']
                (tltrX, tltrY) = self.find_midpoint(tl,tr)
                (blbrX, blbrY) = self.find_midpoint(bl,br)
                (tlblX, tlblY) = self.find_midpoint(tl,bl)
                (trbrX, trbrY) = self.find_midpoint(tr,br)

                # Draw bounding box
                cv2.line(origin,(int(tl[0]), int(tl[1])) ,(int(tr[0]), int(tr[1])) , (0, 255, 0), 2)
                cv2.line(origin,(int(bl[0]), int(bl[1])) ,(int(br[0]), int(br[1])) , (0, 255, 0), 2)
                cv2.line(origin,(int(tl[0]), int(tl[1])) ,(int(bl[0]), int(bl[1])) , (0, 255, 0), 2)
                cv2.line(origin,(int(tr[0]), int(tr[1])) ,(int(br[0]), int(br[1])) , (0, 255, 0), 2)

                # Draw coner points
                cv2.circle(origin, (int(tl[0]), int(tl[1])), 5, (0, 0, 255), -1)
                cv2.circle(origin, (int(tr[0]), int(tr[1])), 5, (0, 0, 255), -1)
                cv2.circle(origin, (int(br[0]), int(br[1])), 5, (0, 0, 255), -1)
                cv2.circle(origin, (int(bl[0]), int(bl[1])), 5, (0, 0, 255), -1)

                dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
                dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

                dimA = dA / pixelsPerMetric
                dimB = dB / pixelsPerMetric
                object_lable = "[" + self.ml_model_name + "_" + str(object_lable_number) + "]"
                object_lable_number = object_lable_number + 1
                
                result_object_data = {
                    'lable' : object_lable,
                    'dimA' : dimB, #สลับค่า A B เพราะต้องการแสดงผลตามความกว้างและยาว
                    'dimB' : dimA,
                    'unit' : self.ref_model_unit
                }

                result_object_list.append(result_object_data)
                font = ImageFont.truetype(thai_font_path, 40)
                img_pil = Image.fromarray(origin)
                draw = ImageDraw.Draw(img_pil)
                draw.text( (int(tl[0]), int(tl[1] - 50)),object_lable, font = font, fill = (255, 255, 255 , 0))
                origin = np.array(img_pil)
                # cv2.putText(origin, object_lable,
                #     (int(tl[0]), int(tl[1] - 30)), cv2.FONT_HERSHEY_SIMPLEX,
                #     0.65, (255, 255, 255), 2)

                # Dimension A lable
                cv2.circle(origin, (int(tltrX - 5), int(tltrY - 20)), 26, (0, 0, 0), -1)
                cv2.putText(
                    origin, 
                    "A",
                    (int(tltrX - 15), int(tltrY - 10)), 
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, 
                    (255, 255, 255), 
                    2
                )

                # Dimension B lable
                cv2.circle(origin, (int(trbrX + 20), int(trbrY - 10)), 26, (0, 0, 0), -1)
                cv2.putText(
                    origin, 
                    "B",
                    (int(trbrX  + 10), int(trbrY)), 
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, 
                    (255, 255, 255), 
                    2
                )
            #############################################################
            #############################################################

            result = {'img' : origin ,'img_data' : result_object_list ,'status' : "success"}
            return result
        except Exception as identifier:
            try:
                # ใช้เพื่อค้นหาว่าค่า identifier มีใน err_msg.msg หรือไม่ ถ้าไม่มีการทำงานจะ error และเข้าสู่ except
                list(err_msg.msg.keys())[list(err_msg.msg.values()).index(identifier)]
            except:
                logger.warning("{}.".format(str(identifier)))
                result = {'mes' : str(identifier), 'status' : "system_error"}
                # result = {'mes' : err_msg.msg['other_err']}
            return result
    def __del__(self): 
        db_connect.close()