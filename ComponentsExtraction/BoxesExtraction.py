import cv2
import pytesseract as pt
import numpy as np
from PIL import Image
import os



# CANNY algorithm
CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO = 0.66
# we want to low threshold value of candy always below 0.1 #255, some
# image the contrast between button and background not must different
CANNY_RATIO_CONTROL_THRESHOLD = 0.1 / CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO
    
dilationSize = 1
lowThreshold = 30
highThreshold = 80
cannyRatio = 2

def updateLowHeightThreshold(imgData):
    imgHist = cv2.equalizeHist(imgData)
    mean = np.average(imgHist)
    lowThreshold = int(CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO * mean * CANNY_RATIO_CONTROL_THRESHOLD)
    highThreshold = int(CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO * cannyRatio * mean * CANNY_RATIO_CONTROL_THRESHOLD)
    return lowThreshold, highThreshold

def preProcess(image):
    # convert the resized image to grayscale, blur it slightly,
    # and threshold it
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayImg, (5,5), 0)  
    #lowThreshold, highThreshold = updateLowHeightThreshold(blurred)
    kernel = np.ones((2 * dilationSize + 1, 2 * dilationSize + 1), np.uint8)
    edges = cv2.Canny(blurred, lowThreshold, highThreshold)
    morph = cv2.dilate(edges,kernel,iterations = 5)
    return morph

# Extract boxes from given image.
def extractBoxes(img, directory):
    allBoxes=[]

    preProcessedImage = preProcess(img)
    #finding the contours
    (contours, hierarchy, _) = cv2.findContours(preProcessedImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    j = 0
    margin = 10
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if not os.path.exists(directory):
            os.makedirs(directory)
        # testing: print the cropped in folder
        crop_img = img[y-margin:y+h+margin, x-margin:x+w+margin]
        cv2.imwrite(directory + "/comp"+str(j) + ".jpg",crop_img)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        allBoxes.append([x, y, w, h])
        j=j+1

    filteredBoxes=filterBoxes(allBoxes)
    return filteredBoxes

def filterBoxes(allBoxes):
    filteredBoxes=allBoxes #TODO: Filter Them.
    
    return filteredBoxes