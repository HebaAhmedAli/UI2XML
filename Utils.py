import sys
sys.path.append('../')
from collections import Counter 
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import numpy as np
import copy


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

