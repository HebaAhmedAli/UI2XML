import sys
sys.path.append('../')
import Utils
import Constants
import CodeGeneration.JavaGeneration as JavaGeneration
import os
from PIL import Image
import operator
import re
import numpy as np
import copy


class node:
    def __init__(self):
        self.id = -1
        self.nodeType = ""  # ex: Button , TextView , ... , LinearLayoutHorizontal, LinearLayoutVertical
        self.x = 0
        self.y = 0
        self.rightMargin = 0
        self.leftMargin = 0
        self.topMargin = 0
        self.bottomMargin = 0
        self.gravity = ""
        self.weight = 0
        self.text = ""
        self.backgroundColor = ""
        self.textColor = ""
        self.imagePath = ""
        self.height = ""  # ex: fixed no , wrap_content ,match_parent
        self.width = ""   # ex: fixed no , wrap_content ,match_parent
        self.childNodes = []
    
def clearInnerBoxes(parentNode,childNodes,img):
    cropImg = copy.copy(img)
    cropImg = cropImg[max(0,parentNode.y):min(parentNode.y+parentNode.height,img.shape[0]), max(0,parentNode.x):min(parentNode.x+parentNode.width,img.shape[1])]
    for i in range(len(childNodes)):
        startY = max(0,max(0,childNodes[i].y)-max(0,parentNode.y))
        startX = max(0,max(0,childNodes[i].x)-max(0,parentNode.x))
        cropImg[startY:min(startY+childNodes[i].height,cropImg.shape[0]),startX:min(startX+childNodes[i].width,cropImg.shape[1])] = np.array([-255,-255,-255])  # y , x
    return cropImg

def getFirstUnvisitedIndex(visited):
    for i in range(len(visited)):
        if visited[i]== False:
            return i
    return -1

def setMarginsHorizontal(groupedNodes):
    groupedNodes = sorted(groupedNodes, key=operator.attrgetter('x'))
    
    return groupedNodes

def setMarginsVertical(groupedNodes):
    groupedNodes = sorted(groupedNodes, key=operator.attrgetter('y'))

    return groupedNodes

def getWeightFromRatio(ratio,step):
    i = 1
    weight = 0
    while i*step <= 1:
        if ratio <= i*step:
            weight = i
            break
        i = i+1    
    return weight 
  
def setWeights(groupedNodes,sortAttr,screenDim,root,img=None,notLeafChilds=None):
    if not root and sortAttr != 'x':
        groupedNodes = sorted(groupedNodes, key=operator.attrgetter(sortAttr))
    ratio = 0
    weight = 0
    for i in range(len(groupedNodes)):
        if sortAttr == 'x':
            if i+1 >= len(groupedNodes):
                nextX = screenDim
            else:
                nextX = groupedNodes[i+1].x
            ratio = (nextX - (groupedNodes[i].x)) / screenDim
            weight = getWeightFromRatio(ratio,0.2)
        else:
            if i+1 >= len(groupedNodes) and root: 
                nextY = screenDim
            elif i+1 >= len(groupedNodes) and not root: 
                groupedNodes[i].weight = 1
                return groupedNodes
            else:
                nextY = groupedNodes[i+1].y
            ratio = (nextY - (groupedNodes[i].y)) / screenDim
            weight = getWeightFromRatio(ratio,0.15)
        groupedNodes[i].weight = weight
    return groupedNodes


# set nodeType , text , color , x, y , width , hight , imagePath here.
def createLeafNode(box,text,predictedComponent,img,weight = None):
    leafNode = node()
    leafNode.x = box[0]
    leafNode.y = box[1]
    leafNode.width = box[2]
    leafNode.height = box[3]
    finalText = " ".join(re.findall(r"[a-zA-Z0-9]+", text))
    leafNode.text = finalText
    leafNode.nodeType = predictedComponent
    if predictedComponent == 'android.widget.ImageView' or predictedComponent == 'android.widget.ImageButton':
        if not Constants.HAND_DRAWN:
            if not os.path.exists(Constants.DIRECTORY+'/res/drawable'):
                os.makedirs(Constants.DIRECTORY+'/res/drawable')
            cropImg = img[max(0,leafNode.y):min(leafNode.y+leafNode.height,img.shape[0]), max(0,leafNode.x):min(leafNode.x+leafNode.width,img.shape[1])]
            Image.fromarray(cropImg.astype(np.uint8)).save(Constants.DIRECTORY+'/res/drawable/'+"pic_"+str(leafNode.x)+'_'+str(leafNode.y)+'.png')
            leafNode.imagePath = "pic_"+str(leafNode.x)+'_'+str(leafNode.y)
        else:
            leafNode.imagePath = "pic_x"
    if predictedComponent == 'android.widget.TextView' or predictedComponent == 'android.widget.Button':
        cropImg = img[max(0,leafNode.y):min(leafNode.y+leafNode.height,img.shape[0]), max(0,leafNode.x):min(leafNode.x+leafNode.width,img.shape[1])]
        if not Constants.HAND_DRAWN:
            firstColor,secondColor = Utils.getMostAndSecondMostColors(cropImg,False)
        else:
            firstColor,secondColor = "#808080","#ffffff"
        leafNode.backgroundColor = firstColor
        leafNode.textColor = secondColor
    if weight != None:
        leafNode.weight = weight
    return leafNode


