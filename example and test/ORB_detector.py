from __future__ import print_function
import cv2 as cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Code for Feature Matching with FLANN tutorial.')
parser.add_argument('--input1', help='Path to input image 1.', default='box.png')
parser.add_argument('--input2', help='Path to input image 2.', default='box_in_scene.png')
args = parser.parse_args()

img1 = cv2.imread(cv2.samples.findFile(args.input1), cv2.IMREAD_GRAYSCALE)
img2 = cv2.imread(cv2.samples.findFile(args.input2), cv2.IMREAD_GRAYSCALE)

if img1 is None or img2 is None:
    print('Could not open or find the images!')
    exit(0)
 
# Initialize the ORB detector algorithm 
orb = cv2.ORB_create() 
   
# Now detect the keypoints and compute 
# the descriptors for the query image 
# and train image 
queryKeypoints, queryDescriptors = orb.detectAndCompute(img1,None) 
trainKeypoints, trainDescriptors = orb.detectAndCompute(img2,None) 
  
# Initialize the Matcher for matching 
# the keypoints and then match the 
# keypoints 
matcher = cv2.BFMatcher() 
matches = matcher.match(queryDescriptors,trainDescriptors) 
    
# draw the matches to the final image 
# containing both the images the drawMatches() 
# function takes both images and keypoints 
# and outputs the matched query image with 
# its train image 
final_img = cv2.drawMatches(img1, queryKeypoints,  
img2, trainKeypoints, matches[:20],None) 
   
final_img = cv2.resize(final_img, (1000,650)) 
  
# Show the final image 
cv2.imshow("Matches", final_img) 
cv2.waitKey(0) 