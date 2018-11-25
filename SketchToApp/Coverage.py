# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 23:06:00 2018

@author: vo00timo
"""
import cv2
import copy
import os
import numpy as np
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
            #print('('+str(starting_row)+','+str(starting_col)+') - ('+str(ending_row)+','+str(ending_col)+')')
            
            #cv2.imshow('crop'+str(i)+str(j), name) 
            cv2.imwrite('screen'+str(i-1)+str(j-1)+'.jpg',name)

if __name__ =="__main__":
    screen=np.full((3, 3), False)
    splitImage("Capture2.JPG")