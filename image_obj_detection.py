import cv2
import matplotlib.pyplot as plt
import cvlib as _cvlib
 
from cvlib.object_detection import draw_bbox
image = cv2.imread('Photo/silom_street.jpg')
recbox, label, configuration = _cvlib.detect_common_objects(image)
output_image = draw_bbox(image, recbox, label, configuration)
plt.imshow(output_image)
plt.show()