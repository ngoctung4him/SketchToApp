# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

class Screen:
   'Common base class for all employees'
   scrCount = 0

   def __init__(self, name, x_start, x_end, y_start, y_end):
       self.name = name
       self.x_start = x_start
       self.x_end = x_end
       self.y_start = y_start
       self.y_end = y_end
       Screen.scrCount += 1
   
   def displayCount(self):
     print ("Total Screen %d" % Screen.scrCount)

   def displayScreen(self):
      print ("screen : ", self.name,"x_start : ", self.x_start,  ", x_end: ", self.x_end, "y_start : ", self.y_start,  ", y_end: ", self.y_end)