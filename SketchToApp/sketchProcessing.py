# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 14:52:03 2018

@author: sxm6202xx
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 00:16:19 2017

@author: soumi
"""
from time import sleep
#import numpy as np
import cv2
from viewProcessor.Canny import Canny
from viewProcessor.ContourAnalysis import ContourAnalysis
from viewProcessor.ContourAnalysis import ContourInfo
from Utils.Project import Project
from viewProcessor.ViewHierarchyProcessor import ViewHierarchyProcessor
from Utils.Resolution import Resolution
from ocr.TextProcessor import TextProcessor
from Utils import Util
import copy
from Utils import XmlUtil
from Utils import Constants
from Utils.Profile import Profile
from Utils.Profile import DeviceDensity
from Utils.DipCalculator import DipCalculator
import os
from Utils import ImageUtil
from viewProcessor import Transform
from shutil import copyfile
from ocr import AzureVision
import numpy as np
from Screen import Screen2 as Scr
import math


def Distance(aLine):   
    return math.sqrt(math.pow((aLine[0][2]-aLine[0][0]),2) + math.pow((aLine[0][3]-aLine[0][1]),2) )

def RecognizeLines(fileLocation):
    img = cv2.imread(fileLocation)
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
    for line in lines:
        #print(Distance(line))
        if (Distance(line)<25):
             for x1, y1, x2, y2 in line:
                #points.append(((x1 + 0.0, y1 + 0.0), (x2 + 0.0, y2 + 0.0)))
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

    lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
    print(lines_edges.shape)
    cv2.imwrite('image_out.png', lines_edges)
    return lines    
    

def checkValidScreen(fileLocation):
    fileExitst = os.path.isfile(fileLocation)
    if(not fileExitst):
        return "Can't access the file"
    img_raw = cv2.imread(fileLocation)


    img_raw = cv2.fastNlMeansDenoising(img_raw,30.0, 7, 21)
    
    img_gray = copy.deepcopy(img_raw)
    
    if len(img_raw.shape) == 3 :
        img_gray  = cv2.cvtColor(img_raw, cv2.COLOR_BGR2GRAY)
    return AzureVision.getTextfromNA(img_gray)  


    
def generateProject(fileLocation):
    
    fileExitst = os.path.isfile(fileLocation)
    if(not fileExitst):
        return "Can't access the file"
    img_raw = cv2.imread(fileLocation)


    img_raw = cv2.fastNlMeansDenoising(img_raw,30.0, 7, 21)
    
    img_gray = copy.deepcopy(img_raw)
    
    if len(img_raw.shape) == 3 :
        img_gray  = cv2.cvtColor(img_raw, cv2.COLOR_BGR2GRAY)
    


    # dilate and find edges in the provided screenshot

    # This part is for finding window    
    adaptiveThresholding = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
    
    canny = Canny()
    
    dst_edge = canny.findEdge(adaptiveThresholding)  
    dst_edge_dilate = canny.addDilate(dst_edge)
#
#
    contourAnalysis = ContourAnalysis()
    contours = contourAnalysis.findContoursWithCanny(dst_edge_dilate)
    contoursOutput = contourAnalysis.analyzeforCrop(dst_edge_dilate, contours)    
    
    img_raw,img_gray = Transform.transform_Single(contoursOutput,img_raw,img_gray)

    # After Finding window process hierarchy
    
#    dst_denoised = cv2.fastNlMeansDenoising(img_draw,30.0, 7, 21)
    adaptiveThresholding = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)

    
    canny = Canny()
    
    dst_edge = canny.findEdge(adaptiveThresholding)  
    dst_edge_dilate = canny.addDilate(dst_edge)
#
#    ImageUtil.drawWindow("AdaptiveImage",dst_edge_dilate )
    contourAnalysis = ContourAnalysis()
    contours = contourAnalysis.findContoursWithCanny(dst_edge_dilate)
    contoursOutput = contourAnalysis.analyze(dst_edge_dilate, contours)
    
    hierarchyProcessor = ViewHierarchyProcessor(contoursOutput.rootView, adaptiveThresholding, canny)
    hierarchyInfo = hierarchyProcessor.process()
# use tesseract to detect the text 
    textProcessor = TextProcessor(img_gray, hierarchyInfo.biMapViewRect)
## process text to remove invalid texts    
    textInfo = textProcessor.processText()
## Add text boxes to hierarchy    
    hierarchyProcessor.addTextToHierarchy(textInfo,img_raw)


    #cv2.waitKey(0)

def splitImage(fileLocation):
    #fileLocation="sketchImage.jpg"
    fileExitst = os.path.isfile(fileLocation)
    if(not fileExitst):
        print("Can't access the file")
    # Reading image
    img_raw = cv2.imread(fileLocation)
    image = copy.deepcopy(img_raw)
    #cv2.imshow("Raw Image", image)
    cv2.waitKey(0)
    height, width = image.shape[:2]
    print (image.shape)
    # Let's get the starting pixel coordiantes (top left of cropped top)
 
    starting_row, starting_col = int(0), int(0)
    ending_row, ending_col = int(0), int(0)
    
    name=''
    for i in range(1,4): #row =3 if range is 3
        starting_row=ending_row
        ending_row=int(height* (i/3)) 
        ending_col= int(0)
        for j in range(1,4): #col =3
            
            starting_col= ending_col
            ending_col=int(width*(j/3)) 
            name='screen'+str(i-1)+str(j-1);
            name= image[starting_row:ending_row, starting_col:ending_col]
            screenid='screen'+str(i-1)+str(j-1)
            #print('('+str(starting_row)+','+str(starting_col)+') - ('+str(ending_row)+','+str(ending_col)+')')
            screen = Scr.Screen(screenid,starting_row,ending_row,starting_col,ending_col)
            screens.append(screen)
            #cv2.imshow('crop'+str(i)+str(j), name) 
            cv2.imwrite('screen'+str(i-1)+str(j-1)+'.jpg',name)
if __name__ =="__main__":
    screens=[]
    screen=np.full((3, 3), False)
    splitImage("Capture7.JPG")
    #generateProject("sketchImage.jpg")
    for i in range (0,3):
        for j in range (0,3):
            print('Processing '+ 'screen'+str(i)+str(j)+'.jpg')
            #generateProject('crop'+str(i)+str(j)+'.jpg')
            if (checkValidScreen('screen'+str(i)+str(j)+'.jpg')):
                screen[i][j]=True
            else:
                screen[i][j]=False
            #sleep(3)
    #create folder
    for i in range(0,3):
        for j in range(0,3):
            if(screen[i][j]):
                if not os.path.exists("column"+str(i)):
                    os.makedirs("column"+str(i))
                continue
    #recognize relationship on col
    for i in range (0,3):
        if(screen[0][i]) and (screen[1][i]):
            print ("screen0"+str(i)+" is parent of screen1"+str(i)+"\n")           
            copyfile('screen'+str(0)+str(i)+'.jpg','column'+str(i)+'/'+'screen'+str(0)+str(i)+'.jpg')
            copyfile('screen'+str(1)+str(i)+'.jpg','column'+str(i)+'/'+'screen'+str(1)+str(i)+'.jpg')
        if(screen[1][i]) and (screen[2][i]): 
            print ("screen1"+str(i)+" is parent of screen2"+str(i)+"\n")
            copyfile('screen'+str(1)+str(i)+'.jpg','column'+str(i)+'/'+'screen'+str(1)+str(i)+'.jpg')
            copyfile('screen'+str(2)+str(i)+'.jpg','column'+str(i)+'/'+'screen'+str(2)+str(i)+'.jpg')
    #recognize relationship on row
    if(screen[0][0]) and (screen[0][1]):
        print ("screen00 is peer of screen01")
    if(screen[0][1]) and (screen[0][2]):
        print ("screen01 is peer of screen02")
    
    for x in screens:
        x.displayScreen()
    lines=RecognizeLines('Capture7.JPG')    
  
    temp=[]

    img = cv2.imread('Capture7.JPG')
    
    line_image= np.copy(img) * 0 
    
    for line in lines:
        try:
            if (Distance(line)<25):
    #            print(Distance(line))
                 #print(line)
                 #for item in line: #x1 y1 x2 y2
                 for i in range(0, len(screens) -1):
                     for j in range(i+1, len(screens)):
    #                         if ((x1<=screens[i].x_end) and (y1<=screens[i].y_end) and (x2>=screens[j].x_start) and (y2>=screens[j].y_start)): 
                         if( (line[0][0]<=line[0][2]) and (line[0][1]<=line[0][3]) ):
                             if ((line[0][0]<=screens[i].x_end) and (line[0][1]<=screens[i].y_end) and (line[0][2]>=screens[j].x_start) and (line[0][3]>=screens[j].y_start)): 
                                 print(line)
                                 print(screens[i].name )
                                 screens[i].displayScreen()
                                 print(screens[j].name)
                                 screens[j].displayScreen()
                                 print("x1:"+str(line[0][0])+" y1:"+str(line[0][1])+" x2:"+str(line[0][2])+" y2:"+str(line[0][3]))
                                 
                                 #points.append(((x1 + 0.0, y1 + 0.0), (x2 + 0.0, y2 + 0.0)))
                                 cv2.line(line_image, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (0, 0, 255), 5)
                                 #HL_lines.append(line.tolist())
                                 temp.append((screens[i].name,screens[j].name))
                                 raise StopIteration 
        except  StopIteration: 
            pass           
    lines_edges = cv2.addWeighted(img, 0.8, line_image, 1, 0)
    #print(lines_edges.shape)
    cv2.imwrite('lines_edges.png', lines_edges)
             
    print(temp)



 


            
#    for i in range (0,3):#col
#        for j in range (0,3):#row
#            if (screen[j][i]):
#                file='screen'+str(j)+str(i)+'.jpg'
#                
#                #folder = os.path.join('column'+str(i), file)
#                folder='column'+str(i)+'/'+file
#                print('file '+file)
#                print('folder  '+folder)
#                copyfile(file,folder)
