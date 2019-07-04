import sys
sys.path.append('../')
import cv2
import numpy as np
import random
import Utils

# CANNY algorithm
CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO = 0.66
# we want to low threshold value of candy always below 0.1 #255, some
# image the contrast between button and background not must different
CANNY_RATIO_CONTROL_THRESHOLD = 0.1 / CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO
    
dilationSize = 1
lowThreshold = 30 #30
highThreshold = 60 #60
editTextThresholdHeight = 15
editTextThresholdAddedHeight = 50

def preProcess(image):
    grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayImg, (3,3), 0)  
    kernel = np.ones((2 * dilationSize + 1, 2 * dilationSize + 1), np.uint8)
    edges = cv2.Canny(blurred, lowThreshold, highThreshold)
    morph = cv2.dilate(edges,kernel,iterations = 5)
    return morph,edges

# Extract boxes from given image.
def extractBoxes(img):
    allBoxes=[]
    addedManuallyBool=[]
    morph,edges=preProcess(img)
    #finding the contours
    (_, contours , _) = cv2.findContours(morph, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)    
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(img,(x,y),(x+w,y+h),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),2)
        allBoxes.append([x, y, w, h])
        addedManuallyBool.append(False)
        if h <= editTextThresholdHeight:
            #cv2.rectangle(img,(x,y-editTextThresholdAddedHeight),(x+w,y+h+editTextThresholdAddedHeight),(random.randint(0,255),random.randint(0,255),random.randint(0,255)),2)
            allBoxes.append([x, y-editTextThresholdAddedHeight, w, h+editTextThresholdAddedHeight])
            addedManuallyBool.append(True)
    allBoxes,addedManuallyBool = zip(*sorted(zip(allBoxes,addedManuallyBool), key=lambda x: boxArea(x),reverse=True))
    return allBoxes,addedManuallyBool

def boxArea(x):
    return x[0][2]*x[0][3]
