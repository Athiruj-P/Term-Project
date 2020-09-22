# Object size measurement from video
# Description : โปรแกรมการวัดขนาดวัตถุจากภาพเคลื่อนไหว
# Create date : 07-July-2020 
# Auther : Athiruj Poositaporn

import cv2
import numpy as np
import imutils
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import glob
import pprint
import random

from cvlib.object_detection import draw_bbox

cap = cv2.VideoCapture(0)
show_live_video = True

while(show_live_video):
    # Capture frame-by-frame
    ret, image = cap.read()
    # image = cv2.imread(frame)
    # recbox, label, configuration = _cvlib.detect_common_objects(image)
    # output_image = draw_bbox(image, recbox, label, configuration)
    cv2.imshow("Image", output_image)
    if (cv2.waitKey(1) & 0xFF) == 27:
        break
        
cap.release()
cv2.destroyAllWindows()
# plt.imshow(output_image)
# plt.show()
