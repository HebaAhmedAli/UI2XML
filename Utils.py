import sys
sys.path.append('../')
from collections import Counter 
from keras.preprocessing import image
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import numpy as np
import Preprocessing
import copy
import cv2
import math
#import PyQt4

def genTable (rows, columns):
        matrix = [[[255,255,255]] * columns for _i in range(rows)]
        #Indexes of first diagonal
        diag1 = [(i, i) for i in range(rows)]
        #Indexes of second diagonal
        diag2 = [(rows-i-1, i) for i in range(rows)]
        #Iterate over the indexes from diag1 and diag2 and modify matrix
        for i, j in diag1 + diag2:
            matrix[i][j] = [0,0,0]
            if i+1<rows:
                matrix[i+1][j] = [0,0,0]
            if j+1<columns:
                matrix[i][j+1] = [0,0,0]
            if i-1<rows:
                matrix[i-1][j] = [0,0,0]
            if j-1 < columns:
                matrix[i][j-1] = [0,0,0]
            if i+2<rows:
                matrix[i+2][j] = [0,0,0]
            if j+2<columns:
                matrix[i][j+2] = [0,0,0]
            if i-2<rows:
                matrix[i-2][j] = [0,0,0]
            if j-2 < columns:
                matrix[i][j-2] = [0,0,0]
        for i in range(columns):
            matrix[i][0] = [0,0,0]
            matrix[i][1] = [0,0,0]
            matrix[i][2] = [0,0,0]
            matrix[0][i] = [0,0,0]
            matrix[1][i] = [0,0,0]
            matrix[2][i] = [0,0,0]
            matrix[i][columns-1] = [0,0,0]
            matrix[i][columns-2] = [0,0,0]
            matrix[i][columns-3] = [0,0,0]
            matrix[columns-1][i] = [0,0,0]
            matrix[columns-2][i] = [0,0,0]
            matrix[columns-3][i] = [0,0,0]
        return matrix
    
# box = x,y,w,h
def iou(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2]+boxA[0], boxB[2]+boxB[0])
    yB = min(boxA[3]+boxA[1], boxB[3]+boxB[1])

    boxAArea = (boxA[2]) * (boxA[3])
    #boxBArea = (boxB[2]) * (boxB[3])
    interArea = (xB - xA) * (yB - yA)
    # compute the area of intersection rectangle
    if yB>=yA and xB >= xA:
        return interArea / float(boxAArea)
    else:
        return 0
    
def iouSmall(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2]+boxA[0], boxB[2]+boxB[0])
    yB = min(boxA[3]+boxA[1], boxB[3]+boxB[1])

    #boxAArea = (boxA[2]) * (boxA[3])
    boxBArea = (boxB[2]) * (boxB[3])
    interArea = (xB - xA) * (yB - yA)
    # compute the area of intersection rectangle
    if yB>=yA and xB >= xA:
        return interArea / float(boxBArea)
    else:
        return 0
    
def checkYrange(boxA,boxB):
    if (boxA[1]>=boxB[1] and boxA[1]<(boxB[1]+boxB[3])) or \
    ((boxA[1]+boxA[3])>boxB[1] and (boxA[1]+boxA[3])<(boxB[1]+boxB[3])) or \
    (boxB[1]>=boxA[1] and boxB[1]<(boxA[1]+boxA[3])) or \
    ((boxB[1]+boxB[3])>boxA[1] and (boxB[1]+boxB[3])<(boxA[1]+boxA[3])):
        return True
    return False

def checkXrange(boxA,boxB):
    if (boxA[0]>=boxB[0] and boxA[0]<(boxB[0]+boxB[2])) or \
    ((boxA[0]+boxA[2])>boxB[0] and (boxA[0]+boxA[2])<(boxB[0]+boxB[2])) or \
    (boxB[0]>=boxA[0] and boxB[0]<(boxA[0]+boxA[2])) or \
    ((boxB[0]+boxB[2])>boxA[0] and (boxB[0]+boxB[2])<(boxA[0]+boxA[2])):
        return True
    return False

