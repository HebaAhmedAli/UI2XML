import sys
sys.path.append('../')
import ComponentsExtraction.BoxesExtraction as BoxesExtraction
import ComponentsExtraction.TextExtraction as TextExtraction
import ModelClassification.Model as Model
from PIL import Image
import Utils
import Preprocessing
import numpy as np
import cv2

heightThrshold1 = 20
heightThrshold2 = 40
margin = 10



# Extract the boxes and text from given image -extracted components- and predict them.
def extractComponentsAndPredict(image,imageCopy,imageXML,model,invVocab):
    extratctedBoxes,addedManuallyBool=BoxesExtraction.extractBoxes(image)
    extractedText=[] # List of strings coreesponding to the text in each box.
    pedictedComponents=[]
    # Note: If the box doesn't contain text its index in the extractedText list should contains empty string.
    margin = 10
    height=image.shape[0]
    width=image.shape[1]
    for x,y,w,h in extratctedBoxes:
        features = []
        croppedImage = imageCopy[max(0,y - margin):min(height,y + h + margin), max(x - margin,0):min(width,x + w + margin)]
        croppedImageColor = imageXML[max(0,y):min(height,y + h), max(x,0):min(width,x + w)]
        noOfColorsNorm = Utils.getNoOfColors(croppedImageColor)
        text = TextExtraction.extractText(croppedImage)
        textFeature = 0
        if text != "":
            textFeature = 1
        features.append(noOfColorsNorm)
        features.append(textFeature)
        features += extractShapeFeatures(croppedImage)
        pedictedComponents.append(Model.makeAprediction(invVocab,np.array(features,dtype='float32'),croppedImage,model))
        extractedText.append(TextExtraction.extractText(croppedImage))
    return extratctedBoxes,extractedText,addedManuallyBool,pedictedComponents



def extractShapeFeatures(img):
    edges=Preprocessing.preProcessEdges(img)
    (_, contours , _) = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
    c = max(contours, key = cv2.contourArea)
    shapeFeature=Utils.detectShapeAndFeature(c)
    return shapeFeature
        
def filterComponents(boxes, texts ,addedManuallyBool ,predictedComponents,imageCopy,model,invVocab):
    boxesRemovingManual,textsRemovingManual,predictedComponentsRemovingManual= \
    removenonEditTextThatAddedManually(boxes,texts,addedManuallyBool,predictedComponents)
    
    boxesInBackets,textsInBackets,predictedComponentsInBackets \
    =backetOverlappingBoxes(boxesRemovingManual,textsRemovingManual,predictedComponentsRemovingManual)
    
    boxesFiltered = []
    textsFiltered = []
    predictedComponentsFiltered = []
    for i in range(len(boxesInBackets)):
        filterEachBacket(boxesInBackets[i],textsInBackets[i],predictedComponentsInBackets[i], \
                         boxesFiltered,textsFiltered,predictedComponentsFiltered,imageCopy,model,invVocab)
    if 'android.widget.Button' not in predictedComponentsFiltered \
    and 'android.widget.EditText' in predictedComponentsFiltered:
        changeEditTextToTextViewInCaseNoButtons(predictedComponentsFiltered)    
    if 'android.widget.ProgressBarVertical' in predictedComponentsFiltered\
        or 'android.widget.ProgressBarHorizontal' in predictedComponentsFiltered: # TODO : Try to find alternative sol.
        boxesFiltered,textsFiltered,predictedComponentsFiltered = changeProgressBarVerticalToRadioButtonAndDeleteHorizontal(boxesFiltered,textsFiltered,predictedComponentsFiltered,imageCopy)
    buttonsKeyWords(boxesFiltered,textsFiltered,predictedComponentsFiltered,imageCopy) # TODO : Comment in case change.
    return boxesFiltered,textsFiltered,predictedComponentsFiltered

# Case image containing all image or text inside.
def specialCaseImageText(boxesInBacket,textsInBacket,predictedComponentsInBacket,imageCopy):
    imageArea=imageCopy.shape[0]*imageCopy.shape[1]
    if predictedComponentsInBacket[0] == 'android.widget.ImageView' \
    or predictedComponentsInBacket[0] == 'android.widget.TextView':
        baseArea = boxesInBacket[0][2]*boxesInBacket[0][3]
        sumAreaPos = 0
        sumAreaNeg = 0
        for i in range(1,len(predictedComponentsInBacket)):
            if predictedComponentsInBacket[i] == 'android.widget.TextView' \
            or predictedComponentsInBacket[i] == 'android.widget.ImageView':
                sumAreaPos+= (boxesInBacket[i][2]*boxesInBacket[i][3])
            else:
                sumAreaNeg+= (boxesInBacket[i][2]*boxesInBacket[i][3])
        if sumAreaPos>sumAreaNeg and (baseArea/imageArea<0.5):
            return True
        else:
            return False
    else:
        return False
    
