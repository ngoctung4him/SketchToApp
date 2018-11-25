# import the necessary packages
import cv2
 
# load the image and show it
image = cv2.imread("sketchImage.jpg")
cv2.imshow("original", image)
cv2.waitKey(0)