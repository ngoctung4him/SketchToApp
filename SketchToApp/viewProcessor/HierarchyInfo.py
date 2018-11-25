# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 22:00:11 2017

@author: soumi
"""
import RectUtils.RectUtil as RectUtil
from RectUtils.RectView import RectView
import RectUtils.RectView as RectViewType
from RectUtils.Rect import Rect
import numpy as np
from Utils  import ImageUtil
from Utils import ColorUtil
import cv2
import copy
from ocr.OCRTextWrapper import OCRTextWrapper
import ocr.TextProcessorUtil as TextProcessorUtil
from Utils.ColorUtil import CColor, ColorWrapper
import Utils.ColorUtil as ColorUtil
from ocr.TextInfo import TextInfo

class HierarchyInfo:
    rootView = RectView()
    biMapViewRect ={}

class OrderViewWraper:
    otherView= None

    def __init__(self,view, ranking):
        self.view = view
        self.ranking = ranking

    def getRank(self):
        if (self.otherView == None):
            return self.ranking
        else:
            return self.otherView.getRank() + 0.1
            

