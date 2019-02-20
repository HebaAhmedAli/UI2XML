import cv2
import numpy as np



# CANNY algorithm
CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO = 0.66
# we want to low threshold value of candy always below 0.1 #255, some
# image the contrast between button and background not must different
CANNY_RATIO_CONTROL_THRESHOLD = 0.1 / CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO
    
dilationSize = 1
lowThreshold = 30
highThreshold = 80
cannyRatio = 2


def preProcess(image):
    # convert the image to grayscale, blur it slightly, and threshold it
    grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(grayImg, (5,5), 0)  
    kernel = np.ones((2 * dilationSize + 1, 2 * dilationSize + 1), np.uint8)
    edges = cv2.Canny(blurred, lowThreshold, highThreshold)
    morph = cv2.dilate(edges,kernel,iterations = 5)
    return morph

# Extract boxes from given image.
def extractBoxes(img):
    allBoxes=[]
    morph=preProcess(img)
    #finding the contours
    (contours, hierarchy, _) = cv2.findContours(morph, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   
    #contours = np.array(contours).reshape((-1,1,2)).astype(np.int32)
    #cv2.drawContours(img,contours,-1,(0,0,255),2)
    for cnt in contours:
        cnt = np.array(cnt).reshape((-1,1,2)).astype(np.int32)
        cv2.drawContours(img,[cnt],0,(0,0,255),2)
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        allBoxes.append([x, y, w, h])
     
    filteredBoxes=filterBoxes(allBoxes)
    return filteredBoxes

def filterBoxes(allBoxes):
    filteredBoxes=allBoxes #TODO: Filter Them.
    
    return filteredBoxes