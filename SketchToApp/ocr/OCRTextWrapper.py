# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 12:43:56 2017

@author: soumi
"""
#from RectUtils.RectUtil import *
from RectUtils.Rect import Rect
from Utils import Constants
import RectUtils.RectUtil as RectUtil
from RectUtils.RectView import RectView



class OCRTextWrapper(RectView):
    def __init__(self, x=0 ,y=0 , width=0, height=0,text=None):
        super().__init__(x,y,width,height)
        self.text = ""
        self.words = []
    
        
    def isSameTextInfoAndSameLine(self, other):
        
        if (not(self.height == other.height and self.top == other.top or other.bottom <= self.bottom
                and other.top <= self.top or self.bottom <= other.bottom and self.top <= other.top
                or other.bottom <= self.bottom and self.top <= other.top or self.bottom <= other.bottom
                and other.top <= self.top)):
            return False
        
        spaceBetweenWord = int (Constants.SPACE_BETWEEN_WORD_RATIO * self.fontSize)

        #not to far from each other
        if (not(self.right + spaceBetweenWord > other.left and self.right < other.left or other.right+ spaceBetweenWord > self.left and other.right < self.left)):
            return False


        return True
    
    



        
    
    def getTextAttributes(self):
        properties = []
#        wrapper = self
        
        #TODO
#        properties.append((Constants.ATTRIBUTE_TEXT_SIZE, str(tesseractOCR.getPreferenceFontSize(wrapper, height))+ Constants.UNIT_DIP))
#        properties.append((Constants.ATTRIBUTE_TEXT_SIZE, str(self.fontSize)+ Constants.UNIT_DIP))

        buffer = "normal"
#        if self.bold :
#            buffer += "|bold"
#        
#        if (self.italic) :
#            buffer += "|italic"
#        
#        properties.append((Constants.ATTRIBUTE_TEXT_STYLE, buffer))
# 
#        buffer = ""
#        if self.serif :
#            buffer += "serif"
#        elif self.monospace :
#            buffer += "monospace"
#        else :
#            buffer += "normal"
        
        properties.append((Constants.ATTRIBUTE_TYPEFACE, buffer))
        return properties
