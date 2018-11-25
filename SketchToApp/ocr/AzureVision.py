# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 20:12:48 2018

@author: sxm6202xx
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 19:21:06 2018

@author: sxm6202xx
"""
import requests
from matplotlib.patches import Polygon
import time
import cv2
import os

def detectText(imagePath):
    try:
        vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
        ocr_url = vision_base_url + "recognizeText"
        subscription_key = "294807076f4d4dd2a65cc461f2901aa3"
        image_data = open(imagePath, "rb").read()
        headers  = {'Ocp-Apim-Subscription-Key': subscription_key,  "Content-Type": "application/octet-stream" }
        params   = {'handwriting' : True}
        response   = requests.post(ocr_url, 
                                   headers=headers, 
                                   params=params, 
                                   data=image_data)
        response.raise_for_status()
        #    operation_url = response.headers["Operation-Location"]
        analysis = {}
        while not "recognitionResult" in analysis:
            response_final = requests.get(response.headers["Operation-Location"], headers=headers)
            analysis       = response_final.json()
            time.sleep(1)
        #polygons = [(line["boundingBox"], line["text"]) for line in analysis["recognitionResult"]["lines"]]
        polygons = [(line["text"]) for line in analysis["recognitionResult"]["lines"]]
        print(polygons)
        if (polygons!=[]):
            print("sketch is a screen\n")
            return True
        else:
            print("sketh is not a screen\n")
            return False
        
    except:
        print("Getting Error, maybe blank image")
        
        return False
#plt.figure(figsize=(15,15))
#
#image  = Image.open(BytesIO(requests.get(image_url).content))
#ax     = plt.imshow(image)





def getTextfromNA(mImage):
#    resizedImage = cv2.resize(mImage,(1200,768), interpolation = cv2.INTER_CUBIC)
    cv2.imwrite("vision_temp.jpg",mImage)
    textOut = detectText("vision_temp.jpg")
    os.remove("vision_temp.jpg")
    return textOut

if __name__ =="__main__":
    filename = r"vision_temp.jpg"
    detectText(filename)