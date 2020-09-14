# Object size measurement from image with RGB background
# Description : โปรแกรมการวัดขนาดวัตถุจากภาพ
# Update date : 09-July-2020
# Auther : Athiruj Poositaporn

# import the necessary packages
# LOC : 4 => การหาระยะห่างระหว่างจุดหรือหลักของ Euclidean distance
from scipy.spatial import distance as dist

# imutils ใช้เกี่ยวกับการจัดการภาพคือ การหมุน
from imutils import perspective
# LOC : 10 contours => การหารูปร่าง
from imutils import contours

import numpy as np
# argparse =>  Library สำหรับรับพารามิเตอร์
import argparse
import imutils
import cv2

# midpoint
# ฟังก์ชันหาจุดกึ่งกลางระหว่างจุดสองจุด
# Input : point A and point B
# Output : Middle point of point A and point B
# Create date : 08-July-2020
# Auther : Athiruj Poositaporn
def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# ResizeWithAspectRatio
# ฟังก์ชันปรับขนาดของภาพตามที่กำหนด (Pixel) ตามอัตราส่วนของภาพ
# Input : Image , Width and/or hight in pixel
# Output : Resized image
# Create date : 07-July-2020
# Auther : Athiruj Poositaporn
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

# get_background_mask
# ฟังก์ชัน mask สีพื้นหลังตามภาพและสีที่กำหนด
# Input : Image , background color
# Output : Mask
# Create date : 07-July-2020
# Auther : Athiruj Poositaporn
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


# LOC : 24 - 29  =>รับพารามิเตอร์ 2 ค่าคือ
# 1. Path ไปของไฟล์รูป
# 2. ขนาดของวัถุที่ใช้อ้างอิง
ap=argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
# ap.add_argument("-c", "--color", required=True,
#                 help="color of background (red green or blue)")
ap.add_argument("-w", "--width", type=float, required=True,
                help="width of the left-most object in the image (in millimeter)")
args=vars(ap.parse_args())

# นำเข้ารูปภาพจาก Path ที่ใส่มา
image=cv2.imread(args["image"])
image=ResizeWithAspectRatio(image, width=1080)
hsv=cv2.cvtColor(cv2.GaussianBlur(image, (7, 7), 0), cv2.COLOR_BGR2HSV)
# hsv=cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)	
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 10, 200)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)


mask_r=get_background_mask(hsv, "red")
mask_g=get_background_mask(hsv, "green")
mask_b=get_background_mask(hsv, "blue")

# cv2.imshow("mask_r", mask_r)
# cv2.imshow("mask_g", mask_g)
# cv2.imshow("mask_b", mask_b)

# cv2.Canny => การตีกรอบให้กับภาพ
edged_r=cv2.Canny(mask_r, 10, 100)
# dilate => ขยายเส้นขอบให้ใหญ่ขึ้น
edged_r=cv2.dilate(edged_r, None, iterations=1)
# dilate => ลบ Noise สีขาวออกจากรูปภาพ
edged_r=cv2.erode(edged_r, None, iterations=1)

edged_g=cv2.Canny(mask_g, 10, 100)
edged_g=cv2.dilate(edged_g, None, iterations=1)
edged_g=cv2.erode(edged_g, None, iterations=1)

edged_b=cv2.Canny(mask_b, 10, 100)
edged_b=cv2.dilate(edged_b, None, iterations=1)
edged_b=cv2.erode(edged_b, None, iterations=1)

dst1 = cv2.addWeighted(edged_r, 1, edged_g, 1, 0)
dst2 = cv2.addWeighted(dst1, 1, edged_b, 1, 0)
dst3 = cv2.addWeighted(dst2, 1, edged, 1, 0)

# cv2.imshow("dst1", dst1)
# cv2.imshow("dst2", dst2)
# cv2.imshow("dst3", dst3)
# cv2.imshow("edged", edged)
# cv2.waitKey(0)
# exit()
# writeImage(edged,"bg_green","eraser") 


