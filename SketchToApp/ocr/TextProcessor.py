# -*- coding: utf-8 -*-
"""
Created on Tue Oct 24 22:24:31 2017

@author: soumi
"""

import copy
from Utils.ColorUtil import CColor, ColorWrapper
from RectUtils import RectUtil
from RectUtils.Rect import Rect
from Utils import ColorUtil
from Utils import ImageUtil
from Rules.FilterRuleManager import *
from ocr  import AzureVision
from functools import cmp_to_key
from ocr.OCRTextWrapper import OCRTextWrapper
from Utils import Constants
from Rules.FilterRuleManager import FilterRuleManager
from ocr.TextInfo import TextInfo
from ocr.VisionAPI import VisionApi

class TextProcessor :
    isDebugMode = False

    def __init__(self, image, biMapViewRect) :
        self.mImage = image
        self.mBiMapViewRect = biMapViewRect
#        self.mOcr = VisionApi()
        values = set([k for k in biMapViewRect])
        self.mViewBounds = []
        self.mViewBounds.extend(values)
        RectUtil.sortLeftRightTopBottom(self.mViewBounds)
        self.mViews = [k for k in biMapViewRect]
  

    def invalidWord(self,text):
        singleInvalidCharacters = [',','.','+','-','o',')','(','/','\\','|','~']
        if(len(text)==1):
            if text not in singleInvalidCharacters:
                return True
            else:
                return False
        return True


      
    def recalCulateOCR(self, ocrWrapper, validWords):
        validOcrs = []
        for validWord in validWords:
            indexOfX = int(((ocrWrapper.text.index(validWord)/ len(ocrWrapper.text))* ocrWrapper.width)+ ocrWrapper.x)
            width = int((len(validWord)/ len(ocrWrapper.text))* ocrWrapper.width)
            wrapper = OCRTextWrapper()
            wrapper.text = validWord
            wrapper.x = indexOfX
            wrapper.y = ocrWrapper.y
            wrapper.width = width
            wrapper.height = ocrWrapper.height
            
            validOcrs.append(wrapper) 
        return validOcrs


      # split into word and check if it a valid word and seperate with other words
    def getValidWords(self,visionResponses):
        blockVisionResponse =  []
        for visionResponse in visionResponses:
            splitWords = visionResponse.text.split()
            if(len(splitWords) != 1):
                validSplitWord = []
                currenWord= ""
                for i in range(len(splitWords)):
                    if(self.invalidWord(splitWords[i])):
                        currenWord += splitWords[i]                   
                    else:
                        validSplitWord.append(currenWord)
                        currenWord =""
                    if(i!=len(splitWords)-1):
                        currenWord +=" "
                validSplitWord.append(currenWord)
                blockVisionResponse.extend(self.recalCulateOCR(visionResponse,validSplitWord))
            else:
                blockVisionResponse.append(visionResponse)
        return blockVisionResponse

          
        

    def processText(self):
