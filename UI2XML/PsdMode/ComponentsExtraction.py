import sys
sys.path.append('../')
import ScreenShotMode.TextExtraction as TextExtraction
import ModelClassification.Model as Model
import Utils
import Preprocessing
import numpy as np
import cv2
import Constants


def boxArea(x):
    return x[2]*x[3]

def extractBoxesFromLayers(psd):
    boxes = []
    for layer in psd.layers:
        boxes.append([layer.bbox.x1, layer.bbox.y1,layer.bbox.width,layer.bbox.height])
    boxes.sort(key= boxArea,reverse=True)
    return boxes[1:]

# Extract the boxes and text from given image -extracted components- and predict them.
def extractComponentsAndPredict(imagePsd,imageCopy,imageXML,model,invVocab):
    extratctedBoxes= extractBoxesFromLayers(imagePsd)
    extractedText=[] # List of strings coreesponding to the text in each box.
    pedictedComponents=[]
    # Note: If the box doesn't contain text its index in the extractedText list should contains empty string.
    height=imageCopy.shape[0]
    width=imageCopy.shape[1]
    for x,y,w,h in extratctedBoxes:
        features = []
        croppedImage = imageCopy[max(0,y):min(height,y + h), max(x,0):min(width,x + w)]
        resizedImg = cv2.resize(croppedImage, (150,150))
        croppedImageColor = imageXML[max(0,y):min(height,y + h), max(x,0):min(width,x + w)]
        text = TextExtraction.extractText(croppedImage)
        textFeature = 0
        if text != "":
            textFeature = 1
        features += Utils.getNoOfColorsAndBackGroundRGB(croppedImageColor)
        features.append(textFeature)
        shpeFeatuesList,slopedLines = extractShapeFeatures(croppedImage,resizedImg)
        features += shpeFeatuesList
        ifSquare = features[-6]
        circularity = features[-5]
        prediction = Model.makeAprediction(invVocab,np.array(features,dtype='float32'),croppedImage,model)
        prediction = handleRadioAndCheck(prediction,[x,y,w,h],imageCopy,ifSquare,circularity,slopedLines,features,invVocab,model)
        pedictedComponents.append(prediction)
        extractedText.append(TextExtraction.extractText(croppedImage))
        
    if ('android.widget.Button' not in pedictedComponents \
       and 'android.widget.ImageButton' not in pedictedComponents) \
    and 'android.widget.EditText' in pedictedComponents:
        changeEditTextToTextViewInCaseNoButtons(pedictedComponents,extratctedBoxes)    
    buttonsKeyWords(extratctedBoxes,extractedText,pedictedComponents,imageCopy)
    changeUnDesiredComponents(pedictedComponents)
    return extratctedBoxes,extractedText,pedictedComponents

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


def handleRadioAndCheck(prediction,box,imageCopy,ifSquare,circularity,slopedLines,features,invVocab,model):
    if ifSquare:
        if slopedLines > 2 and slopedLines < 4:
            return 'android.widget.CheckBox'
    if circularity != 0 and (prediction == 'android.widget.ImageView' or prediction == 'android.widget.ImageButton'):
        x,y,w,h = box
        marginNew = 5
        croppedImage = imageCopy[max(0,y - marginNew):min(imageCopy.shape[0],y + h + marginNew), max(x - marginNew,0):min(imageCopy.shape[1],x + w + marginNew)]
        newPrediction = Model.makeAprediction(invVocab,np.array(features,dtype='float32'),croppedImage,model)
        if newPrediction == 'android.widget.RadioButton':
            return 'android.widget.RadioButton'
    return prediction

def extractShapeFeatures(img,resizedImg):
    allShapeFeatures = []
    edges,_=Preprocessing.preProcessEdges(img)
    edgesResized,grayImgResized = Preprocessing.preProcessEdges(resizedImg)
    # normalizedNoOfEdges, normalizedNoOfLines, maxHorzLineLength/150, noOfSlopedLines/noOfLines
    linesEdgeFeatures =  Utils.getLinesEdgesFeatures(edgesResized)
    allShapeFeatures += linesEdgeFeatures
    slopedLines = linesEdgeFeatures[-1]
    # widthResizingRatio, hightResizingRatio
    allShapeFeatures += Utils.getResizeRatios(img)
    # LBP hist, HOG hist(hist of gradients 8 directions), 5 gray hist range.
    allShapeFeatures += Utils.describeLBP(grayImgResized)
    allShapeFeatures += Utils.descripeHog(grayImgResized)
    allShapeFeatures += Utils.describe5Gray(grayImgResized)
    (_, contours , _) = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    if len(contours) == 0:
      Constants.noContors+=1
      print("noContors: ",str(Constants.noContors))
      return allShapeFeatures+[0,0,0,0,0,0]
    cnt = max(contours, key = cv2.contourArea)
    # ifSquare, circularity, noOfVerNormalized, areaCntRatio, perCntRatio, aspectRatio
    allShapeFeatures += Utils.detectShapeAndFeature(cnt)
    return allShapeFeatures,slopedLines

def changeUnDesiredComponents(pedictedComponents):
    for i in range(len(pedictedComponents)):
        if pedictedComponents[i]== 'android.widget.NumberPicker' or\
        pedictedComponents[i] =='android.widget.ProgressBarHorizontal' or\
        pedictedComponents[i] =='android.widget.ProgressBarVertical' or\
        pedictedComponents[i] =='android.widget.RatingBar':
            pedictedComponents[i] = 'android.widget.ImageView'
        elif pedictedComponents[i] =='android.widget.ToggleButton':
            pedictedComponents[i] = 'android.widget.Switch'
        elif pedictedComponents[i] =='android.widget.Spinner':
            pedictedComponents[i] = 'android.widget.ImageButton'