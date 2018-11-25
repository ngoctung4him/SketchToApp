"""
Created on Wed May  2 14:06:21 2018

@author: sxm6202xx
"""
import numpy as np
import cv2
def order_points(pts,maxVal):
    
    rect = np.zeros((4, 2), dtype = "float32")
    rect=[[0,0],[0,0],[0,0],[0,0]]
    maxSum = 0 
    maxDif1 = 0
    maxDif2 = 0
    minSum = maxVal
    for pt in pts:
        sumVal = pt[0][0] + pt[0][1]
        difVal1 = pt[0][1] - pt[0][0]
        difVal2 = pt[0][0] - pt[0][1]
            
        if(sumVal<minSum):
            minSum = sumVal
            rect[0] = [pt[0][0], pt[0][1]] 
        
        if(sumVal>maxSum):
            maxSum = sumVal
            rect[1] = [pt[0][0], pt[0][1]] 
        
        if(difVal1>maxDif1):
            maxDif1 = difVal1
            rect[2] = [pt[0][0], pt[0][1]] 
        
        if(difVal2>maxDif2):
            maxDif2 = difVal2
            rect[3] = [pt[0][0], pt[0][1]] 
    return rect


def transform_Single(contourInfo, orgPic, orgPic_gray):
    
    maxVal = orgPic.shape[0] + orgPic.shape[1]
    rect = order_points(contourInfo.rootViewContour,maxVal)
    maxWidth = contourInfo.rootView.width
    maxHeight = contourInfo.rootView.height
    src = np.array([rect[0],rect[3],rect[1],rect[2]], dtype = "float32")    
    dst = np.array([[0, 0],[maxWidth - 1, 0],[maxWidth - 1, maxHeight - 1],[0, maxHeight - 1]], dtype = "float32")
 
	# compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(src, dst)
    wrapOrg = cv2.warpPerspective(orgPic, M, (maxWidth, maxHeight))
    wrapOrg_gray = cv2.warpPerspective(orgPic_gray, M, (maxWidth, maxHeight))
#    wrapthrPicd = cv2.warpPerspective(thrPic, M, (maxWidth, maxHeight))
#    wrapOrg = cv2.resize(wrapOrg,(1200,768), interpolation = cv2.INTER_CUBIC)
#    wrapthrPicd = cv2.resize(wrapthrPicd,(1200,768), interpolation = cv2.INTER_CUBIC)

    return wrapOrg,wrapOrg_gray

def transform(contourInfo, orgPic, thrPic):
    
    maxVal = orgPic.shape[0] + orgPic.shape[1]
    rect = order_points(contourInfo.rootViewContour,maxVal)
    maxWidth = contourInfo.rootView.width
    maxHeight = contourInfo.rootView.height
    src = np.array([rect[0],rect[3],rect[1],rect[2]], dtype = "float32")    
    dst = np.array([[0, 0],[maxWidth - 1, 0],[maxWidth - 1, maxHeight - 1],[0, maxHeight - 1]], dtype = "float32")
 
	# compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(src, dst)
    wrapOrg = cv2.warpPerspective(orgPic, M, (maxWidth, maxHeight))
    wrapthrPicd = cv2.warpPerspective(thrPic, M, (maxWidth, maxHeight))
#    wrapOrg = cv2.resize(wrapOrg,(1200,768), interpolation = cv2.INTER_CUBIC)
#    wrapthrPicd = cv2.resize(wrapthrPicd,(1200,768), interpolation = cv2.INTER_CUBIC)

    return (wrapOrg,wrapthrPicd)
    
    


#include "opencv2/imgproc.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"
#include <iostream>

