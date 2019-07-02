import sys
sys.path.append('../')
from collections import Counter 
from keras.preprocessing import image
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import numpy as np
import cv2
import copy
import math
from skimage.feature import hog,local_binary_pattern
import Constants
import Preprocessing
import re

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
         # If under each other.
        if boxA[1]<boxB[1] and boxB[1]-boxA[1]>=boxA[3]-5:
            return False
        elif boxB[1]<boxA[1] and boxA[1]-boxB[1]>=boxB[3]-5:
            return False
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
    return "-1"

def detectShapeAndFeature(cnt):
    M = cv2.moments(cnt)
    shape = 'unknown'
    noOfVer = 0
    areaRatio = 0
    perRatio = 0
    aspectRatio = 0
    if M['m00'] > 0:
        # calculate perimeter using
        peri = cv2.arcLength(cnt, True)
        area = cv2.contourArea(cnt)
        circularity  = 4*math.pi*(area/(peri*peri))
        # apply contour approximation and store the result in vertices
        vertices = cv2.approxPolyDP(cnt, 0.04 * peri, True)
        noOfVer = len(vertices)/16
        x, y, width, height = cv2.boundingRect(vertices)
        aspectRatio = float(width) / height
        areaRatio = float(area)/(width*height)
        perRatio = float(peri)/(2*(width+height))
        if len(vertices) == 4 and aspectRatio >= 0.95 and aspectRatio <= 1.05:
            shape = "square"
        elif len(vertices) > 5 and circularity >= 0.7:
            shape = "circle"
        else:
            shape = "unknown"
        # return the name of the shape
    features = []
    if shape == "square":
        features.append(1)
    else:
        features.append(0)
    if shape == "circle":
        features.append(circularity)
    else:
        features.append(0)
    features.append(noOfVer)
    features.append(areaRatio)
    features.append(perRatio)
    features.append(aspectRatio)
    return features

# Take gray resized image.
def describeLBP(gray,numPoints=8,radius=1,eps=1e-7):
         # compute the Local Binary Pattern representation
		# of the image, and then use the LBP representation
		# to build the histogram of patterns
        lbp = local_binary_pattern(gray, numPoints,radius, method="default")     
        (hist, _) = np.histogram(lbp, bins=256, range=(0,256))	
        #(hist, _) = np.histogram(lbp.ravel(),bins=np.arange(0, numPoints + 3),range=(0, numPoints + 2))
		# normalize the histogram [np.where(lbp<255)]
        hist = hist.astype("float")
        if hist.sum()!=0:
          hist /= (hist.sum())
		# return the histogram of Local Binary Patterns
        return hist.tolist()
    
# Take gray resized image.  
def descripeHog(gray):
    (H, hogImage) = hog(gray, orientations=8, pixels_per_cell=(150,150),
                    cells_per_block=(1,1), visualize=True)
    H = H.astype("float")
    if H.sum()!=0.0:
      H /= (H.sum())
    return H.tolist()

# Take gray resized image.
def describe5Gray(gray):
    (hist5Gray, _) = np.histogram(gray, bins=5)
    hist5Gray = hist5Gray.astype("float")
    if hist5Gray.sum()!=0.0:
      hist5Gray /= (hist5Gray.sum())
    return hist5Gray.tolist()

def getResizeRatios(img):
    ratios = []
    if img.shape[1] == 0:
      print("image 0 ratio")
      ratios.append(0)
    elif img.shape[1]<Constants.IMAGE_SIZE_CLASSIFICATION:
        ratios.append(img.shape[1]/Constants.IMAGE_SIZE_CLASSIFICATION)
    else:
        ratios.append(-1*(Constants.IMAGE_SIZE_CLASSIFICATION/img.shape[1]))
    if img.shape[0] == 0:
      print("image 0 ratio")
      ratios.append(0)
    elif img.shape[0]<Constants.IMAGE_SIZE_CLASSIFICATION:
        ratios.append(img.shape[0]/Constants.IMAGE_SIZE_CLASSIFICATION)
    else:
        ratios.append(-1*(Constants.IMAGE_SIZE_CLASSIFICATION/img.shape[0]))
    return ratios

