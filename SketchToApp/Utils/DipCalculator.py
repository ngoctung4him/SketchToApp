# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 00:08:24 2017

@author: soumi
"""
from Utils import Constants

# Calculate DIP from image property and phone resolution





class DipCalculator:
    
    def __init__(self, rgbaImage, profile):
            
        self.mWidthPx = 0
        self.mHeightPx = 0
    
        if len(rgbaImage.shape) == 2 :
            self.mHeightPx, self.mWidthPx = rgbaImage.shape
        else:
            self.mHeightPx, self.mWidthPx,channels = rgbaImage.shape
        
#        standardScreenWidthDpi = profile.mDpWidth
#        standardScreenHeightDpi = profile.mDpHeight
        standardScreenWidthDpi = 400
        standardScreenHeightDpi = 600
    
        
##        if Environment.getValue(Environment.KEY_WITH_TITLE_BAR) == False:
##            standardScreenHeightDpi += profile.mDpTitleBarHeight
#
#        scaleType = int(Environment.getValue(Environment.KEY_SCALE_TYPE))
#
#        if scaleType== 3: 
#            self.mWidthDpr = profile.mWidth / standardScreenWidthDpi
#            # We just need the same dpr here, regardless of dpr of height,
#            # because we don't want
#            # the height of the output to scale to the screen size
#            self.mHeightDpr = self.mWidthDpr
#
#        elif scaleType== 1: 
#             ratioWidth = self.mWidthPx / standardScreenWidthDpi
#             ratioHeight = self.mHeightPx / standardScreenHeightDpi
#            
#             self.mWidthDpr = max(ratioWidth, ratioHeight)
#             self.mHeightDpr = self.mWidthDpr
#        else:
        self.mWidthDpr = self.mWidthPx / standardScreenWidthDpi
        self.mHeightDpr = self.mHeightPx / standardScreenHeightDpi
            

    def isViewToBeIgnoreInternal(self, width, height):
        dipHeight = self.pxToHeightDip(height)
        dipWidth = self.pxToWidthDip(width)
        return  (dipHeight < Constants.MIN_AREA_TO_IGNORE_RATIO_HEIGHT_DP) or (dipWidth < Constants.MIN_AREA_TO_IGNORE_RATIO_WIDTH_DP) or (dipHeight * dipWidth < Constants.MIN_AREA_TO_IGNORE_RATIO_HEIGHT_DP * Constants.MIN_AREA_TO_IGNORE_RATIO_WIDTH_DP)
    

    def isViewToBeIgnore(self, rectView):
        return self.isViewToBeIgnoreInternal(rectView.width, rectView.height)
    

    def pxToWidthDip(self,  px) :
        return px / self.mWidthDpr
    

    def pxToHeightDip(self,  px) :
        return px / self.mHeightDpr
    

    def dipToHeightPx(self,  height) :
        return height * self.mHeightDpr
    

    def dipToWidthPx(self,  dip) :
        return dip * self.mWidthDpr
    

    def pxToFontDip(self,  px) :
        return px / self.mHeightDpr
    

