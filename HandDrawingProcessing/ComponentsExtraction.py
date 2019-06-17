import sys
sys.path.append('../')
import HandDrawingProcessing.BoxesExtraction as BoxesExtraction
import HandDrawingProcessing.TextExtraction as TextExtraction
import Utils

def getFirstTextBoxAndRatio(boxesInBacket,textsInBacket):
    text = ""
    for i in range(len(textsInBacket)):
        if textsInBacket[i] != "":
            return textsInBacket[i],Utils.iou(boxesInBacket[0],boxesInBacket[i]),i
    return text,1,0

def filterComponentsAndPredict(allBoxes,texts):
    predictedComonents = []
    filteredBoxes = [] 
    filteredTexts = []
    boxesInBackets,textsInBackets = backetOverlappingBoxes(allBoxes,texts)
    for i in range(len(boxesInBackets)):
        if textsInBackets[i][0] != "":
            filteredBoxes.append(boxesInBackets[i][0])
            filteredTexts.append(textsInBackets[i][0])
            predictedComonents.append("android.widget.TextView")
        elif len(boxesInBackets[i])==1:
            filteredBoxes.append(boxesInBackets[i][0])
            filteredTexts.append(textsInBackets[i][0])
            if boxesInBackets[i][0][3]/boxesInBackets[i][0][2] < 0.3:
                predictedComonents.append("android.widget.EditText")
            else:
                predictedComonents.append("android.widget.ImageView")
        else:
            text,textAreaRatio,textIndex = getFirstTextBoxAndRatio(boxesInBackets[i],textsInBackets[i])
            filteredTexts.append(text)
            #print(text,textAreaRatio)
            if textAreaRatio < 0.9 and text != "":
                predictedComonents.append("android.widget.Button")
                filteredBoxes.append(boxesInBackets[i][0])
            elif text != "":
                predictedComonents.append("android.widget.TextView")
                filteredBoxes.append(boxesInBackets[i][textIndex])
            else: # A7tyaty ma7sltsh.
                predictedComonents.append("android.widget.ImageView")
                filteredBoxes.append(boxesInBackets[i][0])
    return filteredBoxes,filteredTexts,predictedComonents

# Extract the boxes and text from given image -extracted components-.
def extractComponents(image,image4Txt,appName): # TODO: Remove appName.
    # TODO: Uncomment after testing and delete the line after this.
    #extractedText, textPositions= TextExtraction.extractText(image4Txt) # List of strings coreesponding to the text in each box.
    extractedTexts,textPositions = getFromAppName(appName)
    extratctedBoxes,extractedTexts = BoxesExtraction.extractBoxes(image, extractedTexts, textPositions)
    myImageBox = extratctedBoxes[0]
    extratctedBoxes,extractedTexts,predictedComponents = filterComponentsAndPredict(extratctedBoxes[1:len(extratctedBoxes)],extractedTexts[1:len(extratctedBoxes)])
    return extratctedBoxes,extractedTexts,predictedComponents,myImageBox

def getFirstUnvisitedIndex(visited):
    for i in range(len(visited)):
        if visited[i]== False:
            return i
    return -1

def backetOverlappingBoxes(boxes,texts):
    boxesInBackets = []
    textsInBackets = []
    visited = [False for i in range(len(boxes))]
    indexUnvisited = 0
    while(indexUnvisited!=-1):
        backetBoxes=[]
        backetTexts=[]
        backetBoxes.append(boxes[indexUnvisited])
        backetTexts.append(texts[indexUnvisited])
        visited[indexUnvisited]=True
        for i in range(indexUnvisited+1,len(boxes)):
            if visited[i] == False and Utils.iou(boxes[indexUnvisited],boxes[i])>0:
                visited[i] = True
                backetBoxes.append(boxes[i])
                backetTexts.append(texts[i])
        boxesInBackets.append(backetBoxes)
        textsInBackets.append(backetTexts)
        indexUnvisited=getFirstUnvisitedIndex(visited)
    return boxesInBackets,textsInBackets

# I neglect it as already handled before. may be needed.
def getAllText(boxesInBacket,textsInBacket):
    boxesInBacketCopy = boxesInBacket
    textsInBacketCopy = textsInBacket
    boxesInBacketCopy,textsInBacketCopy = zip(*sorted(zip(boxesInBacketCopy,textsInBacketCopy), key=lambda x: x[0][0],reverse=False))
    text = ""
    for i in range(len(textsInBacketCopy)):
        if textsInBacketCopy[i] != "":
            text += (textsInBacketCopy[i] + " ")
    return text

# For testing.
appDict = {
"loadingN.jpg":
(['S', 'WIL'],
[[426, 600, 98, 124], [484, 614, 278, 85]]),
"locationN.jpg":
(['Whe', 're', 'to?', 'ON'],
[[174, 407, 144, 109], [320, 403, 92, 111], [444, 401, 142, 99], [396, 544, 84, 43]]),
"logoutN.jpg":
(['LOO', 'Log', 'out', 'all', '1', 'get', 'it'],
[[939, 158, 192, 166], [920, 162, 227, 153], [1178, 162, 217, 69], [864, 438, 139, 112], [509, 456, 90, 90], [1226, 754, 170, 64], [1457, 758, 56, 49]]),
"twitterN.jpg":
(['HOME'],
[[396, 116, 295, 106]]),
"loginN.jpg":
(['Logm', 'Name', 'Email', 'Save'],
[[87, 53, 37, 22], [27, 104, 31, 11], [23, 134, 32, 12], [195, 203, 32, 12]]),
 "login2N.jpg":
(['Login', 'Email', 'Password', 'Log', 'in'],
[[677, 745, 219, 143], [330, 1015, 204, 94], [286, 1165, 360, 103], [832, 1516, 102, 80], [949, 1522, 59, 46]]),
 "login3N.jpg":
     (['LOGTN', 'Name', 'Register', 'EMaiL:', 'Pass:', 'LOGIM', 'Log', 'LOg', 'out'],
[[508, 307, 348, 140], [151, 636, 188, 74], [953, 640, 334, 99], [167, 755, 224, 51], [167, 887, 178, 46], [504, 1061, 274, 110], [485, 1296, 155, 87], [326, 1474, 122, 72], [482, 1482, 138, 45]])
        }
def getFromAppName(appName):
    return appDict[appName][0],appDict[appName][1]
# 1126,754,287,64