from scipy.spatial import distance as dist
import imutils
from imutils import perspective
from imutils import contours
import glob
import random
import numpy as np
import cv2
import sys
import pprint
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

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

def get_background_mask(image, color):
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

def detect_object(image,path_img):
    height, width = image.shape[:2]
    net = cv2.dnn.readNet("yolov3_training_last.weights", "yolov3_testing.cfg")
    classes = ["Box"]
    images_path = glob.glob(r""+path_img)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    # Store center point of detected object
    arr_center_point = []

    random.shuffle(images_path)
    for img_path in images_path:
        img = cv2.imread(img_path)
        # img = cv2.resize(img, None, fx=0.4, fy=0.4)
        height, width, channels = img.shape
        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
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

def main():
    try:
        path_img = "../Photo/bg_red.JPG"
        image = cv2.imread(path_img)
        hsv=cv2.cvtColor(cv2.GaussianBlur(image, (7, 7), 0), cv2.COLOR_BGR2HSV)
        width_of_ref_obj = 10

        arr_center_point = detect_object(image,path_img)
        ##############################
        # Image size measure section #
        ##############################
        center_contour = []
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)	
        gray = cv2.GaussianBlur(gray, (5, 7), 0)
        edged = cv2.Canny(gray, 50, 200)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)

        mask_r=get_background_mask(hsv, "red")
        edged_r=cv2.Canny(mask_r, 10, 100)
        edged_r=cv2.dilate(edged_r, None, iterations=1)
        edged_r=cv2.erode(edged_r, None, iterations=1)
        
        mask_g=get_background_mask(hsv, "green")
        edged_g=cv2.Canny(mask_g, 10, 100)
        edged_g=cv2.dilate(edged_g, None, iterations=1)
        edged_g=cv2.erode(edged_g, None, iterations=1)

        mask_b=get_background_mask(hsv, "blue")
        edged_b=cv2.Canny(mask_b, 10, 100)
        edged_b=cv2.dilate(edged_b, None, iterations=1)
        edged_b=cv2.erode(edged_b, None, iterations=1)

        merge_rg = cv2.addWeighted(edged_r, 1, edged_g, 1, 0)
        merge_rgb = cv2.addWeighted(merge_rg, 1, edged_b, 1, 0)
        merge_rgb_edged = cv2.addWeighted(merge_rgb, 1, edged, 1, 0)


        cnts = cv2.findContours(merge_rgb_edged.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        (cnts, _) = contours.sort_contours(cnts)

        pixelsPerMetric = None
        origin = image.copy()
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
            # cv2.drawContours(origin, [box.astype("int")], -1, (0, 255, 0), 2)

            # นำจุดทั้ง 4 จุด เก็บไว้ใน (tl, tr, br, bl) เพื่อคำนวณ   หาจุดกึ่งกลาง
            # ระหว่างจุดด้านบน (บนซ้าย บนขวา) และระหว่างจุดด้านล่าง (่ล่างซ้าน ล่างขวา)
            (tl, tr, br, bl) = box
            (tltrX, tltrY) = midpoint(tl, tr)
            (blbrX, blbrY) = midpoint(bl, br)
            # หาจุดกึ่งกลางของกล่องปิดล้อมวัตถุ
            (center_x1, center_y1) = midpoint([tltrX, tltrY], [blbrX, blbrY])
            contour_data = { "center_point":[center_x1, center_y1] , "box" : (tl, tr, br, bl) }
            center_contour.append(contour_data)

        distance_list = []
        for center_point in arr_center_point:
            sub_list = []
            for data in center_contour:
                distance = dist.euclidean(center_point, data['center_point'])
                sub_list.append({
                    "data" : data,
                    "distance" : distance
                })
            distance_list.append(sorted(sub_list, key = lambda i: i['distance'])[0])
        
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(distance_list)

        for obj_list in distance_list:
            (tl, tr, br, bl) = obj_list['data']['box']
            (tltrX, tltrY) = midpoint(tl,tr)
            (blbrX, blbrY) = midpoint(bl,br)
            (tlblX, tlblY) = midpoint(tl,bl)
            (trbrX, trbrY) = midpoint(tr,br)

            # Draw bounding box
            cv2.line(origin,(int(tl[0]), int(tl[1])) ,(int(tr[0]), int(tr[1])) , (0, 255, 0), 2)
            cv2.line(origin,(int(bl[0]), int(bl[1])) ,(int(br[0]), int(br[1])) , (0, 255, 0), 2)
            cv2.line(origin,(int(tl[0]), int(tl[1])) ,(int(bl[0]), int(bl[1])) , (0, 255, 0), 2)
            cv2.line(origin,(int(tr[0]), int(tr[1])) ,(int(br[0]), int(br[1])) , (0, 255, 0), 2)

            cv2.line(origin, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
            (255, 0, 255), 2)
            cv2.line(origin, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
            (255, 0, 255), 2)

            cv2.circle(origin, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
            cv2.circle(origin, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
            cv2.circle(origin, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
            cv2.circle(origin, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

            cv2.circle(origin, (int(tl[0]), int(tl[1])), 5, (0, 0, 255), -1)
            cv2.circle(origin, (int(tr[0]), int(tr[1])), 5, (0, 0, 255), -1)
            cv2.circle(origin, (int(br[0]), int(br[1])), 5, (0, 0, 255), -1)
            cv2.circle(origin, (int(bl[0]), int(bl[1])), 5, (0, 0, 255), -1)

            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
            if pixelsPerMetric is None:
                pixelsPerMetric = dB / width_of_ref_obj
            dimA = dA / pixelsPerMetric
            dimB = dB / pixelsPerMetric

            cv2.putText(origin, "{:.1f}mm".format(dimA),
                (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 255, 255), 2)
            cv2.putText(origin, "{:.1f}mm".format(dimB),
                (int(trbrX  + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 255, 255), 2)
        origin = ResizeWithAspectRatio(origin, width=1000)
        cv2.imshow("Image", origin)
        cv2.waitKey(0)
        raise TypeError("")
    except Exception as srt_err:
        return 0
    finally:
        return 0
if __name__ == '__main__':
    main()