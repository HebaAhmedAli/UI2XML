import sys
sys.path.append('../')
import ScreenShotMode.BoxesExtraction as BoxesExtraction
import ScreenShotMode.TextExtraction as TextExtraction
import ModelClassification.Model as Model
from PIL import Image
import Utils
import Preprocessing
import numpy as np
import cv2
import Constants
import time
from multiprocessing import Process,Manager
import math

heightThrshold1 = 20
heightThrshold2 = 40
margin = 10

def extractFeatures(image,imageCopy,imageXML,extratctedBoxesPart,featuresProcesses,index):
    height=image.shape[0]
    width=image.shape[1]
    for x,y,w,h in extratctedBoxesPart:
        croppedImage = imageCopy[max(0,y - margin):min(height,y + h + margin), max(x - margin,0):min(width,x + w + margin)]
        text = TextExtraction.extractText(croppedImage)
        croppedImageColor = imageXML[max(0,y):min(height,y + h), max(x,0):min(width,x + w)]
        resizedImg = cv2.resize(croppedImage, (150,150))
        colorFeatures = Utils.getNoOfColorsAndBackGroundRGB(croppedImageColor)
        edgesResized,grayImgResized = Preprocessing.preProcessEdges(resizedImg)
        # normalizedNoOfEdges, normalizedNoOfLines, maxHorzLineLength/150, noOfSlopedLines/noOfLines
        linesEdgeFeatures =  Utils.getLinesEdgesFeatures(edgesResized)
        resizeRatios = Utils.getResizeRatios(croppedImage)
        hogFeature = Utils.descripeHog(grayImgResized)
        gray5Feature = Utils.describe5Gray(grayImgResized)
        lbpFeature = Utils.describeLBP(grayImgResized)
        featuresProcesses[index]=[text,colorFeatures,linesEdgeFeatures,resizeRatios,hogFeature,gray5Feature,lbpFeature]
        index+=1
    
        
def createProcess(image,imageCopy,imageXML,extratctedBoxesPart,featuresProcesses,index):
    process = Process(target=extractFeatures, args=(image,imageCopy,imageXML,extratctedBoxesPart,featuresProcesses,index))
    return (process,index)

# Extract the boxes and text from given image -extracted components- and predict them.
def extractComponentsAndPredict(image,imageCopy,imageXML,model,invVocab):
    start0 = time.time()
    extratctedBoxes,addedManuallyBool=BoxesExtraction.extractBoxes(image)
    print("timeBoxesExtraction = ",time.time()-start0)
    extractedText=[] # List of strings coreesponding to the text in each box.
    pedictedComponents=[]
    # Note: If the box doesn't contain text its index in the extractedText list should contains empty string.
    timeExtractText = time.time()
    manager=Manager()
    # Initialize the vectors of each image with empty vector(this vector is shared between processes)
    featuresProcesses=manager.list()
    for i in range(len(extratctedBoxes)):
        featuresProcesses.append([])
    step = int(math.ceil(len(extratctedBoxes)/float(Constants.PROCESSES_NO)))
    processes = [createProcess(image,imageCopy,imageXML,extratctedBoxes[i*step:min(i*step+step,len(extratctedBoxes))],featuresProcesses,i*step) for i in range(Constants.PROCESSES_NO)]
    for p in processes:
        p[0].start()
    for p in processes:
        p[0].join()
        p[0].terminate()
    print("time timeExtractText = ",time.time()-timeExtractText)
    # featuresProcesses[i][0] features
    # featuresProcesses[i][1] ifSquare
    # featuresProcesses[i][2] circularity
    # featuresProcesses[i][3] slopedLines
    # featuresProcesses[i][4] text
    height=image.shape[0]
    width=image.shape[1]
    timePrediction = time.time()
    for i in range(len(extratctedBoxes)):
        features = []
        x,y,w,h = extratctedBoxes[i]
        croppedImage = imageCopy[max(0,y - margin):min(height,y + h + margin), max(x - margin,0):min(width,x + w + margin)]
        resizedImg = cv2.resize(croppedImage, (150,150))
        textFeature = 0
        text = featuresProcesses[i][0]
        if text != "":
            textFeature = 1
        features += featuresProcesses[i][1]
        features.append(textFeature)
        shpeFeatuesList,slopedLines = extractShapeFeatures(croppedImage,resizedImg,featuresProcesses[i])
        features += shpeFeatuesList
        ifSquare = features[-6]
        circularity = features[-5]
        prediction = Model.makeAprediction(invVocab,np.array(features,dtype='float32'),croppedImage,model)
        prediction = handleRadioAndCheck(prediction,[x,y,w,h],imageCopy,ifSquare,circularity,slopedLines,features,invVocab,model)
        pedictedComponents.append(prediction)
        extractedText.append(text)
    print("Time for features and prediction = ",time.time()-timePrediction)
    del featuresProcesses
    return extratctedBoxes,extractedText,addedManuallyBool,pedictedComponents

