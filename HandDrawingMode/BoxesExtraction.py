import cv2
import numpy as np
from scipy.ndimage import morphology, label
import random
import Utils

# CANNY algorithm
CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO = 0.66
# we want to low threshold value of candy always below 0.1 #255, some
# image the contrast between button and background not must different
CANNY_RATIO_CONTROL_THRESHOLD = 0.1 / CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO
    
dilationSize = 1
lowThreshold = 30
highThreshold = 80
cannyRatio = 2

def boxArea(x):
    return x[0][2]*x[0][3]

def preProcess(image):
    # convert the image to grayscale, blur it slightly, and threshold it
    im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Inner morphological gradient.
    morph = morphology.grey_dilation(im, (5, 5)) - im
    return morph

def getFirstUnvisitedIndex(visited):
    for i in range(len(visited)):
        if visited[i]== False:
            return i
    return -1

def groupHorizontalTexts(boxes,texts):
    groupedTexts = []
    groupedBoxs = []
    if (len(boxes)) == 0:
        return boxes,texts
    visited = [False for i in range(len(boxes))]
    indexUnvisited = 0
    while(indexUnvisited!=-1):
        backetTexts = []
        backetBoxs = []
        backetTexts.append(texts[indexUnvisited])
        backetBoxs.append(boxes[indexUnvisited])
        visited[indexUnvisited]=True
        for i in range(indexUnvisited+1,len(boxes)):
            if visited[i] == False and Utils.checkYrange(boxes[i],boxes[indexUnvisited]) == True:
                visited[i] = True
                backetTexts.append(texts[i])
                backetBoxs.append(boxes[i])
        groupedTexts.append(backetTexts)
        groupedBoxs.append(backetBoxs)
        indexUnvisited=getFirstUnvisitedIndex(visited)
    return groupedBoxs,groupedTexts

def mergeTextBoxsForSameWord(txtBoxes,texts,imgW):
    groupedBoxs,groupedTexts = groupHorizontalTexts(txtBoxes,texts)
    txtBoxes = []
    texts = []
    for i in range(len(groupedBoxs)):
        groupedBoxs[i],groupedTexts[i] = zip(*sorted(zip(groupedBoxs[i],groupedTexts[i]), key=lambda x: x[0][0],reverse=False))
        j=0
        while j<len(groupedBoxs[i]):
            startJ = j
            minY = groupedBoxs[i][startJ][1]
            maxY =  groupedBoxs[i][startJ][3]+groupedBoxs[i][startJ][1]
            while j+1 < len(groupedBoxs[i]) and (groupedBoxs[i][j+1][0]-(groupedBoxs[i][j][0]+groupedBoxs[i][j][2]))/imgW < 0.07:
                j+=1
                minY = min(minY,groupedBoxs[i][j][1])
                maxY = max(maxY,groupedBoxs[i][j][3]+groupedBoxs[i][j][1])
            texts.append(' '.join(groupedTexts[i][startJ:j+1]))
            txtBoxes.append([groupedBoxs[i][startJ][0],minY,groupedBoxs[i][j][0]+groupedBoxs[i][j][2]-groupedBoxs[i][startJ][0],maxY-minY])
            j += 1
    return txtBoxes,texts
# Extract boxes from given image.
def extractBoxes(img,texts, txtBoxes):    
    allBoxes = []
    isText = []
    morph=preProcess(img)
    # Binarize.
    mean, std = morph.mean(), morph.std()
    t = mean + std
    morph[morph < t] = 0
    morph[morph >= t] = 1
    # Connected components.
    lbl, numcc = label(morph)
    # Size threshold.
    min_size = 200 # pixels
    biggestBoxArea = []
    minxBox = 10000000
    maxxBox = 0
    minyBox = 10000000
    maxyBox = 0
    for i in range(1, numcc + 1):
        py, px = np.nonzero(lbl == i)
        if len(py) < min_size:
            morph[lbl == i] = 0
            continue
        xmin, xmax, ymin, ymax = px.min(), px.max(), py.min(), py.max()
        randColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        cv2.rectangle(img, (xmin,ymin), (xmax,ymax), randColor,2)
        allBoxes.append([xmin, ymin, xmax-xmin, ymax-ymin])
        isText.append("")
        minxBox = min(xmin,minxBox)
        maxxBox = max(xmax,maxxBox)
        minyBox = min(ymin,minyBox)
        maxyBox = max(ymax,maxyBox)
    txtBoxes,texts = mergeTextBoxsForSameWord(txtBoxes,texts,maxxBox-minxBox)
    for i in range(len(txtBoxes)):
        minxBox = min(txtBoxes[i][0],minxBox)
        maxxBox = max(txtBoxes[i][0]+txtBoxes[i][2],maxxBox)
        minyBox = min(txtBoxes[i][1],minyBox)
        maxyBox = max(txtBoxes[i][1]+txtBoxes[i][3],maxyBox)
    biggestBoxArea.append([minxBox, minyBox, maxxBox-minxBox, maxyBox-minyBox])
    # Add isText and textBoxes
    allBoxes += txtBoxes
    isText += texts
    allBoxes,isText = zip(*sorted(zip(allBoxes,isText), key=lambda x: boxArea(x),reverse=True))
    biggestBoxArea+=allBoxes[1:len(allBoxes)]
    allBoxes = biggestBoxArea
    return allBoxes,isText