def groupHorizontalLeafNodes(groupedNodesI,imgH,img):
    groupedNodesHorizontal = []
    visited = [False for i in range(len(groupedNodesI))]
    indexUnvisited = 0
    while(indexUnvisited!=-1):
        backetNodes=[]
        backetNodes.append(groupedNodesI[indexUnvisited])
        visited[indexUnvisited]=True
        minY=100000
        maxY=-1
        minY = min(minY,groupedNodesI[indexUnvisited].y)
        maxY = max(maxY,groupedNodesI[indexUnvisited].y+groupedNodesI[indexUnvisited].height)
        boxNew = [groupedNodesI[indexUnvisited].x,minY,groupedNodesI[indexUnvisited].width,maxY-minY]
        for i in range(indexUnvisited+1,len(groupedNodesI)):
            boxI = [groupedNodesI[i].x,groupedNodesI[i].y,groupedNodesI[i].width,groupedNodesI[i].height]
            if visited[i] == False and Utils.checkYrange(boxNew,boxI) == True:
                minY = min(minY,groupedNodesI[i].y)
                maxY = max(maxY,groupedNodesI[i].y+groupedNodesI[i].height)
                boxNew = [groupedNodesI[i].x,minY,groupedNodesI[i].width,maxY-minY]
                visited[i] = True
                backetNodes.append(groupedNodesI[i])
        if len(backetNodes) == 1:
            groupedNodesHorizontal.append(backetNodes[0])
        else:
            backetNodes = groupTextViewsOfSameWord(backetNodes,img)
            groupedNodesHorizontal.append(createParentNodeHorizontal(backetNodes,img,backetNodes[0].x,backetNodes[-1].x+backetNodes[-1].width-backetNodes[0].x))
        indexUnvisited=getFirstUnvisitedIndex(visited)
    return groupedNodesHorizontal

def groupHorizontalLeafBoxes(boxes,texts,predictedComponents,img):
    groupedNodes = []
    visited = [False for i in range(len(boxes))]
    indexUnvisited = 0
    while(indexUnvisited!=-1):
        backetNodes=[]
        leafNode = createLeafNode(boxes[indexUnvisited],texts[indexUnvisited],predictedComponents[indexUnvisited],img)
        backetNodes.append(leafNode)
        visited[indexUnvisited]=True
        minY=100000
        maxY=-1
        minY = min(minY,boxes[indexUnvisited][1])
        maxY = max(maxY,boxes[indexUnvisited][1]+boxes[indexUnvisited][3])
        boxNew = [boxes[indexUnvisited][0],minY,boxes[indexUnvisited][2],maxY-minY]
        for i in range(indexUnvisited+1,len(boxes)):
            if visited[i] == False and Utils.checkYrange(boxes[i],boxNew) == True:
                minY = min(minY,boxes[i][1])
                maxY = max(maxY,boxes[i][1]+boxes[i][3])
                boxNew = [boxes[i][0],minY,boxes[i][2],maxY-minY]
                visited[i] = True
                leafNodeI = createLeafNode(boxes[i],texts[i],predictedComponents[i],img)
                backetNodes.append(leafNodeI)
        groupedNodes.append(backetNodes)
        indexUnvisited=getFirstUnvisitedIndex(visited)
    return groupedNodes

def specialRadioHandDrawn(groupedNodesIA,groupedNodesIB):
    if Constants.HAND_DRAWN == False:
        return False
    if groupedNodesIA.nodeType == "android.widget.RadioButton" and groupedNodesIB.text != "" and (groupedNodesIB.text[0] == 'o' or groupedNodesIB.text[0] == 'O'):
        return True
    if groupedNodesIB.nodeType == "android.widget.RadioButton" and groupedNodesIA.text != "" and (groupedNodesIA.text[0] == 'o' or groupedNodesIA.text[0] == 'O'):
        return True
    
def groupVerticalLeafNodes(groupedNodesI,imgH,img):
    groupedNodesVertical = []
    visited = [False for i in range(len(groupedNodesI))]
    indexUnvisited = 0
    while(indexUnvisited!=-1):
        backetNodes=[]
        backetNodes.append(groupedNodesI[indexUnvisited])
        visited[indexUnvisited]=True
        minX=100000
        maxX=-1
        minX = min(minX,groupedNodesI[indexUnvisited].x)
        maxX = max(maxX,groupedNodesI[indexUnvisited].x+groupedNodesI[indexUnvisited].width)
        boxNew = [minX,groupedNodesI[indexUnvisited].y,maxX-minX,groupedNodesI[indexUnvisited].height]
        for i in range(indexUnvisited+1,len(groupedNodesI)):
            boxI = [groupedNodesI[i].x,groupedNodesI[i].y,groupedNodesI[i].width,groupedNodesI[i].height]
            if visited[i] == False and Utils.checkXrange(boxNew,boxI) == True and not specialRadioHandDrawn(groupedNodesI[indexUnvisited],groupedNodesI[i]):
                minX = min(minX,groupedNodesI[i].x)
                maxX = max(maxX,groupedNodesI[i].x+groupedNodesI[i].width)
                boxNew = [minX,groupedNodesI[i].y,maxX-minX,groupedNodesI[i].height]
                visited[i] = True
                backetNodes.append(groupedNodesI[i])
        if len(backetNodes) == 1:
            groupedNodesVertical.append(backetNodes[0])
        else:
            groupedNodesVertical.append(createParentNodeVertical(backetNodes,imgH,"LinearLayoutVertical",img,True))
        indexUnvisited=getFirstUnvisitedIndex(visited)
    return groupedNodesVertical

