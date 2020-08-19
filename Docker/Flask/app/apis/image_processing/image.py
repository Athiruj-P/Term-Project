import cv2
class Image:
    def __init__(self, width=0 , height=0 ,image=cv2,measurement_unit=0):
        self.width = width
        self.height = height
        self.image = image
        self.measurement_unit = measurement_unit