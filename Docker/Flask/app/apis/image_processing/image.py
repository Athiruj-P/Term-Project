# image
# Description : คลาสเก็บข้อมูลของรูปภาพ
# Author : Athiruj Poositaporn
import cv2
class Image:
    def __init__(self ,image=cv2,measurement_unit=0):
        self.image = image
        self.measurement_unit = measurement_unit