def handleRadioAndCheck(prediction,box,imageCopy,ifSquare,circularity,slopedLines,features,invVocab,model):
    if ifSquare:
        if slopedLines > 2 and slopedLines < 4:
            return 'android.widget.CheckBox'
    '''
    if prediction == 'android.widget.CheckBox' and (not(slopedLines > 2 and slopedLines < 4) or not ifSquare):
        return 'android.widget.ImageView'
    '''
    if circularity != 0 and (prediction == 'android.widget.ImageView' or prediction == 'android.widget.ImageButton'):
        x,y,w,h = box
        marginNew = 5
        croppedImage = imageCopy[max(0,y - marginNew):min(imageCopy.shape[0],y + h + marginNew), max(x - marginNew,0):min(imageCopy.shape[1],x + w + marginNew)]
        newPrediction = Model.makeAprediction(invVocab,np.array(features,dtype='float32'),croppedImage,model)
        if newPrediction == 'android.widget.RadioButton':
            return 'android.widget.RadioButton'
    return prediction

def extractShapeFeatures(img,resizedImg,featuresProcessesI):
    allShapeFeatures = []
    edges,_=Preprocessing.preProcessEdges(img)
    edgesResized,grayImgResized = Preprocessing.preProcessEdges(resizedImg)
    # normalizedNoOfEdges, normalizedNoOfLines, maxHorzLineLength/150, noOfSlopedLines/noOfLines
    allShapeFeatures += featuresProcessesI[2]
    slopedLines = featuresProcessesI[2][-1]
    # widthResizingRatio, hightResizingRatio
    allShapeFeatures += featuresProcessesI[3]
    # LBP hist, HOG hist(hist of gradients 8 directions), 5 gray hist range.
    allShapeFeatures += featuresProcessesI[6]
    allShapeFeatures += featuresProcessesI[4]
    allShapeFeatures += featuresProcessesI[5]
    (_, contours , _) = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    if len(contours) == 0:
      Constants.noContors+=1
      print("noContors: ",str(Constants.noContors))
      return allShapeFeatures+[0,0,0,0,0,0]
    cnt = max(contours, key = cv2.contourArea)
    # ifSquare, circularity, noOfVerNormalized, areaCntRatio, perCntRatio, aspectRatio
    allShapeFeatures += Utils.detectShapeAndFeature(cnt)
    return allShapeFeatures,slopedLines
        
def filterComponents(boxes, texts ,addedManuallyBool ,predictedComponents,imageCopy):
    boxesRemovingManual,textsRemovingManual,predictedComponentsRemovingManual= \
    removenonEditTextThatAddedManually(boxes,texts,addedManuallyBool,predictedComponents)
    
    boxesInBackets,textsInBackets,predictedComponentsInBackets \
    =backetOverlappingBoxes(boxesRemovingManual,textsRemovingManual,predictedComponentsRemovingManual)
    
    boxesFiltered = []
    textsFiltered = []
    predictedComponentsFiltered = []
    for i in range(len(boxesInBackets)):
        filterEachBacket(boxesInBackets[i],textsInBackets[i],predictedComponentsInBackets[i], \
                         boxesFiltered,textsFiltered,predictedComponentsFiltered,imageCopy)
    if ('android.widget.Button' not in predictedComponentsFiltered \
       and 'android.widget.ImageButton' not in predictedComponentsFiltered) \
    and 'android.widget.EditText' in predictedComponentsFiltered:
        changeEditTextToTextViewInCaseNoButtons(predictedComponentsFiltered,boxesFiltered)    
    if 'android.widget.ProgressBarVertical' in predictedComponentsFiltered\
        or 'android.widget.ProgressBarHorizontal' in predictedComponentsFiltered: # TODO : Try to find alternative sol.
        boxesFiltered,textsFiltered,predictedComponentsFiltered = DeleteVerticalAndHorizontalProgressBar(boxesFiltered,textsFiltered,predictedComponentsFiltered,imageCopy)
    buttonsKeyWords(boxesFiltered,textsFiltered,predictedComponentsFiltered,imageCopy) # TODO : Comment in case change.
    changeUnDesiredComponents(predictedComponentsFiltered)
    return boxesFiltered,textsFiltered,predictedComponentsFiltered

