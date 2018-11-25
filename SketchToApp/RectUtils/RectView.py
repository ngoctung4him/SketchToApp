# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 17:20:53 2017

@author: soumi
"""

from RectUtils.Rect import Rect
import RectUtils.RectUtil as RectUtil
from Utils import FileMetadata
import RectUtils.RectViewUtil as RectViewTypes
from RectUtils.RectViewUtil import ListInfo, ListItemInfo, ListItemMetadata, ListItemType, ListMetadataRoot,TextInfo 



class RectView(Rect):

    def __init__(self, x=0 ,y=0 , width=0, height=0,contour=None):
        super().__init__(x,y,width,height)
        self.contour = contour
        self.mChildren = []
		#mTextWithLocations = new ArrayList<OCRTextWrapper>();
#        self.mImageInfo = ImageInfo()
        self.mListInfo = ListInfo();
        self.mTextInfo = TextInfo()
        self.mType = RectViewTypes.VIEW_TYPE_DEFAULT
        self.mColor=  None
        self.mAlpha=0.0
        self.mTextChildren = []
        self.mTextWithLocations = []
        self.mIconInfo = ""
        self.mListItemInfo = ListItemInfo()
        self.textColor =  0
        self.elementID = -1
        self.iconID = -1
    
    def __hash__(self):
        return hash((self.tl(), self.br(), self.mType))

    def __eq__(self, other):
        
        if other is None:
            return self.area() == 0
        elif type(other) != type(self):
                return False
        else:
            return (self.x, self.y,self.width, self.height)== (other.x, other.y,other.width, other.height) and (self.mType == other.mType)

    def __ne__(self, other):
        return not(self.__eq__(other))


    def includes(self,bound):
        return RectUtil.contains(self.rect, bound)

    def hasText(self):
         return len(self.mTextWithLocations) > 0


    def getOverlapRatio(self):
        overlapRatio = 0.0
        for rawView in self.mChildren :
            overlapRatio += rawView.area()
        
        return overlapRatio / self.rect.area()
    
    def addAllChild(self,child):
        self.mChildren.extend(child)
    
    def addChild(self,rawView):
        self.mChildren.append(rawView)
        
#    def getChildren(self):
#        return self.mChildren
#    
#
#    def getTextChildren(self):
#        return self.mTextChildren


    def toString(self):
        textInfo = "Info: "
        if self.mType == self.VIEW_TYPE_TEXT:
            textInfo += "TEXT: " + self.mTextInfo.textWrapper.getText();
            
        elif self.mType ==  self.VIEW_TYPE_IMAGE:
            textInfo += "IMAGE: " + self.mImageInfo.drawableId + ", drawable_id: " + self.mImageInfo.drawableId;
			
        else:
            textInfo += "RECT: " + self.mTextWithLocations;
			
        return "Bound: " + self.bound() + ", Text Children: " + self.mTextChildren + ", " + self.textInfo

    def hasTextRecusive(self):
        if self.hasText():
            return True
        
        hasText = False
        
        for rectView in self.mChildren:
            hasText = rectView.hasTextRecusive()
            if (hasText):
                    return True
        return hasText

    def isIconButton(self):
        nonImageClass = [5, 6 ,13, 16, 14, 17, 19]
        if(self.iconID not in nonImageClass):
            return True
        else:
            return False
    
    
    def getIconName(self):
        className = ['addbutton','binbutton','camerabutton','chatbutton','checkbutton','radiobutton','chatbutton','homebutton'
                 ,'userimage','locationbutton','lovebutton','musicbutton','switch','searchbutton','settingbutton','sliders','starbutton'
                 ,'volumebutton','vsliders']
        return className[self.iconID-1]
    
    
    def getViewTypeForAtomicElement(self):
        
        viewTypes = [RectViewTypes.VIEW_TYPE_ICON,RectViewTypes.VIEW_TYPE_ICON,RectViewTypes.VIEW_TYPE_ICON,RectViewTypes.VIEW_TYPE_ICON,
                     RectViewTypes.VIEW_TYPE_CHECK_BOX,RectViewTypes.VIEW_TYPE_RADIO_BUTTON,RectViewTypes.VIEW_TYPE_ICON,RectViewTypes.VIEW_TYPE_ICON,
                     RectViewTypes.VIEW_TYPE_ICON,RectViewTypes.VIEW_TYPE_ICON,RectViewTypes.VIEW_TYPE_ICON,RectViewTypes.VIEW_TYPE_ICON,
                     RectViewTypes.VIEW_TYPE_SWITCH,RectViewTypes.VIEW_TYPE_SEARCH,RectViewTypes.VIEW_TYPE_ICON,RectViewTypes.VIEW_TYPE_SEEK,
                     RectViewTypes.VIEW_TYPE_RATING,RectViewTypes.VIEW_TYPE_ICON,RectViewTypes.VIEW_TYPE_VIR_SEEK]
                     
        return viewTypes[self.iconID-1]
    
    def getElementID(self):
       return "element" + str(self.elementID)