def checkInsideRange(boxA,boxB):
    if boxB[0]>=boxA[0] and boxB[0]+boxB[2] <= boxA[0]+boxA[2] \
    and boxB[1]>=boxA[1] and boxB[1]+boxB[3] <= boxA[1]+boxA[3]:
        return True
    return False

def isSliceList(s,l):
    for i in range(len(s)):
        if s[i] not in l:
            return False
    return True

def mostFrequentInList(dictt,ocuurences,level): 
    if level>len(ocuurences)-1:
        return "-1"
    mostFreq = ocuurences[level] 
    if mostFreq < 2:
        return "-1"
    # Traverse dictionary and print key whose 
    # value is equal to second large element 
    for (key, val) in dictt.items(): 
        if val == mostFreq: 
            dictt.pop(key, None)
            return key

def getMostAndSecondMostColors(img,firstOnly):
    B = copy.copy(img)
    #B *= 255
    B = B.astype(int)
    B = np.reshape(B,(B.shape[0]*B.shape[1],B.shape[2]))
    rgb2hex = lambda r,g,b: '#%02x%02x%02x' %(r,g,b)
    hexArr =[ rgb2hex(*B[i,:]) for i in range(B.shape[0])]
    # Convert given list into dictionary 
    # it's output will be like {'ccc':1,'aaa':3,'bbb':2}
    dictt = Counter(np.array(hexArr))
    if "#-ff-ff-ff" in dictt:
        dictt.pop("#-ff-ff-ff", None)
    if len(dictt) == 0:
        if firstOnly:
            return "#ffffff"
        else:
            return "#ffffff","#000000"
    # Get the list of all values and sort it in ascending order 
    ocuurences = sorted(dictt.values(), reverse=True)
    first = mostFrequentInList(dictt,ocuurences,0).lstrip('#')
    firstRgb = tuple(int(first[i:i+2], 16) for i in (0, 2, 4))
    firstRgbs = sRGBColor(firstRgb[0]/255.0,firstRgb[1]/255.0,firstRgb[2]/255.0)
    color1Lab = convert_color(firstRgbs, LabColor)
    if firstOnly == True:
        return '#'+first
    deltaE = 0
    maxDeltaE = 0
    second = first
    maxDeltaSecond = first
    level = 1
    while deltaE <= 60:
        second = mostFrequentInList(dictt,ocuurences,level).lstrip('#')
        if second == "-1":
            return '#'+first,'#'+maxDeltaSecond
        secondRgb = tuple(int(second[i:i+2], 16) for i in (0, 2, 4))
        
        secondRgbs = sRGBColor(secondRgb[0]/255.0,secondRgb[1]/255.0,secondRgb[2]/255.0)
        # Convert from RGB to Lab Color Space
        color2Lab = convert_color(secondRgbs, LabColor)
        # Find the color difference
        deltaE = delta_e_cie2000(color1Lab, color2Lab)
        deltaE = abs(deltaE)
        if deltaE > maxDeltaE:
            maxDeltaE = deltaE
            maxDeltaSecond = second
        level += 1
    return '#'+first,'#'+second

def isCircle(imageCrop):
    edged = Preprocessing.preProcessEdges(imageCrop)
    (_, cnts, _) = cv2.findContours(edged,
                                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) == 0:
        return False
    cnt = max(cnts, key = cv2.contourArea)
    M = cv2.moments(cnt)
    circle = False
    if M['m00'] > 0:
        # calculate perimeter using
        peri = cv2.arcLength(cnt, True)
        area = cv2.contourArea(cnt)
        circularity  = 4*math.pi*(area/(peri*peri))
        # apply contour approximation and store the result in vertices
        vertices = cv2.approxPolyDP(cnt, 0.04 * peri, True)
        if (len(vertices) > 5 and circularity > 0.7) or len(vertices) == 5:
            circle = True
        # return the name of the shape
    return circle

'''
# For Testing.

img = image.load_img('/home/heba/Documents/cmp/fourth_year/gp/UI2XML/data/ScreenShots/ourTest/compOutputsface1A/5-android.widget.EditText.jpg')
img = np.array(img)  
print(getMostAndSecondMostColors(img,False))
'''
