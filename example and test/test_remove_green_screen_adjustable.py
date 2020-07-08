import cv2
import numpy as np

video = cv2.VideoCapture(0)
image = cv2.imread("10B_coin.jpg")

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
    ret, frame = video.read()
    frame = cv2.resize(frame, (640, 480))
    image = cv2.resize(image, (640, 480))
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # upper_green = np.array([255, 255, 255])
    # lower_green = np.array([58, 176, 204])
    lh = cv2.getTrackbarPos("LH", "Track")
    ls = cv2.getTrackbarPos("LS", "Track")
    lv = cv2.getTrackbarPos("LV", "Track")

    uh = cv2.getTrackbarPos("UH", "Track")
    us = cv2.getTrackbarPos("US", "Track")
    uv = cv2.getTrackbarPos("UV", "Track")

    l_green = np.array([lh, ls, lv])
    u_green = np.array([uh, us, uv])

    mask = cv2.inRange(hsv, l_green, u_green)

    # mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # temp = frame - res
    # temp = np.where(temp == 0, image, temp)
    cv2.imshow("frame", frame)  
    cv2.imshow('mask', mask)
    # cv2.imshow("mask", temp)
    cv2.imshow('res', res)

    if (cv2.waitKey(1) & 0xFF) == 27:
        break

video.release()
cv2.destroyAllWindows()
