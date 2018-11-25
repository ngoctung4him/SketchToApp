from Rules.ASingleRule import ASingleRule
from Utils import ColorUtil
from RectUtils import RectUtil
from Rules.TextValidator import TextValidator
from Utils import Constants
from Utils import GroupUtil
from Utils import TextUtils
from string import printable


 

class RuleSingleCharacter(ASingleRule):
    
    def __init__(self,ocrs, views):
            super().__init__(ocrs, views)
    
    def singleCharacterofDots(self,text):
        singleInvalidCharacters = [',','.','+','-','o',')','(','/','\\','|','~']
        if(len(text)==1):
            if text not in singleInvalidCharacters:
                return True
            else:
                return False
        return True
#    @Override
    def accept(self,ocr):      
        if self.singleCharacterofDots(ocr.text):
            return None   
        
        
#        return None
#        
        tv = TextValidator(ocr, ( 130, 238, 255), False, "There is not text. it is all spaces")
        return tv

    
#     Contain: all spaces, all invisible chars, or all non-ascii chars
#     * 
#     * @param text
#     * @return
#     */