def packetVerticalLeafNodesNoParent(groupedNodesI,imgH,img):
    groupedNodesVertical = []
    visited = [False for i in range(len(groupedNodesI))]
    indexUnvisited = 0
    minX=100000
    maxX=-1
    oldPacket = []
    while(indexUnvisited!=-1):
        backetNodes=[]
        backetNodes.append(groupedNodesI[indexUnvisited])
        visited[indexUnvisited]=True
        minX = min(minX,groupedNodesI[indexUnvisited].x)
        maxX = max(maxX,groupedNodesI[indexUnvisited].x+groupedNodesI[indexUnvisited].width)
        boxNew = [minX,groupedNodesI[indexUnvisited].y,maxX-minX,groupedNodesI[indexUnvisited].height]
        for i in range(indexUnvisited+1,len(groupedNodesI)):
            boxI = [groupedNodesI[i].x,groupedNodesI[i].y,groupedNodesI[i].width,groupedNodesI[i].height]
            if visited[i] == False and Utils.checkXrange(boxNew,boxI) == True:
                minX = min(minX,groupedNodesI[i].x)
                maxX = max(maxX,groupedNodesI[i].x+groupedNodesI[i].width)
                boxNew = [minX,groupedNodesI[i].y,maxX-minX,groupedNodesI[i].height]
                visited[i] = True
                backetNodes.append(groupedNodesI[i])
            else:
                break
        if len(backetNodes) == 1:
            if len(oldPacket) != 0:
                if indexUnvisited==len(groupedNodesI)-1 and backetNodes[0].nodeType == 'android.widget.TextView':
                    oldPacket.append(backetNodes[0])
                    groupedNodesVertical.append(oldPacket)
                    oldPacket = []
                else:
                    groupedNodesVertical.append(oldPacket)
                    groupedNodesVertical.append(backetNodes)
                    oldPacket = []
            else:
                groupedNodesVertical.append(backetNodes)
        else:
            oldPacket += backetNodes
        indexUnvisited=getFirstUnvisitedIndex(visited)
    if len(oldPacket) != 0:
        groupedNodesVertical.append(oldPacket)
    return groupedNodesVertical

def createParentNodeVertical(groupedNodes,imgH,parentType,img,notLeafChilds):
    parentNode = node()
    parentNode.nodeType = parentType
    minX=1000000
    maxX=0
    minY=1000000
    maxY=0
    for i in range(len(groupedNodes)):
        minX=min(minX,groupedNodes[i].x)
        maxX=max(maxX,groupedNodes[i].x+int(groupedNodes[i].width))
        minY=min(minY,groupedNodes[i].y)
        maxY=max(maxY,groupedNodes[i].y+int(groupedNodes[i].height))
    parentNode.x = minX
    parentNode.width = maxX - minX
    parentNode.y = minY
    parentNode.height = maxY - minY  # TODO: replace with match_parent in mapping
    groupedNodes = setWeights(groupedNodes,'y',imgH,False,img,notLeafChilds)
    parentNode.childNodes = groupedNodes
    return parentNode
 
def createParentNodeHorizontal(groupedNodes,img,x,width):
    parentNode = node()
    parentNode.nodeType = "LinearLayoutHorizontal"
    #parentNode.width = "match_parent"
    minY=1000000
    maxY=0
    for i in range(len(groupedNodes)):
        minY=min(minY,groupedNodes[i].y)
        maxY=max(maxY,groupedNodes[i].y+int(groupedNodes[i].height))
    parentNode.x = x 
    parentNode.width = width
    parentNode.y = minY
    parentNode.height = maxY - minY
    if len(groupedNodes) == 1 :
        if (abs(groupedNodes[0].x+0.5*groupedNodes[0].width - img.shape[1]/2) <= 50):
            parentNode.gravity = "center"
        elif groupedNodes[0].x/img.shape[1] > 0.5:
            parentNode.gravity = "right"
        parentNode.childNodes = groupedNodes
        if not Constants.HAND_DRAWN:
            imgClean = clearInnerBoxes(parentNode,parentNode.childNodes,img)
            parentNode.backgroundColor = Utils.getMostAndSecondMostColors(imgClean,True)
        else:
            parentNode.backgroundColor = "#ffffff"
        return parentNode
    groupedNodes = setWeights(groupedNodes,'x',width,False)
    parentNode.childNodes = groupedNodes
    if not Constants.HAND_DRAWN:
        imgClean = clearInnerBoxes(parentNode,parentNode.childNodes,img)
        parentNode.backgroundColor = Utils.getMostAndSecondMostColors(imgClean,True)
    else:
        parentNode.backgroundColor = "#ffffff"
    return parentNode

