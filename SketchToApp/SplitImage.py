import os
import cv2
import copy
# Numbers of rows
nRows = 4
# Number of columns
mCols = 2
fileLocation="sketchImage.jpg"
fileExitst = os.path.isfile(fileLocation)
if(not fileExitst):
    print("Can't access the file")
# Reading image
img_raw = cv2.imread(fileLocation)
image = copy.deepcopy(img_raw)
#cv2.imshow("Raw Image", image)
cv2.waitKey(0)
height, width = image.shape[:2]
print (image.shape)
# Let's get the starting pixel coordiantes (top left of cropped top)
start_row, start_col = int(0), int(0)
starting_row, starting_col = int(0), int(0)
ending_row, ending_col = int(0), int(0)
count=int(0)
name=''
crop_image=[20]
for i in range(1,4):
    starting_row=ending_row
    ending_row=int(height* (i/3))
    ending_col= int(0)
    for j in range(1,4):
        
        starting_col= ending_col
        ending_col=int(width*(j/3))
        name='crop'+str(i)+str(j);
        name= image[starting_row:ending_row, starting_col:ending_col]
        print('('+str(starting_row)+','+str(starting_col)+') - ('+str(ending_row)+','+str(ending_col)+')')
        
        #cv2.imshow('crop'+str(i)+str(j), name) 
        cv2.imwrite('crop'+str(i)+str(j)+'.jpg',name)
    
    
    
#cv2.imshow('crop'+str(i)+str(j), name) 
#cv2.waitKey(0) 
#cv2.imwrite('temp.jpg', img_raw)
# =============================================================================
# # Let's get the ending pixel coordinates (bottom right of cropped top)
# end_row, end_col = int(height * .5), int(width)
# cropped_top = image[start_row:end_row , start_col:end_col]
# print (start_row, end_row) 
# print (start_col, end_col)
# 
# cv2.imshow("Cropped Top", cropped_top) 
# cv2.waitKey(0) 
# cv2.destroyAllWindows()
# 
# # Let's get the starting pixel coordiantes (top left of cropped bottom)
# start_row, start_col = int(height * .5), int(0)
# # Let's get the ending pixel coordinates (bottom right of cropped bottom)
# end_row, end_col = int(height), int(width)
# cropped_bot = image[start_row:end_row , start_col:end_col]
# print (start_row, end_row) 
# print (start_col, end_col)
# 
# cv2.imshow("Cropped Bot", cropped_bot) 
cv2.waitKey(100) 
# =============================================================================
#cv2.destroyAllWindows()