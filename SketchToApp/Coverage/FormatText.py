# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 23:38:44 2018

@author: vo00timo
"""


def isEmpty(text):
    return text == None or len(text) == 0
def formatText(text):
    if (isEmpty(text)):
        return text
    buffer = ""
		# remove no ASCII character
    for c in text:
      
        if (c < ' ' or c > '~'):
            buffer+= ' '
           
        elif (c == chr(63)):
            buffer+="\\?"
           
        elif (c == chr(64)):
            buffer += '\\@'
          
        elif (c == chr(39)):
            buffer += '\\'
           
        else:
            buffer+=c
    return buffer.strip().replace("\\n", " ")

if __name__ =="__main__":
    print(formatText("Hello ? @"+chr(39)+chr(ord(' ')-2)+"World"))
    
    
    #print(formatText("Hello@"+chr(ord(' ')-2)) +"World"+chr(63)) "? @ "+