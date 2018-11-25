# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 19:54:10 2018

@author: soumi
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 16:29:44 2017

@author: soumi
"""
import numpy as np
from RectUtils.Rect import Rect
from RectUtils.RectView import RectView
import cv2
from RectUtils.Point import Point
import RectUtils.RectUtil as RectUtil
from viewProcessor.ContourAnalysis import ContourAnalysis
class CropWindow:
    
    def __init__(self,img):
        contourAnalysis = ContourAnalysis()
        contoursdata = contourAnalysis.findContoursWithCanny(img)
        contours = contoursdata['contours']
    
        points = []
        for i in range(len(contours)):
            (x1,y1,width,height)= cv2.boundingRect(contours[i])
            points.append(Point(x1,y1))
            points.append(Point(x1+width,y1+height))
            points.append(Point(x1+width,y1))
            points.append(Point(x1,y1+height))
        RectUtil.sortleftRight(points)
        self.leftX = points[0].x
        self.rightX = points[len(points)-1].x
        RectUtil.sortTopBottom(points)
        self.topY = points[0].y
        self.bottomY = points[len(points)-1].y
   
    def cropImg(self,img,threshold=2):
                return img[self.topY-threshold:self.bottomY+threshold, self.leftX-threshold:self.rightX+threshold]