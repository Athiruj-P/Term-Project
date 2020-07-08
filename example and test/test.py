from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2


def nothing(x):
    pass


cv2.namedWindow("Track")
cv2.createTrackbar("LH", "Track", 0, 255, nothing)
cv2.createTrackbar("LS", "Track", 0, 255, nothing)
cv2.createTrackbar("LV", "Track", 0, 255, nothing)
cv2.createTrackbar("UH", "Track", 255, 255, nothing)
cv2.createTrackbar("US", "Track", 255, 255, nothing)
cv2.createTrackbar("UV", "Track", 255, 255, nothing)

while True:
    bg_green = cv2.imread('bg_green.jpg')  # queryImage
    # bg_blue = cv2.imread('bg_blue.jpg')  # queryImage
    # bg_red = cv2.imread('bg_red.jpg')  # queryImage
    hsv = cv2.cvtColor(bg_green, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (7, 7), 0)
    lh = cv2.getTrackbarPos("LH", "Track")
    ls = cv2.getTrackbarPos("LS", "Track")
    lv = cv2.getTrackbarPos("LV", "Track")

    uh = cv2.getTrackbarPos("UH", "Track")
    us = cv2.getTrackbarPos("US", "Track")
    uv = cv2.getTrackbarPos("UV", "Track")

    l_green = np.array([lh, ls, lv])
    u_green = np.array([uh, us, uv])

    mask = cv2.inRange(hsv, l_green, u_green)
    res = cv2.bitwise_and(bg_green, bg_green, mask=mask)

    cv2.imshow('bg_green', bg_green)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindow()
# cv2.imshow("bg_green_mask", mask)

# lower_blue = np.array([0, 0, 100])
# upper_blue = np.array([120, 100, 255])

# cv2.waitKey(0)

# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# gray = cv2.GaussianBlur(gray, (7, 7), 0)