# ค้นหารูปร่างของวัตถุ
# cv2.findContours(รุูปภาพ,ดึงเส้นขอบของวัตถุ,การประมาณการรูปร่างของวัตถุ)
cnts=cv2.findContours(dst3.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts=imutils.grab_contours(cnts)

# เรียงลำดับเส้นขอบของวัตถุ เพื่อสามารถเข้าถึงวัตถุอ้างอิงได้ และสามารถ
# หาค่าของ pixelsPerMetric จากวัตถุอ้างอิงดังกล่าว
(cnts, _)=contours.sort_contours(cnts)

# กำหนดให้ pixelsPerMetric เป็น None ซึ่งใช้ในการคำนวณอัตราส่วนของรูปภาพอ้างอิง
# เพื่อใช้ค้นหาความยาวด้านของวัตถุเป้าหมาย
pixelsPerMetric=None

origin=image.copy()  # ลบลบบรรทัดนี้ออกถ้าต้องการให้แสดงผลลัพธ์ต่อ 1 obj

# loop เพื่อคำนวณความยาวด้านของแต่ละรูปร่างที่ค้นหาได้จากรูปภาพ
for c in cnts:
    # cv2.contourArea => คืนค่าพื้นที่ของรูปร่างที่ c มีหน่วยคือ pixel^2
    # ถ้าพื้นที่มีขนาดที่เล็กเกินไป จะข้ามไปยังรูปร่างถัดไป
    # (cv2.contourArea(c)/args["width"]*args["width"]) คือการแปลงหน่วยจาก pixel^2 เป็น MM^2
    if (cv2.contourArea(c) < 300):
        continue

    # คำนวณหาเส้นรอบรูปรางของวัตถุที่มีความเอียง
    # origin = image.copy() # นำ comment ออกถ้าต้องการให้แสดงผลลัพธ์ต่อ 1 obj
    box=cv2.minAreaRect(c)
    box=cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    box=np.array(box, dtype="int")

    # วางเส้นรอบรูปของวัตถุโดยมีลำดับคือ บนซ้าย บนขวา ล่างซ้าย ล่างขวา
    box=perspective.order_points(box)
    cv2.drawContours(origin, [box.astype("int")], -1, (0, 255, 0), 2)

    # วาดรูปจุด (point) ในแต่ละมุมของเส้นรอบรูป
    for (x, y) in box:
        cv2.circle(origin, (int(x), int(y)), 5, (0, 0, 255), -1)

    # นำจุดทั้ง 4 จุด เก็บไว้ใน (tl, tr, br, bl) เพื่อคำนวณหาจุดกึ่งกลาง
    # ระหว่างจุดด้านบน (บนซ้าย บนขวา) และระหว่างจุดด้านล่าง (่ล่างซ้าน ล่างขวา)
    (tl, tr, br, bl)=box
    (tltrX, tltrY)=midpoint(tl, tr)
    (blbrX, blbrY)=midpoint(bl, br)

    # คำนวณจุดกึ่งกลางระหว่าง บนซ้าย ล่างซ้าย
    # และ บนขวา ล่างขวา
    (tlblX, tlblY)=midpoint(tl, bl)
    (trbrX, trbrY)=midpoint(tr, br)

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
    dA=dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    dB=dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

    # กรณีที่ไม่มีการกำหนดค่า pixelsPerMetric จะนำค่าที่ได้จากพารามิเตอร์มาคำนวณหาอัตราส่วน
    if pixelsPerMetric is None:
        pixelsPerMetric=dB / args["width"]

    # คำนวณหาความยาวด้านของวัตถุ
    dimA=dA / pixelsPerMetric
    dimB=dB / pixelsPerMetric

    # แสดงตัวเลขจากการคำนวณ
    cv2.putText(origin, "{:.4f}mm".format(dimA),
                (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 255, 255), 2)
    cv2.putText(origin, "{:.4f}mm".format(dimB),
                (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                0.65, (255, 255, 255), 2)

    # origin = ResizeWithAspectRatio(origin, width=1080)

    # show the output image
cv2.imshow("Image", origin)
cv2.waitKey(0)
# if (cv2.waitKey(0) & 0xFF) == 27:
#     break
