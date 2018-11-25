# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 18:54:39 2017

@author: soumi
"""

class Point:
    x = 0 
    y = 0
    def __init__(self,x,y):
        self.x = x
        self.y= y
        
    def cvPoint(self):
        return (self.x, self.y)
    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        
        if other is None:
            return False
        else:
            return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        return not(self.__eq__(other))