#        visionresponse= self.get_response()
        ocrResponse = self.extract_vertices_azure()
        visionresponse = self.getValidWords(ocrResponse) 
        width = 0
        height = 0
        copyImage = copy.deepcopy(self.mImage)
        
        if len(copyImage.shape) == 2 :
            height, width = copyImage.shape
        else:
            height, width,channels = copyImage.shape

        
        acceptedvisionresponses = []
        ruleManager = FilterRuleManager(visionresponse, self.mViews)
        invalidTexts = []
        
        for ocrTextWrapper in visionresponse:            
            textValidator = ruleManager.acceptOCRRules(ocrTextWrapper)
            if textValidator != None and not textValidator.valid:
                invalidTexts.append(ocrTextWrapper)
            else :
                acceptedvisionresponses.append(ocrTextWrapper)


        validTexts = []
        validTexts.extend(acceptedvisionresponses) 
        validTexts = [x for x in validTexts if x not in invalidTexts]
        

        for ocrTextWrapper in validTexts:            
            print(ocrTextWrapper.text)
        textInfo = TextInfo()
        textInfo.lines = validTexts

        return textInfo
    
    def getValidLines(self,lines):
        validLines = []
        for line in lines:
            allWords = line.words
            RectUtil.sortleftRight(allWords)
            firstWord = allWords[0]
            currentLine = OCRTextWrapper()
            currentLine.words.append(firstWord)
            for i in range(1,len(allWords)):
                currentWord = allWords[i]
                if(currentWord.x < firstWord.x + firstWord.width+ firstWord.height):
                    currentLine.words.append(currentWord)
                else:
                    validLines.append(currentLine)
                    firstWord = allWords[i]
                    currentLine = OCRTextWrapper()
                    currentLine.words.append(firstWord)
        
        validLines.append(currentLine)
            
            
        
    
    def reCalculateBoundBaseOnWordList(self, validline):
        if (len(self.words) == 0):
            return validline        
        unionRect = self.words[0]
        unionRect.text = self.words[0].text
        for i in range(1,len(self.words)):
            word = self.words[i]
            unionRect = RectUtil.union(unionRect, word)
            unionRect.text = " " +self.words[0].text
        return unionRect
       
    
    def getWordsInLine(self, textWrappers):
        RectUtil.sortTopBottom(textWrappers)
        validLines = []        
        firstWord = textWrappers[0]
        currentLine = OCRTextWrapper()
        currentLine.words.append(firstWord)
        for i in range(1,len(textWrappers)):
            currentWord = textWrappers[i]
            if(currentWord.y < firstWord.y + firstWord.height/2):
                currentLine.words.append(currentWord)
            else:
                validLines.append(currentLine)
                firstWord = textWrappers[i]
                currentLine = OCRTextWrapper()
                currentLine.words.append(firstWord)
        
        validLines.append(currentLine)

        
        return validLines
                        
        

    def getNotHorizontalAlignmentWords(self, words) :
        if len(words) <= 1 :
            return []

        invalidWords = []
        textWrappers = []
        textWrappers.extend(words)
        first = textWrappers[0].bound()
        for i in range(1,len(words)):
            # Assume that the first item is correct
            current = textWrappers[i].bound();
            if (first.y + first.height <= current.y) :
                invalidWords.append(textWrappers[i])

        return invalidWords
    
    def validateWordWithAllViews(self, tv, ocrTextWrapper) :
        ocrBound = ocrTextWrapper.bound();
        for view in self.mViews :
            # woa this word is big and have a lot of children, not good
            # this may okay with url or special texts
            if (RectUtil.contains(ocrBound, view.bound())and len(view.getChildren()) > 0) :
                tv.scalar = ColorUtil.getScalar(CColor.Cyan)
                tv.valid = False
                tv.log = "This word is big and have a lot of children";
                return

            if RectUtil.contains(ocrBound, view.bound()) and len(view.getChildren()) == 0 :
                # make sure this view did not intersect with other view,
                # include is accepted in this case
                hasIntersection = False
                for otherView in self.mViews:
                    if otherView != view and RectUtil.intersectsNotInclude(ocrBound,otherView.bound()) :
                        hasIntersection = True
                        break                    
                
                if (not hasIntersection) :
                    if (RectUtil.dimesionSmallerThan(view, ocrTextWrapper, 0.8)) :
                        # this is wrong, ignore this word
                        tv.scalar = CColor.Black
                        tv.valid = False
                        tv.log = "The box may has the word is too small compare with the word itself"
                        return
                 
            if (self.areChildrenIsTooSmall(self.mDipCalculator, view) and RectUtil.contains(view.bound(), ocrBound)) :
                if (RectUtil.dimesionSmallerThan(ocrTextWrapper, view, 0.8)) :
                    # this is wrong, ignore this word
                    tv.scalar = CColor.Pink
                    tv.valid = False
                    tv.log = "The box may has the word is too big compare to the word, and there is only one word in here. This view may also have other view but it so tiny"
                    return
                
    
    def extract_vertices_azure(self):
        """Returns all the text in text annotations as a single string"""
        listOcrData = []
        polygons= AzureVision.getTextfromNA(self.mImage)
        for polygon in polygons:
#            print(polygon)
            wrapper = OCRTextWrapper()
            wrapper.text = polygon[1]
            print(wrapper.text)
            posX = polygon[0][0]
            if(polygon[0][0]>polygon[0][6]):
                posX = polygon[0][6]
                
            posY = polygon[0][1]
            if(polygon[0][1]>polygon[0][3]):
                posY = polygon[0][3]
                
            tailX = polygon[0][2]
            if(polygon[0][2]<polygon[0][4]):
                tailX = polygon[0][4]
                
            tailY = polygon[0][5]
            if(polygon[0][5]<polygon[0][7]):
                tailY = polygon[0][7]
                
            wrapper.x = posX
            wrapper.y = posY
            wrapper.width = tailX - posX
            wrapper.height = tailY - posY
            listOcrData.append(wrapper)
        return listOcrData
    
    
    def extract_vertices_azure_crop(self,mImage):
        """Returns all the text in text annotations as a single string"""
        wrapper = OCRTextWrapper()
        polygons= AzureVision.getTextfromNA(mImage)
        height_factor = self.mImage.shape[1]/768
        width_factor =  self.mImage.shape[0]/1200
        
        for polygon in polygons:
            wrapper = OCRTextWrapper()
            wrapper.text = polygon[1]
            posX = polygon[0][0]*width_factor
            if(polygon[0][0]>polygon[0][6]):
                posX = polygon[0][6]*width_factor
                
            posY = polygon[0][1]*height_factor
            if(polygon[0][1]>polygon[0][3]):
                posY = polygon[0][3]*height_factor
                
            tailX = polygon[0][2]*width_factor
            if(polygon[0][2]<polygon[0][4]):
                tailX = polygon[0][4]*width_factor
                
            tailY = polygon[0][5]*height_factor
            if(polygon[0][5]<polygon[0][7]):
                tailY = polygon[0][7]*height_factor
                
            wrapper.x = posX
            wrapper.y = posY
            wrapper.width = tailX - posX
            wrapper.height = tailY - posY
            print(wrapper.x)
            print(wrapper.y)
            print(wrapper.width)
            print(wrapper.height)
        return wrapper
    
    


