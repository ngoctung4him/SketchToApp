# -*- coding: utf-8 -*-

import cv2
import numpy as np

img = cv2.imread('Capture7.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imwrite('Capture6_gray.jpg',gray)
edges = cv2.Canny(gray,50,250,apertureSize = 5)
cv2.imwrite('Capture6_edges.jpg',edges)
#minLineLength = 100
#maxLineGap = 1
#lines = cv2.HoughLinesP(edges,1,np.pi/180,400,minLineLength,maxLineGap)
#
#for item in lines:
#    
#    for x1,y1,x2,y2 in item:
#        cv2.line(img,(x1,y1),(x2,y2),(255,0,0),2)
#
#cv2.imwrite('Capture6_out.jpg',img)

lines = cv2.HoughLines(edges,1,np.pi/180,250)
for item in lines:
    
    for rho,theta in item:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
    
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),3)

cv2.imwrite('Capture6_out.jpg',img)