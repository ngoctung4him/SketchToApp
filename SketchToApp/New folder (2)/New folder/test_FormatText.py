# -*- coding: utf-8 -*-

# test_mymath.py
import FormatText
import unittest
 
class TestFormatText(unittest.TestCase):
    """
    Test the add function from the mymath library
    """
 
    def test_formatText(self):
        """
        Test that the addition of two integers returns the correct total
        """
        result = FormatText.formatText("Hello ? @"+chr(39)+chr(ord(' ')-2)+"World")
        self.assertEqual(result, 'Hello \? \@\ World')
 
   
 
if __name__ == '__main__':
    unittest.main()