# Case added manually edit text classified wrong.
# Try to find another solution as (7sah mtaif)
def specialCaseRongEditText(boxesInBacket,textsInBacket,predictedComponentsInBacket,imgW):
    if predictedComponentsInBacket[0] == 'android.widget.EditText':
        if boxesInBacket[0][2] < 0.2*imgW: # To handle fatafet :D
            return False
        for i in range(1,len(predictedComponentsInBacket)):
            if (predictedComponentsInBacket[i] == 'android.widget.ImageButton'):
                return False
        return True
    else:
        return True

    
def buttonsKeyWords(boxesFiltered,textsFiltered,predictedComponentsFiltered,imageCopy):
    keyStrings=['register','login','log','create','forget','change password','change picture','submit','buy']
    for i in range(len(textsFiltered)):
        if boxesFiltered[i][1] < (imageCopy.shape[0]/3.0):
            continue
        lowerStrings=textsFiltered[i].lower().split()
        for j in range(len(keyStrings)):
            if Utils.isSliceList(keyStrings[j].split(),lowerStrings):
                predictedComponentsFiltered[i]='android.widget.Button'
                break
        
def changeEditTextToTextViewInCaseNoButtons(predictedComponentsFiltered):
    for i in range(len(predictedComponentsFiltered)):
        if predictedComponentsFiltered[i]== 'android.widget.EditText':
            predictedComponentsFiltered[i] = 'android.widget.TextView'
    
def changeProgressBarVerticalToRadioButtonAndDeleteHorizontal(boxesFiltered,textsFiltered,predictedComponentsFiltered,img):
    boxesFilteredNew = []
    textsFilteredNew = []
    predictedComponentsFilteredNew = []
    for i in range(len(predictedComponentsFiltered)):
        if predictedComponentsFiltered[i]== 'android.widget.ProgressBarHorizontal':
            continue
        if predictedComponentsFiltered[i]== 'android.widget.ProgressBarVertical'\
            and boxesFiltered[i][2]<img.shape[1]/2 and boxesFiltered[i][3]<img.shape[0]/2:
            predictedComponentsFiltered[i] = 'android.widget.RadioButton'
        elif predictedComponentsFiltered[i]== 'android.widget.ProgressBarVertical':
            continue
        predictedComponentsFilteredNew.append(predictedComponentsFiltered[i])
        boxesFilteredNew.append(boxesFiltered[i])
        textsFilteredNew.append(textsFiltered[i])
    return boxesFilteredNew,textsFilteredNew,predictedComponentsFilteredNew
            
def checkSeekProgress(boxesInBacket,imageCopy):
    croppedImage = imageCopy[max(0,boxesInBacket[0][1] - margin):min(imageCopy.shape[0],boxesInBacket[0][1] + boxesInBacket[0][3] + margin), max(boxesInBacket[0][0] - margin,0):min(imageCopy.shape[1],boxesInBacket[0][0] + boxesInBacket[0][2] + margin)]
    colors = Image.fromarray(croppedImage).convert('RGB').getcolors()
    if colors != None:
        for i in range(len(colors)):  # Gray above (192,192,192)
            if colors[i][1][0] < 192 or colors[i][1][1] < 192 or colors[i][1][2] < 192:
                return True
    return False

def neglect(boxesInBacket,textsInBacket,predictedComponentsInBacket,imageCopy):
    # Case very thin image.
    if (boxesInBacket[0][3]<heightThrshold1 or\
        (boxesInBacket[0][3]<heightThrshold2 and boxesInBacket[0][2]>imageCopy.shape[1]*0.6)) \
        and predictedComponentsInBacket[0] == 'android.widget.ImageView':
        return True
    # Case wrong line classified as SeekBar or ProgressBar.
    if (predictedComponentsInBacket[0] == 'android.widget.SeekBar' \
        and not checkSeekProgress(boxesInBacket,imageCopy)):
        return True
    # Case textView that don't have text so wrong classification.
    if predictedComponentsInBacket[0] == 'android.widget.TextView' and \
        textsInBacket[0] == '':
        return True
    # Taaief ll edit text aly kan ta3bny whwa fasl.
    if predictedComponentsInBacket[0] == 'android.widget.EditText' and boxesInBacket[0][3]+2*margin < heightThrshold2:
        return True

    ''' # may be uncommented if needed
    croppedImage = imageCopy[boxesInBacket[0][1]:boxesInBacket[0][1] + boxesInBacket[0][3] , boxesInBacket[0][0]:boxesInBacket[0][0] + boxesInBacket[0][2]]
    numTotalPixel = croppedImage.shape[0] * croppedImage.shape[1]
    # Case 7dod same color.
    numWhitePixel=0
    valueToCompare = numpy.sum(croppedImage[0][0])
    for i in range(croppedImage.shape[1]):
        for j in range(croppedImage.shape[0]):
            if numpy.sum(croppedImage[j][i]) == valueToCompare:
                numWhitePixel+=1
    if numWhitePixel/numTotalPixel >= 1 and boxesInBacket[0][3]+2*margin<heightThrshold2 \
     and predictedComponentsInBacket[0] != 'android.widget.SeekBar' and boxesInBacket[0][2]+2*margin>imageCopy.shape[0]*0.6:
        return True
    '''
    return False
    
