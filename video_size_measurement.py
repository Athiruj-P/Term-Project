# Object size measurement from video
# Description : โปรแกรมการวัดขนาดวัตถุจากภาพเคลื่อนไหว
# Create date : 07-July-2020 
# Auther : Athiruj Poositaporn

from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import imutils
import argparse
import numpy as np
import cv2

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--width", type=float, required=True,
                help="width of the left-most object in the image (in millimeter)")
args = vars(ap.parse_args())

cap = cv2.VideoCapture(0)

show_live_video = True

while(show_live_video):
    # Capture frame-by-frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)

    edged = cv2.Canny(gray, 50, 100)
    cv2.imshow("Obj-edged", edged)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    cnts = cv2.findContours(
        edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    (cnts, _) = contours.sort_contours(cnts)
    pixelsPerMetric = None

    # loop เพื่อคำนวณความยาวด้านของแต่ละรูปทรงที่ค้นหาได้จากรูปภาพ
    for c in cnts:
	# cv2.contourArea => คืนค่าพื้นที่ของรูปทรงที่ c มีหน่วยคือ pixel
    # ถ้าพื้นที่มีขนาดที่เล็กเกินไป จะข้ามไปยังรูปทรงถัดไป
        if cv2.contourArea(c) < 100:
            continue

        # คำนวณหาเส้นรอบรูปรางของวัตถุที่มีความเอียง
        origin = frame
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

        # คำนวณจุดกึ่งกลางระหว่าง บนซ้าย ล่างซ้าย 
        # และ บนขวา ล่างขวา 
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        # วาดรูปจุดกึ่งกลาง (middle point) จากที่คำนวณข้างต้น
        cv2.circle(origin, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
        cv2.circle(origin, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
        cv2.circle(origin, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
        cv2.circle(origin, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

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
            pixelsPerMetric = dB / args["width"]

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

        cv2.imshow("Image", origin)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            show_live_video = False

cap.release()
cv2.destroyAllWindows()
