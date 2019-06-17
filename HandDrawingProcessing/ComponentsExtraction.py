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
        if textsInBackets[i][0] != "" and textsInBackets[i][0] != "x" and textsInBackets[i][0] != "X":
            filteredBoxes.append(boxesInBackets[i][0])
            filteredTexts.append(textsInBackets[i][0])
            predictedComonents.append("android.widget.TextView")
        elif len(boxesInBackets[i])==1:
            filteredBoxes.append(boxesInBackets[i][0])
            filteredTexts.append(textsInBackets[i][0])
            if boxesInBackets[i][0][3]/boxesInBackets[i][0][2] < 0.4:
                predictedComonents.append("android.widget.EditText")
            else:
                predictedComonents.append("android.widget.ImageView")
        else:
            text,textAreaRatio,textIndex = getFirstTextBoxAndRatio(boxesInBackets[i],textsInBackets[i])
            filteredTexts.append(text)
            if textAreaRatio < 0.9 and text != "" and text != "x" and text != "X":
                predictedComonents.append("android.widget.Button")
                filteredBoxes.append(boxesInBackets[i][0])
            elif text != "" and text != "x" and text != "X":
                predictedComonents.append("android.widget.TextView")
                filteredBoxes.append(boxesInBackets[i][textIndex])
            else: # A7tyaty ma7sltsh.
                if boxesInBackets[i][0][3]/boxesInBackets[i][0][2] < 0.4 and text != "x" and text != "X":
                    predictedComonents.append("android.widget.EditText")
                else:
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
    # Translate x and y and handle outside range.
    extratctedBoxesTranslated = []
    i = 0
    while i<len(extratctedBoxes):
        if Utils.checkInsideRange(myImageBox,extratctedBoxes[i]):
            extratctedBoxesTranslated.append([extratctedBoxes[i][0]-myImageBox[0],extratctedBoxes[i][1]-myImageBox[1],extratctedBoxes[i][2],extratctedBoxes[i][3]])
            i += 1
        else:
            extratctedBoxes.pop(i)
            extractedTexts.pop(i)
            predictedComponents.pop(i)
    return extratctedBoxes,extratctedBoxesTranslated,extractedTexts,predictedComponents,myImageBox

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
            if visited[i] == False and Utils.iouSmall(boxes[indexUnvisited],boxes[i])>0.3:
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
[[508, 307, 348, 140], [151, 636, 188, 74], [953, 640, 334, 99], [167, 755, 224, 51], [167, 887, 178, 46], [504, 1061, 274, 110], [485, 1296, 155, 87], [326, 1474, 122, 72], [482, 1482, 138, 45]]),
"login4N.jpg":
(['L03io', 'Name', 'Register', 'EMail:', 'pass:', 'LogIM', 'Farge', 'pass', 'X', 'LogIn', 'Lgout'],
[[480, 448, 359, 135], [134, 786, 188, 74], [945, 774, 330, 91], [146, 903, 232, 55], [154, 1040, 179, 51], [501, 1205, 280, 107], [932, 1209, 178, 79], [1163, 1210, 177, 67], [984, 1415, 240, 181], [519, 1455, 231, 57], [330, 1629, 302, 60]]),
"login7N.jpg":
(['LogIn', 'Name:', 'Emails', 'register', 'Pass:', 'Login', 'forget', 'pass', 'LOG', 'OUT'],
[[414, 150, 255, 120], [145, 401, 248, 97], [60, 526, 304, 119], [800, 529, 318, 83], [115, 701, 196, 86], [310, 922, 211, 105], [858, 906, 238, 131], [1126, 906, 182, 140], [217, 1252, 188, 83], [433, 1227, 179, 84]]),
 "login5N.jpg":
(['L031N', 'name:', 'email:', 'LOgiN', 'Forger', 'pass', 'RegisTer', 'New', 'user', 'you', 'Are', 'welcame'],
[[536, 624, 339, 117], [255, 883, 208, 37], [254, 975, 222, 39], [372, 1182, 258, 73], [756, 1176, 194, 69], [974, 1164, 170, 38], [484, 1354, 330, 66], [948, 1358, 145, 34], [1128, 1342, 174, 28], [544, 1558, 111, 57], [712, 1549, 93, 51], [821, 1544, 296, 71]]),
 "radioAndCheckN.jpg":
(['Sign', 'up', 'Login', 'Name', 'Email', 'DI', 'agree', 'O', 'Play', 'paoBo', 'Obad', 'Plot'],
[[198, 317, 179, 88], [416, 322, 98, 66], [596, 275, 184, 102], [180, 503, 219, 81], [140, 765, 233, 103], [204, 1053, 137, 96], [402, 1077, 202, 99], [815, 1228, 70, 127], [1039, 1240, 139, 113], [460, 1342, 239, 94], [216, 1340, 168, 81], [535, 1585, 186, 101]]),
 "sketch2codeN.png":
(['SigUp', 'Login', 'Name', 'Last', 'Nane', 'Phene', 'C-mail', 'Gufirn', 'Pass', 'werd', 'Pssrd', 'I', 'agree', 'to', 'Tens', 'and', 'Cokol', 'tous', 'SIGN', 'UP'],
[[29, 25, 126, 54], [202, 27, 73, 48], [29, 107, 52, 27], [303, 111, 40, 25], [374, 115, 55, 24], [21, 205, 73, 25], [299, 210, 95, 18], [309, 294, 73, 29], [404, 292, 41, 27], [448, 293, 48, 20], [27, 297, 100, 23], [86, 405, 26, 17], [124, 409, 63, 20], [200, 401, 23, 16], [241, 398, 65, 15], [328, 392, 42, 21], [382, 392, 56, 16], [444, 392, 52, 14], [447, 440, 46, 16], [519, 442, 27, 12]]),
  "radioAndCheck2N.jpg":
(['sign', 'up', 'login', 'Name', 'Email', 'I', 'agree', 'O', 'Play', 'good', 'Obad', 'Plot'],
[[173, 236, 125, 71], [329, 244, 68, 52], [457, 206, 125, 86], [171, 376, 151, 55], [156, 562, 155, 67], [294, 755, 37, 66], [343, 768, 132, 60], [608, 860, 42, 72], [741, 864, 83, 66], [230, 866, 155, 72], [228, 926, 112, 52], [438, 1070, 114, 57]])
}
def getFromAppName(appName):
    return appDict[appName][0],appDict[appName][1]
# 1126,754,287,64