# Case image containing all image or text inside.
def specialCaseImageText(boxesInBacket,textsInBacket,predictedComponentsInBacket,imageCopy):
    imageArea=imageCopy.shape[0]*imageCopy.shape[1]
    if predictedComponentsInBacket[0] == 'android.widget.ImageView' \
    or predictedComponentsInBacket[0] == 'android.widget.TextView':
        baseArea = boxesInBacket[0][2]*boxesInBacket[0][3]
        sumAreaText = 0 
        sumAreaImg = 0
        sumAreaNeg = 0
        for i in range(1,len(predictedComponentsInBacket)):
            if predictedComponentsInBacket[i] == 'android.widget.TextView':
                sumAreaText+= (boxesInBacket[i][2]*boxesInBacket[i][3])
            elif predictedComponentsInBacket[i] == 'android.widget.ImageView':
                sumAreaImg+= (boxesInBacket[i][2]*boxesInBacket[i][3])
            else:
                sumAreaNeg+= (boxesInBacket[i][2]*boxesInBacket[i][3])
        if sumAreaText+sumAreaImg>sumAreaNeg and baseArea/imageArea<0.3 and predictedComponentsInBacket[0] == 'android.widget.TextView':
            return True
        elif sumAreaImg>sumAreaText and sumAreaText+sumAreaImg>sumAreaNeg and baseArea/imageArea<0.3 and predictedComponentsInBacket[0] == 'android.widget.ImageView':
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
        textViews = 0
        seekBarORImg = 0
        unDesired = 0
        for i in range(1,len(predictedComponentsInBacket)):
            if (predictedComponentsInBacket[i] == 'android.widget.TextView'):
                textViews += 1
            elif (predictedComponentsInBacket[i] == 'android.widget.SeekBar' or predictedComponentsInBacket[i] == 'android.widget.ImageView') and boxesInBacket[i][2]/boxesInBacket[0][2]>= 0.8:
                predictedComponentsInBacket[i] = 'android.widget.ImageView'
                seekBarORImg += 1
            else:
                unDesired += 1
        if textViews == 1 and  seekBarORImg == 1 and unDesired == 0:
            return True
        # Check Change to button.
        if len(boxesInBacket)==1:
            keyStrings=['register','login','log','create','forget','change password','change picture','submit','buy']
            lowerStrings=textsInBacket[0].lower().split()
            for j in range(len(keyStrings)):
                if Utils.isSliceList(keyStrings[j].split(),lowerStrings):
                    predictedComponentsInBacket[0]='android.widget.Button'
                    return True
            if textsInBacket[0]!="":
                 predictedComponentsInBacket[0]='android.widget.TextView'
                 return True
            else:
                predictedComponentsInBacket[0]='android.widget.ImageView'
                return True
        return False
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
        
def changeEditTextToTextViewInCaseNoButtons(predictedComponentsFiltered,boxesFiltered):
    for i in range(len(predictedComponentsFiltered)):
        if predictedComponentsFiltered[i]== 'android.widget.EditText':
            predictedComponentsFiltered[i] = 'android.widget.TextView'
            boxesFiltered[i][2] = int(boxesFiltered[i][2] *0.5)
    
def DeleteVerticalAndHorizontalProgressBar(boxesFiltered,textsFiltered,predictedComponentsFiltered,img):
    boxesFilteredNew = []
    textsFilteredNew = []
    predictedComponentsFilteredNew = []
    for i in range(len(predictedComponentsFiltered)):
        if predictedComponentsFiltered[i]== 'android.widget.ProgressBarHorizontal':
            continue
        elif predictedComponentsFiltered[i]== 'android.widget.ProgressBarVertical':
            continue
        predictedComponentsFilteredNew.append(predictedComponentsFiltered[i])
        boxesFilteredNew.append(boxesFiltered[i])
        textsFilteredNew.append(textsFiltered[i])
    return boxesFilteredNew,textsFilteredNew,predictedComponentsFilteredNew
            
