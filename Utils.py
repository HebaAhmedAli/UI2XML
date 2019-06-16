import sys
sys.path.append('../')
import Constants as Constants
from collections import Counter 
from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000
import numpy as np
import copy
from keras.preprocessing import image
from PIL import Image
import os


# Converts the sequnce  into a list of integers representing the positions of the
# input sequence's strings in the "vocab"
def sequenceToIndices(sequence, vocab):
    keyStrings = sequence.split()  
    keyStrings = ['\t'] + keyStrings + ['\n']
    if len(keyStrings) > Constants.MAX_SEQUENCE_LENGTH:
        keyStrings = keyStrings[:Constants.MAX_SEQUENCE_LENGTH]       
    indices = list(map(lambda x: vocab.get(x), keyStrings))
    if len(keyStrings) < Constants.MAX_SEQUENCE_LENGTH:
        indices += [vocab['<pad>']] * (Constants.MAX_SEQUENCE_LENGTH - len(keyStrings))   
    for i in range(len(indices)):
        if indices[i] == None:
            indices.pop(i)
            indices.append(vocab['<pad>'])
    return indices

# Converts the list of indices into list of coresspnding keyStrings.
def indicesToSequence(indices, invVocab):
    keyStrings = [invVocab[i] for i in indices]
    sequence = ' '.join(keyStrings)
    return sequence

# box = x,y,w,h
def iou(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2]+boxA[0], boxB[2]+boxB[0])
    yB = min(boxA[3]+boxA[1], boxB[3]+boxB[1])

    # compute the area of intersection rectangle
    if yB>=yA and xB >= xA:
        return (xB - xA) * (yB - yA)
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
    '''
    if not os.path.exists(Constants.DIRECTORY+'/test2'):
            os.makedirs(Constants.DIRECTORY+'/test2')
    if not os.path.exists(Constants.DIRECTORY+'/test5'):
            os.makedirs(Constants.DIRECTORY+'/test5')
    Constants.x +=1
    Constants.y +=1
    '''
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
        #Image.fromarray(img).save(Constants.DIRECTORY+'/test5/'+"pic_"+str(Constants.x)+'_'+str(Constants.y)+'_'+'#'+first+'.png')
        return '#'+first
    deltaE = 0
    maxDeltaE = 0
    second = first
    maxDeltaSecond = first
    level = 1
    while deltaE <= 60:
        second = mostFrequentInList(dictt,ocuurences,level).lstrip('#')
        if second == "-1":
            #print(deltaE,level,'exit')
            #Image.fromarray(img).save(Constants.DIRECTORY+'/test2/'+"pic_"+str(Constants.x)+'_'+str(Constants.y)+'_'+'#'+first+'#'+maxDeltaSecond+'.png')
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
    #print(deltaE,level)
    #Image.fromarray(img).save(Constants.DIRECTORY+'/test2/'+"pic_"+str(Constants.x)+'_'+str(Constants.y)+'_'+'#'+first+'#'+second+'.png')
    return '#'+first,'#'+second

# For Testing.
'''
img = image.load_img('/home/heba/Documents/cmp/fourth_year/gp/UI2XML/data/ScreenShots/output/test4/pic_246_246.png')
img = np.array(img)  

print(getMostAndSecondMostColors(img,False))
'''
# For test set slice.
'''
myList = [[[1,1,1],[1,1,1]],[[1,1,1],[1,1,1]],[[1,1,1],[1,1,1]]]
B = copy.copy(np.array(myList))
B[0:3,1:3]=np.array([-255,-255,-255])  # y , x
print(B)
print(getMostAndSecondMostColors(B,True))
'''