def stopEntering(boxesInBacket,textsInBacket,predictedComponentsInBacket, \
                 boxesFiltered,textsFiltered,predictedComponentsFiltered,imageCopy,model,invVocab):
    if (predictedComponentsInBacket[0] != 'android.widget.ImageView' \
    and predictedComponentsInBacket[0] != 'android.widget.TextView'\
    and specialCaseRongEditText(boxesInBacket,textsInBacket,predictedComponentsInBacket,imageCopy.shape[1]))\
    or specialCaseImageText(boxesInBacket,textsInBacket,predictedComponentsInBacket,imageCopy) \
    or len(predictedComponentsInBacket)==1:
        if not neglect(boxesInBacket,textsInBacket,predictedComponentsInBacket,imageCopy):
            boxesFiltered.append(boxesInBacket[0])
            textsFiltered.append(textsInBacket[0])
            predictedComponentsFiltered.append(predictedComponentsInBacket[0])
        return True
    else:
        return False
    
def filterEachBacket(boxesInBacket,textsInBacket,predictedComponentsInBacket, \
                         boxesFiltered,textsFiltered,predictedComponentsFiltered,imageCopy,model,invVocab):
    stop=stopEntering(boxesInBacket,textsInBacket,predictedComponentsInBacket, \
                 boxesFiltered,textsFiltered,predictedComponentsFiltered,imageCopy,model,invVocab)
    if stop==True:
        return
    # Backet the rest of array.
    boxesInBackets,textsInBackets,predictedComponentsInBackets=\
    backetOverlappingBoxes(boxesInBacket[1:len(boxesInBacket)],textsInBacket[1:len(boxesInBacket)],predictedComponentsInBacket[1:len(boxesInBacket)])
    for i in range(len(boxesInBackets)):
        filterEachBacket(boxesInBackets[i],textsInBackets[i],predictedComponentsInBackets[i], \
                         boxesFiltered,textsFiltered,predictedComponentsFiltered,imageCopy,model,invVocab)
        
def getFirstUnvisitedIndex(visited):
    for i in range(len(visited)):
        if visited[i]== False:
            return i
    return -1

def backetOverlappingBoxes(boxesRemovingManual,textsRemovingManual,predictedComponentsRemovingManual):
    boxesInBackets = []
    textsInBackets = []
    predictedComponentsInBackets = []
    visited = [False for i in range(len(boxesRemovingManual))]
    indexUnvisited = 0
    while(indexUnvisited!=-1):
        backetBoxes=[]
        backetTexts=[]
        backetPredicted=[]
        backetBoxes.append(boxesRemovingManual[indexUnvisited])
        backetTexts.append(textsRemovingManual[indexUnvisited])
        backetPredicted.append(predictedComponentsRemovingManual[indexUnvisited])
        visited[indexUnvisited]=True
        for i in range(indexUnvisited+1,len(boxesRemovingManual)):
            if visited[i] == False and Utils.iou(boxesRemovingManual[indexUnvisited],boxesRemovingManual[i])>0:
                visited[i] = True
                backetBoxes.append(boxesRemovingManual[i])
                backetTexts.append(textsRemovingManual[i])
                backetPredicted.append(predictedComponentsRemovingManual[i])
        boxesInBackets.append(backetBoxes)
        textsInBackets.append(backetTexts)
        predictedComponentsInBackets.append(backetPredicted)
        indexUnvisited=getFirstUnvisitedIndex(visited)
    return boxesInBackets,textsInBackets,predictedComponentsInBackets

def removenonEditTextThatAddedManually(boxes,texts,addedManuallyBool,predictedComponents):
    boxesRemovingManual=[]
    textsRemovingManual=[]
    predictedComponentsRemovingManual=[]
    for i in range(len(addedManuallyBool)):
        if not (addedManuallyBool[i]==True and predictedComponents[i] != 'android.widget.EditText'):
            boxesRemovingManual.append(boxes[i])
            textsRemovingManual.append(texts[i])
            predictedComponentsRemovingManual.append(predictedComponents[i])
    return boxesRemovingManual,textsRemovingManual,predictedComponentsRemovingManual

