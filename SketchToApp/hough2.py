# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 10:00:08 2018

@author: vo00timo
"""

import cv2
import numpy as np
import math
#import isect_segments_bentley_ottmann.poly_point_isect as bot

def Distance(aLine):
    
    return math.sqrt(math.pow((aLine[0][2]-aLine[0][0]),2) + math.pow((aLine[0][3]-aLine[0][1]),2) )
    

img = cv2.imread('Capture7.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

kernel_size = 5
blur_gray = cv2.GaussianBlur(gray,(kernel_size, kernel_size),0)

low_threshold = 50
high_threshold = 150
edges = cv2.Canny(blur_gray, low_threshold, high_threshold)

rho = 1  # distance resolution in pixels of the Hough grid
theta = np.pi / 180  # angular resolution in radians of the Hough grid
threshold = 15  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 10  # minimum number of pixels making up a line
max_line_gap = 10  # maximum gap in pixels between connectable line segments
line_image = np.copy(img) * 0  # creating a blank to draw lines on

# Run Hough on edge detected image
# Output "lines" is an array containing endpoints of detected line segments
lines = cv2.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                    min_line_length, max_line_gap)
#print(lines)
points=[]
for line in lines:
    #print(Distance(line))
    if (Distance(line)<25):
         for x1, y1, x2, y2 in line:
            points.append(((x1 + 0.0, y1 + 0.0), (x2 + 0.0, y2 + 0.0)))
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
print(lines_edges.shape)
cv2.imwrite('line_parking.png', lines_edges)
    #print (item.tolist())
    #break;
#points = []
#for line in lines:
#    for x1, y1, x2, y2 in line:
#        points.append(((x1 + 0.0, y1 + 0.0), (x2 + 0.0, y2 + 0.0)))
#        cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)
#
#lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
##print(lines_edges.shape)
#cv2.imwrite('line_parking.png', lines_edges)