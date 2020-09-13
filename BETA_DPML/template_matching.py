import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv.INTER_AREA):
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

    return cv.resize(image, dim, interpolation=inter)

img_rgb = cv.imread("C:/Users/First-AP/Desktop/test_img/IMG_8112.JPG")
img_rgb = ResizeWithAspectRatio(img_rgb,width=900)
img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
template = cv.imread('C:/Users/First-AP/Desktop/test_img/template.png',0)
template = ResizeWithAspectRatio(template,width=300)
w, h = template.shape[::-1]
res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
cv.imshow("Image", img_rgb)
cv.waitKey(0)