def groupTextViewsOfSameWord(groupedNodesI,img):
    j=0
    groupedNodesNew = []
    while j<len(groupedNodesI):
        startJ = j
        if groupedNodesI[startJ].nodeType != 'android.widget.TextView':
            groupedNodesNew.append(groupedNodesI[startJ])
            j += 1
            continue
        minY = groupedNodesI[startJ].y
        maxY =  groupedNodesI[startJ].height+groupedNodesI[startJ].y
        text = groupedNodesI[startJ].text
        while j+1 < len(groupedNodesI) and (groupedNodesI[j+1].x-(groupedNodesI[j].x+groupedNodesI[j].width))/img.shape[1] < 0.07\
        and groupedNodesI[j+1].nodeType == 'android.widget.TextView':
            text += (" "+groupedNodesI[j+1].text)
            j+=1
            minY = min(minY,groupedNodesI[j].y)
            maxY = max(maxY,groupedNodesI[j].height+groupedNodesI[j].y)
        box = [groupedNodesI[startJ].x,minY,groupedNodesI[j].x+groupedNodesI[j].width-groupedNodesI[startJ].x,maxY-minY]
        if startJ != j:
            groupedNodesNew.append(createLeafNode(box,text,'android.widget.TextView',img))
        else:
            groupedNodesNew.append(groupedNodesI[startJ])
        j += 1
    return groupedNodesNew
        
def groupHorizontalInsideVertical(groupedNodesI,img):
    groupedNodesNew = []
    packetsVertical = packetVerticalLeafNodesNoParent(groupedNodesI,img.shape[0],img)
    if len(packetsVertical) == 1:
        return groupedNodesI
    for i in range(len(packetsVertical)):
        if len(packetsVertical[i]) == 1:
            groupedNodesNew.append(packetsVertical[i][0])
        else:
            groupedNodesNew += groupHorizontalLeafNodes(packetsVertical[i],img.shape[0],img)     
    return groupedNodesNew
            
def createLeavesParents(groupedNodes,img):
    parentNodes = []
    for i in range(len(groupedNodes)):
        groupedNodes[i] = sorted(groupedNodes[i], key=operator.attrgetter('x'))
        groupedNodes[i] = groupHorizontalInsideVertical(groupedNodes[i],img)
        groupedNodes[i] = groupTextViewsOfSameWord(groupedNodes[i],img)
        groupedNodesVertical = groupVerticalLeafNodes(groupedNodes[i],img.shape[0],img)
        parentNode = createParentNodeHorizontal(groupedNodesVertical,img,0,img.shape[1])
        parentNodes.append(parentNode)
    return parentNodes
    
def buildParentNodes(boxes,texts,predictedComponents,img):
    groupedNodes = groupHorizontalLeafBoxes(boxes,texts,predictedComponents,img)
    parentNodes = createLeavesParents(groupedNodes,img)
    return parentNodes

def createRoot(parentNodes,imgH,dynamic,img):
    parentNode = node()
    parentNode.nodeType = "LinearLayoutVertical"
    if dynamic == True:
        parentNodes = groupListViewAndRadio(parentNodes,imgH,img)
    else:
        parentNodes = groupRadio(parentNodes,imgH,img)
    parentNodes = setWeights(parentNodes,'y',imgH,True,img,True)
    parentNode.childNodes = parentNodes
    return parentNode
    
def buildHierarchy(boxes,texts,predictedComponents,img):
    parentNodes = buildParentNodes(boxes,texts,predictedComponents,img)
    parentNodesForGui = sorted(parentNodes, key=operator.attrgetter('y'))
    rootNode = createRoot(parentNodesForGui,img.shape[0],Constants.DYNAMIC,img)
    return rootNode,parentNodesForGui

def getTypeAndOriAndID(parentNode,tabsString,myIndex):
    if parentNode.nodeType == 'LinearLayoutVertical':
        return 'LinearLayout\n'+tabsString+'\t'+'android:orientation = "vertical"'\
                '\n'+tabsString+'\t' 
    elif parentNode.nodeType == 'LinearLayoutHorizontal':
        return 'LinearLayout\n'+tabsString+'\t'+'android:orientation = "horizontal"'\
                '\n'+tabsString+'\t' +\
                'android:background = "'+parentNode.backgroundColor+'"'+'\n'+tabsString+'\t'+\
                'android:padding="8dp"'+'\n'+tabsString+'\t'
    parentNode.id = myIndex
    typeN = parentNode.nodeType[15:len(parentNode.nodeType)]
    if typeN == "ListView":
         toReturn = typeN+'\n'+tabsString+'\t'+'android:id = "@+id/'+typeN+str(Constants.listId)+'_'+parentNode.id \
                +'"\n'+tabsString+'\t' + \
                'android:padding="5dp"'+'\n'+tabsString+'\t' 
         parentNode.id = str(Constants.listId)+'_'+parentNode.id
    else:
        toReturn = typeN+'\n'+tabsString+'\t'+'android:id = "@+id/'+typeN+'_'+parentNode.id \
                    +'"\n'+tabsString+'\t' + \
                    'android:padding="5dp"'+'\n'+tabsString+'\t' 
    Constants.ID += 1         
    return toReturn
       
