import sys
sys.path.append('../')
import ComponentsExtraction.BoxesExtraction as BoxesExtraction
import ComponentsExtraction.TextExtraction as TextExtraction
import ModelClassification.Model as Model
import Utils

# Extract the boxes and text from given image -extracted components- and predict them.
def extractComponentsAndPredict(image,imageCopy,model,invVocab):
    extratctedBoxes,addedManuallyBool=BoxesExtraction.extractBoxes(image)
    extractedText=[] # List of strings coreesponding to the text in each box.
    pedictedComponents=[]
    # Note: If the box doesn't contain text its index in the extractedText list should contains empty string.
    margin = 10
    height=image.shape[0]
    width=image.shape[1]
    for x,y,w,h in extratctedBoxes:
        croppedImage = imageCopy[max(0,y - margin):min(height,y + h + margin), max(x - margin,0):min(width,x + w + margin)]
        pedictedComponents.append(Model.makeAprediction(invVocab,croppedImage,model))
        extractedText.append(TextExtraction.extractText(croppedImage))
    return extratctedBoxes,extractedText,addedManuallyBool,pedictedComponents


        
def filterComponents(boxes, texts ,addedManuallyBool ,predictedComponents,imageArea):
    boxesRemovingManual,textsRemovingManual,predictedComponentsRemovingManual= \
    removenonEditTextThatAddedManually(boxes,texts,addedManuallyBool,predictedComponents)
    
    boxesInBackets,textsInBackets,predictedComponentsInBackets \
    =backetOverlappingBoxes(boxesRemovingManual,textsRemovingManual,predictedComponentsRemovingManual)
    
    boxesFiltered = []
    textsFiltered = []
    predictedComponentsFiltered = []
    for i in range(len(boxesInBackets)):
        filterEachBacket(boxesInBackets[i],textsInBackets[i],predictedComponentsInBackets[i], \
                         boxesFiltered,textsFiltered,predictedComponentsFiltered,imageArea)
    return boxesFiltered,textsFiltered,predictedComponentsFiltered

# Case image containing all image or text inside.
def specialCase(boxesInBacket,textsInBacket,predictedComponentsInBacket,imageArea):
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
    
def stopEntering(boxesInBacket,textsInBacket,predictedComponentsInBacket, \
                 boxesFiltered,textsFiltered,predictedComponentsFiltered,imageArea):
    if predictedComponentsInBacket[0] == 'android.widget.EditText' \
    or predictedComponentsInBacket[0] == 'android.widget.Button'\
    or predictedComponentsInBacket[0] == 'android.widget.ImageButton' \
    or predictedComponentsInBacket[0] == 'android.widget.TextView' \
    or len(predictedComponentsInBacket)==1:
        boxesFiltered.append(boxesInBacket[0])
        textsFiltered.append(textsInBacket[0])
        predictedComponentsFiltered.append(predictedComponentsInBacket[0])
        return True
    elif specialCase(boxesInBacket,textsInBacket,predictedComponentsInBacket,imageArea):
        boxesFiltered.append(boxesInBacket[0])
        textsFiltered.append(textsInBacket[0])
        predictedComponentsFiltered.append(predictedComponentsInBacket[0])
        return True
    else:
        return False
    
def filterEachBacket(boxesInBacket,textsInBacket,predictedComponentsInBacket, \
                         boxesFiltered,textsFiltered,predictedComponentsFiltered,imageArea):
    stop=stopEntering(boxesInBacket,textsInBacket,predictedComponentsInBacket, \
                 boxesFiltered,textsFiltered,predictedComponentsFiltered,imageArea)
    if stop==True:
        return
    # Backet the rest of array.
    boxesInBackets,textsInBackets,predictedComponentsInBackets=\
    backetOverlappingBoxes(boxesInBacket[1:len(boxesInBacket)],textsInBacket[1:len(boxesInBacket)],predictedComponentsInBacket[1:len(boxesInBacket)])
    for i in range(len(boxesInBackets)):
        filterEachBacket(boxesInBackets[i],textsInBackets[i],predictedComponentsInBackets[i], \
                         boxesFiltered,textsFiltered,predictedComponentsFiltered,imageArea)
        
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
        
    #print(boxesInBackets,textsInBackets)
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