# Take edged resized image.
def getLinesEdgesFeatures(edged):
    noOfEdges = cv2.countNonZero(edged)
    lines = cv2.HoughLinesP(edged, 1, np.pi/180, 20,minLineLength = 20)
    maxHorLen = 0
    slopedLines = 0
    noOfLines = 0
    if lines is not None:
        noOfLines = len(lines)
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if y2 - y1 == 0:
                length = math.sqrt( ((x1-x2)**2)+((y1-y2)**2))
                maxHorLen = max(maxHorLen,length)
            if (x2 - x1) != 0:
              if (y2 - y1)/(x2 - x1) <= -0.9 and (y2 - y1)/(x2 - x1) >= -1.1:
                  slopedLines += 1
              
    return [(noOfEdges-2306.345)/8900.044,(noOfLines-3.64957)/12.172,maxHorLen/Constants.IMAGE_SIZE_CLASSIFICATION,slopedLines]


def getNoOfColorsAndBackGroundRGB(img):
    dictMean = 3122.3086264194926
    dictStd = 20159.43 
    B = copy.copy(img)
    B = B.astype(int)
    B = np.reshape(B,(B.shape[0]*B.shape[1],B.shape[2]))
    rgb2hex = lambda r,g,b: '#%02x%02x%02x' %(r,g,b)
    hexArr =[ rgb2hex(*B[i,:]) for i in range(B.shape[0])]
    dictt = Counter(np.array(hexArr))
    if len(dictt) == 0:
        return [0,-1.0,-1.0,-1.0]
    # Get the list of all values and sort it in ascending order 
    ocuurences = sorted(dictt.values(), reverse=True)
    first = mostFrequentInList(dictt,ocuurences,0).lstrip('#')
    if first == "-1":
      return [(len(dictt)-dictMean)/dictStd,-1.0,-1.0,-1.0]
    firstRgb = tuple(int(first[i:i+2], 16) for i in (0, 2, 4))
    return [(len(dictt)-dictMean)/dictStd,firstRgb[0]/255.0,firstRgb[1]/255.0,firstRgb[2]/255.0]

def getMostAndSecondMostColors(img,firstOnly):
    B = copy.copy(img)
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
    edged,_ = Preprocessing.preProcessEdges(imageCrop)
    (_, cnts, _) = cv2.findContours(edged,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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

def getContentOfComponent(filedata,componentId):
    toSearch = 'android:id = "@+id/'+ componentId
    i=filedata.find(toSearch)
    content = ""
    while filedata[i] != '>':
        content+=filedata[i]
        i+=1
    content+='>'
    contentList = content.split('\n')
    content = ""
    for i in range(len(contentList)):
        contentList[i]=contentList[i].strip('\t')
        content += ('\n\t'+contentList[i])
    #content = '\n\t'.join(contentList)
    return content

def getXmlOfComponent(index,appName): # index of component in the list of ids in map, appName is the key of map for this activity.
    filedata = ""
    with open(Constants.mapToGui[appName][4][index][1], 'r') as file:
            filedata = file.read()
    file.close() 
    toPrint = ""
    if Constants.mapToGui[appName][4][index][0] == "":
        toPrint += '<'+Constants.mapToGui[appName][2][index]+'\t'
        content = getContentOfComponent(filedata,Constants.mapToGui[appName][1][index])
        toPrint += content+'\n'
        toPrint += '</'+Constants.mapToGui[appName][2][index]+'>'
    else:
        toPrint += '<'+'ListView'+'\t'
        content = getContentOfComponent(filedata,Constants.mapToGui[appName][4][index][0])
        toPrint += content+'\n'
        toPrint += '</'+'ListView'+'>'
    return toPrint
    
# For Testing.
'''
img = image.load_img('/home/heba/Documents/cmp/fourth_year/gp/UI2XML/data/17-android.widget.ImageView.jpg')
img = np.array(img)  
print(getNoOfColors(img[10:img.shape[0]-10,10:img.shape[1]-10]))
'''
'''
first = "000000"
firstRgb = tuple(int(first[i:i+2], 16) for i in (0, 2, 4))
firstRgbs = sRGBColor(firstRgb[0]/255.0,firstRgb[1]/255.0,firstRgb[2]/255.0)
color1Lab = convert_color(firstRgbs, LabColor)
second = "556b2f"
secondRgb = tuple(int(second[i:i+2], 16) for i in (0, 2, 4))

secondRgbs = sRGBColor(secondRgb[0]/255.0,secondRgb[1]/255.0,secondRgb[2]/255.0)
# Convert from RGB to Lab Color Space
color2Lab = convert_color(secondRgbs, LabColor)
# Find the color difference
deltaE = delta_e_cie2000(color1Lab, color2Lab)
print(deltaE)
'''