def checkSeekProgress(predictedComponentsInBacket,boxesInBacket,imageCopy):
    if boxesInBacket[0][2]/imageCopy.shape[1] < 0.2:
        predictedComponentsInBacket[0] = 'android.widget.Switch'
        return True
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
        and not checkSeekProgress(predictedComponentsInBacket,boxesInBacket,imageCopy)):
        return True

    # Case textView that don't have text so wrong classification.
    if predictedComponentsInBacket[0] == 'android.widget.TextView' and \
        textsInBacket[0] == '':
        return True
    
    if predictedComponentsInBacket[0] == 'android.widget.Button' and  boxesInBacket[0][3]/boxesInBacket[0][2]< 0.1 and \
            boxesInBacket[0][2]/imageCopy.shape[1] and textsInBacket[0] == '':
        return True
    
    # Taaief ll edit text aly kan ta3bny whwa fasl.
    if predictedComponentsInBacket[0] == 'android.widget.EditText' and boxesInBacket[0][3]+2*margin < heightThrshold2:
        return True
   
    return False
    
# and specialCaseButton(boxesInBacket,textsInBacket,predictedComponentsInBacket)
def stopEntering(boxesInBacket,textsInBacket,predictedComponentsInBacket, \
                 boxesFiltered,textsFiltered,predictedComponentsFiltered,imageCopy):
    specialRongEdit = specialCaseRongEditText(boxesInBacket,textsInBacket,predictedComponentsInBacket,imageCopy.shape[1])
    if (predictedComponentsInBacket[0] != 'android.widget.ImageView' \
    and predictedComponentsInBacket[0] != 'android.widget.TextView'\
    and specialRongEdit)\
    or specialCaseImageText(boxesInBacket,textsInBacket,predictedComponentsInBacket,imageCopy) \
    or len(predictedComponentsInBacket)==1:
        if not neglect(boxesInBacket,textsInBacket,predictedComponentsInBacket,imageCopy) and specialRongEdit:
            boxesFiltered.append(boxesInBacket[0])
            textsFiltered.append(textsInBacket[0])
            predictedComponentsFiltered.append(predictedComponentsInBacket[0])
        return True
    else:
        return False
    
def filterEachBacket(boxesInBacket,textsInBacket,predictedComponentsInBacket, \
                         boxesFiltered,textsFiltered,predictedComponentsFiltered,imageCopy):
    stop=stopEntering(boxesInBacket,textsInBacket,predictedComponentsInBacket, \
                 boxesFiltered,textsFiltered,predictedComponentsFiltered,imageCopy)
    if stop==True:
        return
    # Backet the rest of array.
    boxesInBackets,textsInBackets,predictedComponentsInBackets=\
    backetOverlappingBoxes(boxesInBacket[1:len(boxesInBacket)],textsInBacket[1:len(boxesInBacket)],predictedComponentsInBacket[1:len(boxesInBacket)])
    for i in range(len(boxesInBackets)):
        filterEachBacket(boxesInBackets[i],textsInBackets[i],predictedComponentsInBackets[i], \
                         boxesFiltered,textsFiltered,predictedComponentsFiltered,imageCopy)
           
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
            notUnderEachOther = True
            if boxesRemovingManual[indexUnvisited][1]<boxesRemovingManual[i][1] and (boxesRemovingManual[i][1]-boxesRemovingManual[indexUnvisited][1])>=(boxesRemovingManual[indexUnvisited][3]-5):
                notUnderEachOther = False
            elif boxesRemovingManual[i][1]<boxesRemovingManual[indexUnvisited][1] and (boxesRemovingManual[indexUnvisited][1]-boxesRemovingManual[i][1])>=(boxesRemovingManual[i][3]-5):
                notUnderEachOther = False
            if visited[i] == False and Utils.iou(boxesRemovingManual[indexUnvisited],boxesRemovingManual[i])>0:
                if  notUnderEachOther or predictedComponentsRemovingManual[indexUnvisited]=='android.widget.EditText':
                    visited[i] = True
                    backetBoxes.append(boxesRemovingManual[i])
                    backetTexts.append(textsRemovingManual[i])
                    backetPredicted.append(predictedComponentsRemovingManual[i])
        boxesInBackets.append(backetBoxes)
        textsInBackets.append(backetTexts)
        predictedComponentsInBackets.append(backetPredicted)
        indexUnvisited=getFirstUnvisitedIndex(visited)
    # print(predictedComponentsInBackets)
    # print('\n')
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

def changeUnDesiredComponents(pedictedComponents):
    for i in range(len(pedictedComponents)):
        if pedictedComponents[i]== 'android.widget.NumberPicker' or\
        pedictedComponents[i] =='android.widget.RatingBar':
            pedictedComponents[i] = 'android.widget.ImageView'
        elif pedictedComponents[i] =='android.widget.ToggleButton':
            pedictedComponents[i] = 'android.widget.Button'
        elif pedictedComponents[i] =='android.widget.Spinner':
            pedictedComponents[i] = 'android.widget.ImageButton'