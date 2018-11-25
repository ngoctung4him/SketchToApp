# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 01:29:46 2018

@author: soumi
"""
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
from viewProcessor.HierarchyInfo import HierarchyInfo
class ViewHierarchyProcessor:

    counter_value = 0

#    private boolean isDebugMode;

    def __init__(self, rootView, image, canny):
        self.widht = 0
        self.height = 0 
        self.height,self.width = image.shape
        self.totalArea = self.width*self.height
        self.mRootView = rootView
        self.mImage = image
        self.mCanny = canny
        self.mRectColorMapLog = {}
        self.hierarchyInfo = HierarchyInfo()
        self.startPointX = rootView.x
        self.startPointY = rootView.y
        
        
#    def ignoreView(self, rectView):
#
#        if(rectView.area()/self.totalArea <0.0001):
#            return False
#        if(rectView.width/self.width < 0.0001):
#            return False
#        if(rectView.height/self.height < 0.0001):
#            return False
#        return True

    def countViews(self,view):
        counter = 0
        self.countViewsInternal(view, counter)
        return counter

    def countViewsInternal(self,view, counter):
        counter = counter + 1
        children = view.getChildren()
        for rawView in children:
            self.countViewsInternal(rawView, counter)

    def delFullOverlapViews(self,view):
        rects = set()
        self.delFullOverlapViewsIntenal(view, rects)


    def delFullOverlapViewsIntenal(self,view, rects):
        rects.add(view)
        children = view.mChildren
        removeViews = []
        for rectView in children: 
            if (rectView in rects):
                removeViews.append(rectView);
            else:
                self.delFullOverlapViewsIntenal(rectView, rects);
        
        view.mChildren = [x for x in view.mChildren if x not in removeViews]
        
    def createMap(self, biMap, view):
        children = view.mChildren
        for rawView in children:
            biMap.append(rawView)
            self.createMap(biMap, rawView)
        
    def delOverlapViews(self,view):
        overlapIndexes = []

        children = view.mChildren
        for rawView in children:
            self.delOverlapViews(rawView)
            
        removingChildrenIndexes = [False] * len(children)
        for i in range(len(children)):
            rectView = children[i]
            for j in range(i+1, len(children)):
                otherRectView = children[j]
                if rectView != otherRectView:
                #Check if Intersects only
                    if (not RectUtil.contains(rectView, otherRectView) and not RectUtil.contains(otherRectView,rectView) and RectUtil.intersects(rectView,otherRectView)):
                        added = False
                        #Check if already in the overlapIndexes
                        for overlapIndex in overlapIndexes:
                            if (i in overlapIndex and j in overlapIndex ):
                                added = True
                                break
                            elif i in overlapIndex:
                                overlapIndex.append(j)
                                added = True
                                break
                            elif j in overlapIndex :
                                overlapIndex.append(i)
                                added = True
                                break
                            
                        # did not contain non of them them add two of them as a list within overlapIndexes 
                        if (not added):
                            rectViews = []
                            rectViews.append(i);
                            rectViews.append(j);
                            overlapIndexes.append(rectViews)
                        removingChildrenIndexes[i] = True
                        removingChildrenIndexes[j] = True;
        

        newRectViews = []

        # process overlap rect
        for rectViewIndexes in overlapIndexes:
            #find bound
            rectView = children[rectViewIndexes[0]]
            unionRect = rectView
            for i in range(1, len(rectViewIndexes)):
                r = children[rectViewIndexes[i]]
                unionRect = RectUtil.union(unionRect, r)
                
            newRectViewParent = RectView(unionRect.x, unionRect.y, unionRect.width, unionRect.height, None)
            for index in rectViewIndexes:
                newRectViewParent.addChild(children[index])
                
            removingChildrenIndexes[rectViewIndexes[0]] = False
            view.mChildren[rectViewIndexes[0]] =  newRectViewParent
            newRectViews.append(newRectViewParent)

        # now we make sure all other children of the parent inside union rect
        # go under this view too.
        for rectView in newRectViews:
            for i in range(len(removingChildrenIndexes)):
                rawView = children[i]
                if rawView != rectView and not removingChildrenIndexes[i]:
                    bound = children[i]
                    if (RectUtil.contains(rectView, bound)):
                        rectView.addChild(children[i])
                        removingChildrenIndexes[i] = True    
                
        # now update the children
        rawViews = []
        for i in range(len(removingChildrenIndexes)):
            if (not removingChildrenIndexes[i]):
                rawViews.append(children[i])

        view.mChildren = [x for x in children if x in rawViews]
                
        
    def process(self):
        self.basicProcess()

        self.mBiMapViewRect = []
        self.mBiMapViewRect.append(self.mRootView)

        self.createMap(self.mBiMapViewRect, self.mRootView)
        self.hierarchyInfo.rootView = self.mRootView
        self.hierarchyInfo.biMapViewRect = self.mBiMapViewRect

        return self.hierarchyInfo
    
    


    
    def ignoreView(self, rectView):
        # Check to see if it a part of the outer line
        if(rectView.x == 0 or rectView.y == 0 or rectView.x+rectView.width == self.width or rectView.x+rectView.height == self.height):
            return False
        if(rectView.area()/self.totalArea <0.0001):
            return False
        if(rectView.width/self.width < 0.01):
            return False
        if(rectView.height/self.height < 0.01):
            return False
        return True
                
    def adjustPoistionOfViews(self,rawView):
        rawView.x = rawView.x - self.startPointX
        rawView.y = rawView.y - self.startPointY
        children = rawView.mChildren
        removeViews = []
        for rectView in children:
            if(not self.ignoreView(rectView)):
                removeViews.append(rectView)
        
        rawView.mChildren = [x for x in rawView.mChildren if x not in removeViews]
        children = rawView.mChildren
        for rectView in children:
            self.adjustPoistionOfViews(rectView)
        
     
    
    def delOuterViews(self):
        children = self.mRootView.mChildren

        removeViews = []
        for rectView in children: 
            if (RectUtil.outliers(self.mRootView, rectView)):
                removeViews.append(rectView)

        
        self.mRootView.mChildren = [x for x in self.mRootView.mChildren if x not in removeViews]
       

    def basicProcess(self):
        #de-overlap views
        self.adjustPoistionOfViews(self.mRootView)
        self.delOuterViews()
#        self.delIgnoredViews()
#        self.delSmallViews(self.mRootView)
        self.delOverlapViews(self.mRootView)
#        self.writeHierarchyLog('after delOverlapViews')
     
        # we reorganize rectangles so that it has the right children
        # sometimes, one rectangle belong to one or the other
        self.reorganizeParentChildHierachyInternal(self.mRootView)
#        self.writeHierarchyLog('after reorganizeParentChildHierachyInternal')
        # de-full-overlap views
        self.delFullOverlapViews(self.mRootView)
#        colListmap={}
#        self.viewRectsList(self.mRootView,colListmap )
#        ImageUtil.logDrawBiMap(colListmap, "Pre Views", self.mImage)
#        
        

    
    def getRandomColor(self,view):
        color = ()
        if view in self.mRectColorMapLog:
            color = self.mRectColorMapLog[view]
        else:
            color = ColorUtil.randomColorInt()
            self.mRectColorMapLog[view]= color
            
        return color
		


    def getSmallestBoundRect( mRectBoundOfTexts, rect):
        smalledRect = Rect()
        # check if there is any rectangle contains with this rect
        for erRect in mRectBoundOfTexts:
            if (RectUtil.contains(erRect, rect)):
                if (smalledRect.area() == 0):
                    smalledRect = erRect
                elif (RectUtil.contains(smalledRect, erRect)):
                    smalledRect = erRect
            
        return smalledRect


    def reorganizeParentChildHierachyInternal(self, view):
        children = view.mChildren
        for childView in view.mChildren:
            self.reorganizeParentChildHierachyInternal(childView)
            
        hierachy = {}
        len(children)
       
        for i in range(len(children)):
            rectView = children[i]
            for j in range(i+1,len(children)):
                otherRectView = children[j]
                if (rectView != otherRectView):
                    if (RectUtil.contains(rectView, otherRectView)):
                        if j in hierachy and  i in hierachy[j] :
                            
                            #"This is wrong: " + j+ "  already is parents of " + i
                            pass
                        else :
                            childrenIndexes = []
                            
                            if (not i in hierachy) :
                                childrenIndexes = []
                                hierachy[i]= childrenIndexes
                            else:
                                childrenIndexes= hierachy[i]
                                
                            if (not j in  childrenIndexes) :
                                childrenIndexes.append(j)
            
                        
                    elif (RectUtil.contains(otherRectView, rectView)) :
                        if i in hierachy and j in hierachy[i] :
                            #"This is wrong: " + i+ "  already is parents of " + j);
                            pass
                        else :
                            childrenIndexes = []
                            
                            if (not j in hierachy) :
                                childrenIndexes = []
                                hierachy[j]= childrenIndexes
                            else:
                                childrenIndexes= hierachy[j]

                            if (not i in childrenIndexes) :
                                childrenIndexes.append(i);


        # remove view if it children claim that its contain that view
        optinmizedHierarchy={}
        parentIndexes = []
        for i in hierachy:
            childrenIndexes = hierachy[i]
            newChildrenIndexes = []
            for childrenIndex in childrenIndexes :
                # remove grandchildren belong to its children
                
                if childrenIndex in hierachy:
                    grandChildrenIndexes = hierachy[childrenIndex]
                    newChildrenIndexes = [x for x in newChildrenIndexes if x not in grandChildrenIndexes]
        
            optinmizedHierarchy[i]=newChildrenIndexes
            parentIndexes.append(i)

        # remove duplication of children        
        includedChildrenIndexes = set()
        for parentIndex in parentIndexes:
            childrenIndexes = optinmizedHierarchy[parentIndex]
            includedChildrenIndexes.update(childrenIndexes)
            childrenIndexes.clear()
            childrenIndexes.extend(includedChildrenIndexes)
        

        # now we reordering the hierarchy
        for i in optinmizedHierarchy:
            childrenIndexes = optinmizedHierarchy[i]
            childrenIndexes.sort()
            rawView = children[i]
            for childIndex in childrenIndexes :
                rawView.addChild(children[childIndex]);
            


        removingChildrenIndexes = [False]* len(children) 
        # all children value of this hierarchy map will be removed
        for i in optinmizedHierarchy:
            childrenIndexes = optinmizedHierarchy[i]
            for childIndex in childrenIndexes :
                removingChildrenIndexes[childrenIndex] = True
        

        # now we add parent according to order
        rawViews = []
        indexes = []
        for i in range(len(removingChildrenIndexes)):
            if (not removingChildrenIndexes[i]) :
                indexes.append(i);
            

        indexes.sort()
        for index in indexes :
            rawViews.append(children[index]);
        
        view.mChildren= [x for x in children if x in rawViews]
    


    def reorganizeOrder(self, view) :
        children = view.getChildren()
        orderViewWrapers = {}
        for childView in children:
            orderViewWraper =  OrderViewWraper(childView, children.index(childView))
            orderViewWrapers[childView]= orderViewWraper
    

        for  childView in children :
            for  otherChildView in children :
                # we want compare reference here!
                # check if we need to move the rectangle to lower level
                if (otherChildView != childView) :
                    childBound = childView
                    otherChildBound = otherChildView
                    if (RectUtil.intersects(childBound, otherChildBound)) :
                        otherGrandChildren = otherChildView.getChildren()
                        # this child did not overlap any children of the
                        # other child overlap
                        overlap = False
                        for rawView in otherGrandChildren:
                            if (RectUtil.intersects(childBound, rawView)) :
                                overlap = True
                                break
                            
                        if (not overlap and children.index(childView) < children.index(otherChildView)) :
                            orderViewWraper = orderViewWrapers[childView]
                            otherOrderViewWraper = orderViewWrapers[otherChildView]
                            orderViewWraper.otherView = otherOrderViewWraper

        
        sortedOrderViewWrapers = orderViewWrapers.values()
        sortedOrderViewWrapers.sort(self.OrderViewWrapers)
        children = []
        for orderViewWraper in sortedOrderViewWrapers :
            children.append(orderViewWraper.view)
        

    def OrderViewWrapers(self, a,b):
        return a.getRank() > b.getRank()    

    def addTextToHierarchy(self, textInfo, image_draw):
#        colListmap = {}
#        colListmap[ColorWrapper(ColorUtil.cColortoInt(CColor.Red), 1)] = textInfo.lines
#        if(isDebugMode)
#        ImageUtil.logDrawMap(colListmap, "addTextToHierarchy_before_blocks", self.mImage, True)

        blocks=[]
        blocks.extend(textInfo.lines)
            
        self.addTextToHierarchyInternal(self.hierarchyInfo.rootView, blocks)
        self.getAtomicElements()
        colListmap={}
        self.viewRectsList(colListmap )
        
        #ImageUtil.logDrawBiMap(colListmap, "Different Views", image_draw)
#        

   
    def getTextAndRemove(self,viewBound, blocks) :
        childTexts = []
        for ocrTextWrapper in blocks:
            bound = ocrTextWrapper
            if (RectUtil.contains(viewBound, bound)) :
                childTexts.append(ocrTextWrapper)
        
        blocks = [x for x in blocks if x not in childTexts]
        return childTexts    
    
    def getAtomicElements(self):
        self.getAtomicElementsInternal(self.hierarchyInfo.rootView)

    def getAtomicElementsInternal(self,view):
        children = view.mChildren
        for childView in children:
            self.getAtomicElementsInternal(childView)
        
        if (not view.hasTextRecusive() and view != self.mRootView):
            view.mChildren = []
            
    def viewRectsList(self,colListmap):
        self.viewRectsListInternal(self.hierarchyInfo.rootView,colListmap)

    def viewRectsListInternal(self,view,colListmap):
        children = view.mChildren
        for childView in children:
            self.viewRectsListInternal(childView,colListmap)
        
        if (view.hasTextRecusive()):
            for textView in view.mTextWithLocations:
                colListmap[textView]  = ColorWrapper(ColorUtil.cColortoInt(CColor.Blue), 3)
        else:
            colListmap[view]  = ColorWrapper(ColorUtil.cColortoInt(CColor.Red), 3)


    def addTextToHierarchyInternal(self,view, blocks):
        children = view.mChildren
        for childView in children:
            self.addTextToHierarchyInternal(childView, blocks)

        childBlocks = self.getTextAndRemove(view, blocks)
        if (len(childBlocks) == 0):
            return
		

        removedChildren = []
        for rectView in children:
            removed = False
            for ocrBlock in childBlocks:
#				// if it overlap a view but not include in it, we sh`ould just
#				// remove these views
#				// if children already has text, we should keep them
#				// *** There is situation in which the text right at the edge so
#				// the vision box
#				// need to expand just a bit (1 px each dimension) to cover the
#				// text
                if (RectUtil.contains(RectUtil.expand1Px(rectView),ocrBlock) or RectUtil.intersects(ocrBlock,rectView)
								 or RectUtil.contains(RectUtil.expand1Px(ocrBlock),rectView)):
                    removed = True
                    break
            if (removed):
                removedChildren.append(rectView)
                
  
        view.mChildren =  [x for x in view.mChildren if x not in removedChildren]
        view.mTextWithLocations = childBlocks
        
