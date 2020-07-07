import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

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

origin_image01 = cv.imread('Photo/cocoa_puffs_brownie_crunch.jpg')
origin_image02 = cv.imread('Photo/products.png')

if origin_image01.shape[1] > 400:
    origin_image01 = ResizeWithAspectRatio(origin_image01,width = 400)

img1 = cv.cvtColor(origin_image01, cv.COLOR_BGR2GRAY)
img2 = cv.cvtColor(origin_image02, cv.COLOR_BGR2GRAY)



# Initiate SIFT detector
sift = cv.xfeatures2d.SIFT_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

# เลือก Algorithm เป็น KDTREE 
FLANN_INDEX_KDTREE = 1
# trees คือจำนวนการทำนายแบบขนานอยู่ระหว่าง ซึ่งมีค่าแนะนำที่ 1 - 16
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 10)
# checks คือจำนวนครั้งการท่อง (Traversals) ในแต่ละ tree 
# ยิ่งมีค่ามากจะมีความแม่นยำสูง แต่ใช้ทรัพยากรเครืองมากเช่นกัน
search_params = dict(checks=50)   # or pass empty dictionary
flann = cv.FlannBasedMatcher(index_params,search_params)
matches = flann.knnMatch(des1,des2,k=2)

# Need to draw only good matches, so create a mask
matchesMask = [[0,0] for i in range(len(matches))]

# ratio test as per Lowe's paper
for i,(m,n) in enumerate(matches):
    if m.distance < 0.7*n.distance:
        matchesMask[i]=[1,0]
draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (0,0,255),
                   matchesMask = matchesMask,
                   flags = cv.DrawMatchesFlags_DEFAULT)
img3 = cv.drawMatchesKnn(origin_image01,kp1,origin_image02,kp2,matches,None,**draw_params)
cv.imshow("Image", img3)
cv.waitKey(0)    
# plt.imshow(img3,),plt.show()