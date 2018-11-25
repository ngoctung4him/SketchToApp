from Rules.RuleInvalidCharacter import RuleInvalidCharacter
from Rules.RuleSingleCharacter import RuleSingleCharacter
from Rules.RuleNoHeight import RuleNoHeight
from Rules.RuleNoWidth import RuleNoWidth
from Rules.RuleBoxHasWordTooSmall import RuleBoxHasWordTooSmall
from Rules.RuleNoChildren import RuleNoChildren
from Rules. RuleBoxHasOneWordTooSmall import RuleBoxHasOneWordTooSmall
from Utils import Logger


class RuleManager:
    
    def __init__(self,ocrTextWrappers, views):
        self.mOCRRules = []
        self.mVisionRules = []
        self.mViews = views
        self.mOcrTextWrappers = ocrTextWrappers
        self.initOCRRules()
        self.initVisionRules()


    def initVisionRules(self):
        return
#       self.mVisionRules.append( RuleTextTooBigCompWords(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
#       self.mVisionRules.append( RuleVisionBoxHasSoManyInvalidTexts(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
#       self.mVisionRules.append( RuleBaseOnNeighbour(self.mDipCalculator, self.mOcrTesseractOCR, self.mMatLog, self.mOcrTextWrappers, self.mViews))
    

    def initOCRRules(self):        
        self.mOCRRules.append(RuleInvalidCharacter(self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleSingleCharacter(self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleNoHeight(self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleNoWidth(self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleBoxHasWordTooSmall(self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleNoChildren(self.mOcrTextWrappers, self.mViews))
        self.mOCRRules.append(RuleBoxHasOneWordTooSmall(self.mOcrTextWrappers, self.mViews))

    def acceptOCRRules(self,ocr):
        firstTextValidator = None
        for rule in self.mOCRRules:
            textValidator = rule.accept(ocr)
            if textValidator != None and not textValidator.valid :
                firstTextValidator = textValidator
#                print(textValidator.log)
                break
        
        
        return firstTextValidator
    

    def acceptVisionRules(self,invalidTexts, acceptedOcrTextWrappers):
        for rule in self.mVisionRules:
            match = rule.run(invalidTexts, acceptedOcrTextWrappers)
            if match:
                Logger.append(Logger.RULE_INFO_LOG, "\t" +  type(rule).__name__)
        