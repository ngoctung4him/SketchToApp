from Rules.ASingleRule import ASingleRule

class RuleBoxHasOneWordTooSmall(ASingleRule):
    
    def __init__(self,ocrs, views):
            super().__init__(ocrs, views)

#    @Override
    def accept(self,ocr):
        return None
#         bound = ocr
#         for view in self.mViews :
#            // the box may has the word is too small compare with the word
#            // itself.
#            // If the word a children view which only have on child, we need
#            // to verify if:
#            // (2) This child view really small compare to the word bound
#            // same here: the box may has the word is too big compare to the
#            // word itself we also make sure that this view may also have
#            // other view but it so tiny will be ignore when layout
#            // itself and there is only one word in here
#            if TextProcessorUtil.areChildrenIsTooSmall(self.mainImageDimension, view) and RectUtil.contains(view, bound):
#                if RectUtil.dimesionSmallerThan(ocr, view, 0.8):
#                    # this is wrong, ignore this word
#                    tv =  TextValidator(ocr, CColor.Pink, False, "The box may has the word is too big compare to the word, and there is only one word in here. This view may also have other view but it so tiny")
#                    return tv
#                
#         return None