def getType(nodeType):
    if nodeType == 'LinearLayoutVertical' or nodeType == 'LinearLayoutHorizontal':
        return 'LinearLayout'
    return nodeType[15:len(nodeType)]

def getWeightWidthHeightGravity(myParentType,height,width,gravity,weight,tabsString):
    toReturn = "" 
    if myParentType == 'LinearLayoutVertical':
        toReturn+= "android:layout_width = "+'"match_parent"'+'\n'+tabsString+'\t'
        if weight == 0:
            toReturn+= 'android:layout_height = "wrap_content"'+'\n'+tabsString+'\t'
        else:
            toReturn+= 'android:layout_height = "0dp"'+'\n'+tabsString+'\t'
            toReturn+= 'android:layout_weight = "'+str(weight)+'"'+'\n'+tabsString+'\t'
    elif myParentType == 'LinearLayoutHorizontal':
        toReturn+= "android:layout_height = "+'"wrap_content"'+'\n'+tabsString+'\t'
        if weight == 0:
           toReturn+= 'android:layout_width = "wrap_content"'+'\n'+tabsString+'\t'
        else:
            toReturn+= 'android:layout_width = "0dp"'+'\n'+tabsString+'\t'
            toReturn+= 'android:layout_weight = "'+str(weight)+'"'+'\n'+tabsString+'\t'
    else:
        toReturn+= "android:layout_width = "+'"match_parent"'+'\n'+tabsString+'\t'
        toReturn+= 'android:layout_height = "wrap_content"'+'\n'+tabsString+'\t'
    if gravity != "":
        toReturn+= 'android:gravity = "'+gravity+'"'+'\n'+tabsString+'\t'        
    return toReturn

