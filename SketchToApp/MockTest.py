# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 00:47:54 2018

@author: vo00timo
"""

import unittest
from FormatText import formatText 
from mock import Mock
class MyTest(unittest.TestCase):
    def test_something(self):
        mock_formatText= Mock()
        formatText(mock_formatText,"Hello ? @ World");
        print(mock_formatText.mock_calls)
       
        pass

if __name__ == "__main__":
    unittest.main()