from Rules.ASingleRule import ASingleRule
from Rules.TextValidator import TextValidator
import ocr.TextProcessorUtil as TextProcessorUtil
from Utils.ColorUtil import CColor

class RuleNoChildren (ASingleRule):
    def __init__(self,ocrs, views):
            super().__init__( ocrs, views)

#    @Override
    def accept(self, ocr):
#        return None
        hasChildren = TextProcessorUtil.hasParent(ocr, self.mOcrs)
        if not hasChildren:
            return None
        tv = TextValidator(ocr, CColor.Magenta, False, "no children")
        return tv
    

