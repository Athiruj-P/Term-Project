# Python code to reading an image using OpenCV 
import numpy as np 
import cv2 
  
# You can give path to the 
# image as first argument 
img = cv2.imread('img.jpg', 0) 
  
# will show the image in a window 
cv2.imshow('image', img) 
k = cv2.waitKey(0) & 0xFF
  
# wait for ESC key to exit 
if k == 27:  
    cv2.destroyAllWindows() 
      
# wait for 's' key to save and exit 
elif k == ord('s'):  
    cv2.imwrite('create_img.png',img) 
    cv2.destroyAllWindows() 