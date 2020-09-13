import cv2
import numpy as np
import imutils
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import glob
import pprint
import random

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
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

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def max_area(cnts = None):
    max_cnt_area = -1.0
    max_cnt = None
    for c in cnts:
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        (tl, tr, br, bl) = box
        dA = dist.euclidean((tl[0],tl[1]), (bl[0],bl[1]))
        dB = dist.euclidean((tr[0],tr[1]), (br[0],br[1]))
        print('####################')
        print('tl: {}'.format(tl))
        print('tr: {}'.format(tr))
        print('br: {}'.format(br))
        print('bl: {}'.format(bl))
        print('dA: {}'.format(dA))
        print('dB: {}'.format(dB))
        area = dA * dB
        print('area: {}'.format(area))
        print('####################')
        if(max_cnt_area < area):
            max_cnt = c
            max_cnt_area = area
    # print('CNT : {}'.format(max_cnt))
    return max_cnt
    

def con(origin, cnts = None, pixelsPerMetric = None):
    c = cnts
    # for c in cnts:
    # print(cv2.contourArea(c))
    # คำนวณหาเส้นรอบรูปรางของวัตถุที่มีความเอียง
    # origin = image.copy()
    box = cv2.minAreaRect(c)
    box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")

    # วางเส้นรอบรูปของวัตถุโดยมีลำดับคือ บนซ้าย บนขวา ล่างซ้าย ล่างขวา
    box = perspective.order_points(box)
    cv2.drawContours(origin, [box.astype("int")], -1, (0, 255, 0), 2)

    # วาดรูปจุด (point) ในแต่ละมุมของเส้นรอบรูป
    for (x, y) in box:
        cv2.circle(origin, (int(x), int(y)), 5, (0, 0, 255), -1)

    # นำจุดทั้ง 4 จุด เก็บไว้ใน (tl, tr, br, bl) เพื่อคำนวณหาจุดกึ่งกลาง
    # ระหว่างจุดด้านบน (บนซ้าย บนขวา) และระหว่างจุดด้านล่าง (่ล่างซ้าน ล่างขวา)
    (tl, tr, br, bl) = box
    (tltrX, tltrY) = midpoint(tl, tr)
    (blbrX, blbrY) = midpoint(bl, br)

    # หาจุดกึ่งกลางของกล่องปิดล้อมวัตถุ
    (center_x1, center_y1) = midpoint([tltrX, tltrY], [blbrX, blbrY])

    # คำนวณจุดกึ่งกลางระหว่าง บนซ้าย ล่างซ้าย 
    # และ บนขวา ล่างขวา 
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)
    
    
    # หาจุดกึ่งกลางของกล่องปิดล้อมวัตถุ (อันนี้มีหรือไม่มีก็ได้ เพราะข้างบนคำนวณไปแล้ว)
    (center_x2, center_y2) = midpoint([tlblX, tlblY], [trbrX, trbrY])


    # วาดรูปจุดกึ่งกลาง (middle point) จากที่คำนวณข้างต้น
    cv2.circle(origin, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
    cv2.circle(origin, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
    cv2.circle(origin, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
    cv2.circle(origin, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

    # วาดจุดวงกลมของจุดกึ่งกลางของกล่องปิดล้อมวัตถุ
    cv2.circle(origin, (int(center_x1), int(center_y1)), 5, (0, 100, 255), -1)
    # cv2.circle(origin, (int(center_x2), int(center_y2)), 5, (0, 100, 255), -1)

    # ลางเส้นเชื่อมระหว่างจุดกึ่งกลาง
    cv2.line(origin, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
        (255, 0, 255), 2)
    cv2.line(origin, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
        (255, 0, 255), 2)

    # คำนวณหาระยะหว่างระหว่างจุด (Euclidean distance)
    dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

    # กรณีที่ไม่มีการกำหนดค่า pixelsPerMetric จะนำค่าที่ได้จากพารามิเตอร์มาคำนวณหาอัตราส่วน
    if pixelsPerMetric is None:
        pixelsPerMetric = dB / 20

    # คำนวณหาความยาวด้านของวัตถุ
    dimA = dA / pixelsPerMetric
    dimB = dB / pixelsPerMetric

    # แสดงตัวเลขจากการคำนวณ

    cv2.putText(origin, "{:.1f}mm".format(dimA),
        (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
        0.65, (255, 255, 255), 2)
    cv2.putText(origin, "{:.1f}mm".format(dimB),
        (int(trbrX  + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
        0.65, (255, 255, 255), 2)
        # break
    cv2.imshow("Image_c0n", origin)
    # cv2.waitKey(0)

# Load Yolo
# net = cv2.dnn.readNet("yolov3_training_last.weights", "yolov3_testing.cfg")
net = cv2.dnn.readNet("../Docker/Flask/app/db_file/ref_model/logo_training_final.weights", "../Docker/Flask/app/db_file/ref_model/ref_model_config.cfg")

# Name custom object
classes = ["Ref"]

# Images path
img_name = 'IMG_8115.JPG'
path_img = "C:/Users/First-AP/Desktop/test_img/{}".format(img_name)
images_path = glob.glob(r""+path_img)



layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Insert here the path of your images
random.shuffle(images_path)
# loop through all the images
for img_path in images_path:
    # Loading image
    img = cv2.imread(img_path)
    img = ResizeWithAspectRatio(img, width=1500)
    # img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 1/255, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []

    # loop over each of the layer outputs
    for out in outs:
        # loop over each of the detections
        for detection in out:
            # extract the class ID and confidence (i.e., probability) of
		    # the current object detection
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            # filter out weak predictions by ensuring the detected
		    # probability is greater than the minimum probability
            if confidence > 0.3:
                print(class_id)

                # Object detected
                # scale the bounding box coordinates back relative to the
                # size of the image, keeping in mind that YOLO actually
                # returns the center (x, y)-coordinates of the bounding
                # box followed by the boxes' width and height
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                print("center_x : {}".format(center_x))
                print("center_y : {}".format(center_y))
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                print("width : {}".format(w))
                print("height : {}".format(h))

                # Rectangle coordinates
                # use the center (x, y)-coordinates to derive the top and
			    # and left corner of the bounding box
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

        print("========================")


    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    print(indexes)
    font = cv2.FONT_HERSHEY_PLAIN
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            per = 0.10
            crop_img = img[y-int(h*per):y+h+int(h*per), x-int(w*per):x+w+int(w*per)]
            cv2.imwrite("croped.jpg",crop_img)
            # cv2.imshow("cropped", crop_img)
            gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)	
            gray = cv2.GaussianBlur(gray, (7, 7), 0)
            edged = cv2.Canny(gray, 50, 200)
            _, binary = cv2.threshold(edged, 225, 255, cv2.THRESH_BINARY)
            temp_b = ResizeWithAspectRatio(binary,width=500)
            # cv2.imshow("binary", temp_b)

            cnts = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)  
            max_cnt_area = max_area(cnts)
            con(crop_img.copy(),max_cnt_area)
            # get_cnt = cnts[0]
            # (cnts, _) = contours.sort_contours(cnts)
            # cnts = sorted(cnts, key=lambda x: cv2.contourArea(get_cnt),reverse=True)
            # pp = pprint.PrettyPrinter(indent=4)
            # pp.pprint(cnts)


            label = str(classes[class_ids[i]])
            color = colors[class_ids[i]]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 2)

    origin = ResizeWithAspectRatio(img, width=1000)
    cv2.imshow("Image", origin)
    key = cv2.waitKey(0)

cv2.destroyAllWindows()