#"android:textSize = "+'"'+str(int(parentNode.height/imgH * 1000)) +'sp"'+'\n'+tabsString+'\t'+ \
def printSpecialCase(parentNode,tabsString,imgH):
    attributeString = ""
    if parentNode.nodeType == 'android.widget.EditText':
        attributeString += "android:hint = "+'"'+parentNode.text+'"'+'\n'+tabsString+'\t'+ \
        "android:ems = "+'"'+str(parentNode.width // 16)+'"'+'\n'+tabsString+'\t'
   
    if parentNode.nodeType == 'android.widget.TextView'or parentNode.nodeType == 'android.widget.Button':
        attributeString += "android:text = "+'"'+parentNode.text.replace('"','t')+'"'+'\n'+tabsString+'\t'+ \
        'android:textColor = "'+parentNode.textColor+'"'+'\n'+tabsString+'\t'+\
        'android:background = "'+parentNode.backgroundColor+'"'+'\n'+tabsString+'\t'
        
    if (parentNode.nodeType == 'android.widget.RadioButton' or parentNode.nodeType == 'android.widget.CheckBox')\
    and parentNode.text != "":
        attributeString += "android:text = "+'"'+parentNode.text.replace('"','t')+'"'+'\n'+tabsString+'\t'
        
 
    if parentNode.nodeType == 'android.widget.ImageView'or parentNode.nodeType == 'android.widget.ImageButton':
        attributeString += "android:src = "+'"'+"@drawable/"+parentNode.imagePath+'"'+'\n'+tabsString+'\t'
        
    if parentNode.nodeType == 'android.widget.ImageButton' or parentNode.nodeType == 'android.widget.Button':
         attributeString += "android:onClick = "+'"'+"clickMe"+parentNode.id+'"'+'\n'+tabsString+'\t'
         
    if parentNode.nodeType == 'android.widget.Button':
        attributeString+= 'android:gravity = "center'+'"'+'\n'+tabsString+'\t'
    return attributeString

def printSpecialCaseListView(parentNode,tabsString,imgH):
    attributeString = ""
    
    if parentNode.nodeType == 'android.widget.TextView':
        attributeString +='android:textColor = "'+parentNode.textColor+'"'+'\n'+tabsString+'\t'+\
        'android:background = "'+parentNode.backgroundColor+'"'+'\n'+tabsString+'\t'+\
        "android:text = "+'"'+parentNode.text.replace('"','t')+'"'+'\n'+tabsString+'\t'
        
    if parentNode.nodeType == 'android.widget.ImageView'or parentNode.nodeType == 'android.widget.ImageButton':
        attributeString += "android:src = "+'"'+"@drawable/"+parentNode.imagePath+'"'+'\n'+tabsString+'\t'
      
    return attributeString

def printListViewChildNode(parentNode,myParentType,tabs,imgH,myIndex):
    tabsString=""
    for i in range(tabs):
        tabsString+='\t'
    returnString=""
    returnString+= tabsString+'<'+getTypeAndOriAndID(parentNode,tabsString,myIndex)+\
                  getWeightWidthHeightGravity(myParentType,parentNode.height,parentNode.width\
                                    ,parentNode.gravity,parentNode.weight,tabsString)+\
                                    printSpecialCaseListView(parentNode,tabsString,imgH)+'>\n'                                  
    for i in range(len(parentNode.childNodes)) :                                   
        returnString += printListViewChildNode(parentNode.childNodes[i],parentNode.nodeType,2,imgH,myIndex+'_'+str(i))
    returnString+= tabsString+"</"+ getType(parentNode.nodeType)+'>'+'\n'
                                    
    return returnString

def printNodeXml(fTo,parentNode,myParentType,tabs,imgH,actionBarOp,myIndex,specialId=None):    
    tabsString=""
    for i in range(tabs):
        tabsString+='\t'
    if tabs == 0:
        fTo.write('<?xml version = "1.0" encoding = "utf-8"?>\n'+
                  '<LinearLayout xmlns:android = "http://schemas.android.com/apk/res/android"\n'
                  +'\t'+'xmlns:app = "http://schemas.android.com/apk/res-auto"\n'
                  +'\t'+'xmlns:tools = "http://schemas.android.com/tools"\n'
                  +'\t'+'android:layout_width = "match_parent"\n'
                  +'\t'+'android:layout_height = "match_parent"\n'
                  +'\t'+'android:orientation = "vertical"\n'
                  +'\t'+'tools:context = "'+'.'+myParentType.capitalize()+'Activity"'+'>\n')
    else:
        fTo.write(tabsString+'<'+getTypeAndOriAndID(parentNode,tabsString,myIndex)+\
                  getWeightWidthHeightGravity(myParentType,parentNode.height,parentNode.width\
                                    ,parentNode.gravity,parentNode.weight,tabsString)+\
                                    printSpecialCase(parentNode,tabsString,imgH)+'>\n')
    if len(parentNode.childNodes)==0:
        typeOfNode = getType(parentNode.nodeType)
        fTo.write(tabsString+"</"+ typeOfNode+'>'+'\n')
        Constants.boxToGui.append([int(parentNode.x),int(parentNode.y),int(parentNode.width),int(parentNode.height)])
        Constants.idToGui.append(typeOfNode+'_'+parentNode.id)
        Constants.predictedToGui.append(typeOfNode)
        return
    
    if parentNode.nodeType == 'android.widget.ListView':
        fToListView=open(Constants.DIRECTORY+'/res/layout/'+'list_view'+str(Constants.listId)+'_'+myIndex+'.xml', 'w+')
        Constants.xmlFilesToGui.append('list_view'+str(Constants.listId)+'_'+myIndex+'.xml')
        Constants.listId += 1
        fileOuput = '<?xml version = "1.0" encoding = "utf-8"?>\n'+\
        '<LinearLayout xmlns:android = "http://schemas.android.com/apk/res/android"\n'\
        +'\t'+'xmlns:app = "http://schemas.android.com/apk/res-auto"\n'\
        +'\t'+'xmlns:tools = "http://schemas.android.com/tools"\n'\
        +'\t'+'android:layout_width = "match_parent"\n'\
        +'\t'+'android:layout_height = "match_parent"\n'\
        +'\t'+'android:orientation = "vertical"'+'>\n'
        fToListView.write(fileOuput)            
        fToListView.write(printListViewChildNode(parentNode.childNodes[0],parentNode.nodeType,1,imgH,myIndex[:-2]+'_'+str(0+specialId)))
        fToListView.write("</LinearLayout>"+'\n')    
        fToListView.close()   
        # Append the rest of chils.
        for i in range(len(parentNode.childNodes)):
            for j in range(len(parentNode.childNodes[i].childNodes)):
                typeOfNode = getType(parentNode.childNodes[i].childNodes[j].nodeType)
                Constants.boxToGui.append([int(parentNode.childNodes[i].childNodes[j].x),int(parentNode.childNodes[i].childNodes[j].y),int(parentNode.childNodes[i].childNodes[j].width),int(parentNode.childNodes[i].childNodes[j].height)])
                Constants.idToGui.append(typeOfNode+'_'+myIndex[:-2]+'_'+str(i+specialId)+'_'+str(j))
                Constants.predictedToGui.append(typeOfNode)
    elif parentNode.nodeType == 'android.widget.RadioGroup':
        for i in range(len(parentNode.childNodes)):
            printNodeXml(fTo,parentNode.childNodes[i],parentNode.nodeType,tabs+1,imgH,actionBarOp,myIndex[:-2]+'_'+str(i+specialId))
    else:
        if actionBarOp == 'A' and tabs == 0:
            fToActionBar=open(Constants.DIRECTORY+'/res/layout/'+'action_bar_'+myParentType+'.xml', 'w+')
            Constants.xmlFilesToGui.append('action_bar_'+myParentType+'.xml')
            fileOuput = '<?xml version = "1.0" encoding = "utf-8"?>\n'+\
                '<LinearLayout xmlns:android = "http://schemas.android.com/apk/res/android"\n'\
                +'\t'+'xmlns:app = "http://schemas.android.com/apk/res-auto"\n'\
                +'\t'+'xmlns:tools = "http://schemas.android.com/tools"\n'\
                +'\t'+'android:layout_width = "match_parent"\n'\
                +'\t'+'android:layout_height = "wrap_content"\n'\
                +'\t'+'android:background = "'+parentNode.childNodes[0].backgroundColor+'"'+'\n'\
                +'\t'+'android:padding="8dp"'+'\n'\
                +'\t'+'android:orientation = "horizontal"'+'>\n'
            fToActionBar.write(fileOuput) 
            for i in range(0,len(parentNode.childNodes[0].childNodes)):
                printNodeXml(fToActionBar,parentNode.childNodes[0].childNodes[i],parentNode.childNodes[0].nodeType,1,imgH,actionBarOp,myIndex+'_'+str(0)+'_'+str(i))
            fToActionBar.write("</LinearLayout>"+'\n')    
            fToActionBar.close() 
            idd = 1
            for i in range(1,len(parentNode.childNodes)):
                if parentNode.childNodes[i].nodeType == 'android.widget.ListView' or parentNode.childNodes[i].nodeType == 'android.widget.RadioGroup':
                    printNodeXml(fTo,parentNode.childNodes[i],parentNode.nodeType,tabs+1,imgH,actionBarOp,myIndex+'_'+str(idd),idd)
                    idd += len(parentNode.childNodes[i].childNodes)
                else:
                    printNodeXml(fTo,parentNode.childNodes[i],parentNode.nodeType,tabs+1,imgH,actionBarOp,myIndex+'_'+str(idd))
                    idd += 1
        else:
            idd= 0
            for i in range(len(parentNode.childNodes)):
                if parentNode.childNodes[i].nodeType == 'android.widget.ListView' or parentNode.childNodes[i].nodeType == 'android.widget.RadioGroup':
                    printNodeXml(fTo,parentNode.childNodes[i],parentNode.nodeType,tabs+1,imgH,actionBarOp,myIndex+'_'+str(idd),idd)
                    idd += len(parentNode.childNodes[i].childNodes)
                else:
                    printNodeXml(fTo,parentNode.childNodes[i],parentNode.nodeType,tabs+1,imgH,actionBarOp,myIndex+'_'+str(idd))
                    idd += 1
    fTo.write(tabsString+"</"+ getType(parentNode.nodeType)+'>'+'\n')
        
def mapToXml(parentNode,appName,imgH,actionBarOp):
    if not os.path.exists(Constants.DIRECTORY+'/res/layout'):
            os.makedirs(Constants.DIRECTORY+'/res/layout') 
    fTo=open(Constants.DIRECTORY+'/res/layout/'+'activity_'+appName+'.xml', 'w+')
    Constants.xmlFilesToGui.append('activity_'+appName+'.xml')
    printNodeXml(fTo,parentNode,appName,0,imgH,actionBarOp,"0")
    return

    
def generateXml(boxes,texts,predictedComponents,img,appName,actionBarOp):
    Constants.boxToGui = []
    Constants.predictedToGui = []
    Constants.idToGui = []
    Constants.xmlFilesToGui = []
    parentNode,parentNodesForGui=buildHierarchy(boxes,texts,predictedComponents,img)        
    mapToXml(parentNode,appName,img.shape[0],actionBarOp)
    JavaGeneration.generateJava(parentNode,appName,actionBarOp)
    return parentNodesForGui

def updateXml(parentNodesForGui,boxUpdated,predictedUpdated,idUpdated,img,appName,actionBarOp):
    Constants.boxToGui = []
    Constants.predictedToGui = []
    Constants.idToGui = []
    Constants.xmlFilesToGui = []
    for i in range(len(idUpdated)):
        indices = idUpdated[i].split('_')
        if len(indices) == 4: # horizontal leaf
            parentNode = parentNodesForGui[int(indices[2])].childNodes[int(indices[3])]
            parentNodesForGui[int(indices[2])].childNodes[int(indices[3])] = createLeafNode(boxUpdated[i],parentNode.text,predictedUpdated[i],img,parentNode.weight)
        elif len(indices) == 5: # 5 horizontal vertical leaf
            parentNode = parentNodesForGui[int(indices[2])].childNodes[int(indices[3])].childNodes[int(indices[4])]
            parentNodesForGui[int(indices[2])].childNodes[int(indices[3])].childNodes[int(indices[4])] = createLeafNode(boxUpdated[i],parentNode.text,predictedUpdated[i],img,parentNode.weight)
        else: # 6 horizontal vertical horizontal leaf
            parentNode = parentNodesForGui[int(indices[2])].childNodes[int(indices[3])].childNodes[int(indices[4])].childNodes[int(indices[5])]
            parentNodesForGui[int(indices[2])].childNodes[int(indices[3])].childNodes[int(indices[4])].childNodes[int(indices[5])] = createLeafNode(boxUpdated[i],parentNode.text,predictedUpdated[i],img,parentNode.weight)   
    # Merge text views after update.
    for i in range(len(idUpdated)):
        indices = idUpdated[i].split('_')
        if len(indices) == 4: # horizontal leaf
            parentNodesForGui[int(indices[2])].childNodes = groupTextViewsOfSameWord(parentNodesForGui[int(indices[2])].childNodes,img)
        elif len(indices) == 6: # 6 horizontal vertical horizontal leaf
            parentNodesForGui[int(indices[2])].childNodes[int(indices[3])].childNodes[int(indices[4])].childNodes = groupTextViewsOfSameWord(parentNodesForGui[int(indices[2])].childNodes[int(indices[3])].childNodes[int(indices[4])].childNodes,img) 
    parentNode = createRoot(parentNodesForGui,img.shape[0],Constants.DYNAMIC,img)
    mapToXml(parentNode,appName,img.shape[0],actionBarOp) 
    JavaGeneration.generateJava(parentNode,appName,actionBarOp)
    return parentNodesForGui

def groupListViewAndRadio(groupedNodes,imgH,img):
    groupedNodesNew = []
    i = 0
    while i<len(groupedNodes):
        patternToSearch,radioHorizontal = extractPatternOfNode(groupedNodes[i])
        if patternToSearch == 'android.widget.RadioButton' and radioHorizontal:
            groupedNodesNew.append(createParentNodeVertical([groupedNodes[i]],imgH,'android.widget.RadioGroup',img,True))
            i+=1
            continue
            
        lastIndex = getLastPatternIndex(i,groupedNodes,patternToSearch)
        if lastIndex != i:
            childs = groupedNodes[i:lastIndex+1]
            if patternToSearch ==  'android.widget.RadioButton':
                groupedNodesNew.append(createParentNodeVertical(childs,imgH,'android.widget.RadioGroup',img,True))
                i = lastIndex
            elif lastIndex-i>=2 and patternToSearch.find('android.widget.EditText') == -1 and not(patternToSearch.find('android.widget.Button') != -1 and patternToSearch.find('android.widget.TextView') == -1)\
            and not(patternToSearch.find('android.widget.CheckBox') != -1 and patternToSearch.find('android.widget.TextView') == -1) \
            and not(patternToSearch.find('android.widget.SeekBar') != -1 and patternToSearch.find('android.widget.TextView') == -1) \
            and not(patternToSearch.find('android.widget.Switch') != -1 and patternToSearch.find('android.widget.TextView') == -1):
                groupedNodesNew.append(createParentNodeVertical(childs,imgH,'android.widget.ListView',img,True))
                i = lastIndex
            else:
                groupedNodesNew.append(groupedNodes[i])
        else:
            groupedNodesNew.append(groupedNodes[i])
        i+=1
    return groupedNodesNew

def groupRadio(groupedNodes,imgH,img):
    groupedNodesNew = []
    i = 0
    while i<len(groupedNodes):
        patternToSearch,radioHorizontal = extractPatternOfNode(groupedNodes[i])
        if patternToSearch == 'android.widget.RadioButton' and radioHorizontal:
            groupedNodesNew.append(createParentNodeVertical(groupedNodes[i],imgH,'android.widget.RadioGroup',img,True))
            i+=1
            continue        
        lastIndex = getLastPatternIndex(i,groupedNodes,patternToSearch)
        if lastIndex != i and patternToSearch ==  'android.widget.RadioButton':
            childs = groupedNodes[i:lastIndex+1]
            groupedNodesNew.append(createParentNodeVertical(childs,imgH,'android.widget.RadioGroup',img,True))
            i = lastIndex
        else:
            groupedNodesNew.append(groupedNodes[i])
        i+=1
    return groupedNodesNew

def extractPatternOfNode(parentNode):
    pattern = ""
    countChildRadio  = 0
    radioHorizontal = False
    for i in range(len(parentNode.childNodes)):
        pattern += parentNode.childNodes[i].nodeType
        if parentNode.childNodes[i].nodeType == 'android.widget.RadioButton':
            pattern =  'android.widget.RadioButton'
            countChildRadio +=1
    if countChildRadio > 1:
        radioHorizontal = True
        pattern =  'android.widget.RadioButton'
    return pattern,radioHorizontal
        
def getLastPatternIndex(firstIndex,groupedNodes,pattern):
    for i in range(firstIndex+1,len(groupedNodes)):
        foundPattern,radioHorizontal = extractPatternOfNode(groupedNodes[i])
        if foundPattern != pattern or radioHorizontal:
            return i-1
    return len(groupedNodes)-1

# TO test.

def printNode(fTo,parentNode):        
    fTo.write(parentNode.nodeType+" ("+" x = "+ str(parentNode.x)+
        " y = "+str(parentNode.y)+
        " text = "+parentNode.text+
        " imagePath = "+parentNode.imagePath+
        " height = "+str(parentNode.height)+
        " width = "+str(parentNode.width)+
        " gravity = "+parentNode.gravity+
        " weight = "+str(parentNode.weight)+" )\n")
    if len(parentNode.childNodes)==0:
        return
    fTo.write("{\n")
    for i in range(len(parentNode.childNodes)):
        printNode(fTo,parentNode.childNodes[i])
    fTo.write("}\n")
        
def printHierarchy(parentNode,appName):
    if not os.path.exists(Constants.DIRECTORY+'/XML'):
            os.makedirs(Constants.DIRECTORY+'/XML') 
    fTo=open(Constants.DIRECTORY+'/XML/'+'xmlHirarchy_'+appName+'.txt', 'w+')
    printNode(fTo,parentNode)

    