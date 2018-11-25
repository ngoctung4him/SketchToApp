from Rules.ASingleRule import ASingleRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Rules.TextValidator import TextValidator
from Utils import Constants
from ocr.OCRTextWrapper import OCRTextWrapper
from Utils import GroupUtil
from Utils import TextUtils
from Utils.ColorUtil import CColor
from string import printable


class RuleInvalidCharacter(ASingleRule):
    def __init__(self,ocrs, views):
            super().__init__(ocrs, views)

#    @Override
            
            
    def validCharacters(self,text):
        asciiContain = all([ord(char) < 33 or ord(char)>126 for char in text])
        invalidChar = len([char for char in text if char not in printable]) != 0 
        allSpace = all([" " == c or '\n'== c for c in text])
        return not(allSpace or invalidChar  or asciiContain)
    

        
        
    
    def accept(self, ocr):
        if self.validCharacters(ocr.text):
            return None
        
        
        tv = TextValidator(ocr, CColor.Magenta, False,"width is 0")
        return tv
