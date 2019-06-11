import sys
sys.path.append('../')
import Utils
import Constants
import os
import cv2
import operator

class node:
    def __init__(self):
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
        self.backgroundColor = "white"
        self.textColor = "black"
        self.imagePath = ""
        self.height = "" # ex: fixed no , wrap_content ,match_parent
        self.width = "" # ex: fixed no , wrap_content ,match_parent
        self.childNodes = []
    
def getFirstUnvisitedIndex(visited):
    for i in range(len(visited)):
        if visited[i]== False:
            return i
    return -1

def setWeightsAndMarginsHorizontal(groupedNodes):
    groupedNodes = sorted(groupedNodes, key=operator.attrgetter('x'))
    
    return groupedNodes

def setWeightsAndMarginsVertical(groupedNodes):
    groupedNodes = sorted(groupedNodes, key=operator.attrgetter('y'))

    return groupedNodes

# set nodeType , text , color , x, y , width , hight , imagePath here.
def createLeafNode(box,text,predictedComponent,img):
    leafNode = node()
    leafNode.x = box[0]
    leafNode.y = box[1]
    leafNode.width = box[2]
    leafNode.height = box[3]
    leafNode.text = text
    leafNode.nodeType = predictedComponent
    if predictedComponent == 'android.widget.ImageView':
        if not os.path.exists(Constants.DIRECTORY+'/drawable'):
            os.makedirs(Constants.DIRECTORY+'/drawable')
        cropImg = img[leafNode.y:leafNode.y+leafNode.height, leafNode.x:leafNode.x+leafNode.width]
        cv2.imwrite(Constants.DIRECTORY+'/drawable/'+str(leafNode.x)+'_'+str(leafNode.y)+'.png',cropImg)
        leafNode.imagePath = Constants.DIRECTORY+'/drawable/'+str(leafNode.x)+'_'+str(leafNode.y)+'.png'
    # TODO: set Color.
    return leafNode

def groupHorizontalLeafNodes(boxes,texts,predictedComponents,img):
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

def groupVerticalLeafNodes(groupedNodesI):
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
            if visited[i] == False and Utils.checkXrange(boxNew,boxI) == True:
                minX = min(minX,groupedNodesI[indexUnvisited].x)
                maxX = max(maxX,groupedNodesI[i].x+groupedNodesI[i].width)
                boxNew = [minX,groupedNodesI[i].y,maxX-minX,groupedNodesI[i].height]
                visited[i] = True
                backetNodes.append(groupedNodesI[i])
        if len(backetNodes) == 1:
            groupedNodesVertical.append(backetNodes[0])
        else:
            groupedNodesVertical.append(createParentNodeVertical(backetNodes))
        indexUnvisited=getFirstUnvisitedIndex(visited)
    return groupedNodesVertical

def createParentNodeVertical(groupedNodes):
    parentNode = node()
    parentNode.nodeType = "LinearLayoutVertical"
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
    groupedNodes = setWeightsAndMarginsVertical(groupedNodes)
    parentNode.childNodes = groupedNodes
    return parentNode
 
def createParentNodeHorizontal(groupedNodes):
    parentNode = node()
    parentNode.nodeType = "LinearLayoutHorizontal"
    parentNode.width = "match_parent"
    minY=1000000
    maxY=0
    for i in range(len(groupedNodes)):
        minY=min(minY,groupedNodes[i].y)
        maxY=max(maxY,groupedNodes[i].y+int(groupedNodes[i].height))
    parentNode.y = minY
    parentNode.height = maxY - minY
    groupedNodes = setWeightsAndMarginsHorizontal(groupedNodes)
    parentNode.childNodes = groupedNodes
    return parentNode

def createLeavesParents(groupedNodes):
    parentNodes = []
    for i in range(len(groupedNodes)):
        groupedNodesVertical = groupVerticalLeafNodes(groupedNodes[i])
        parentNode = createParentNodeHorizontal(groupedNodesVertical)
        parentNodes.append(parentNode)
    return parentNodes
    
def buildParentNodes(boxes,texts,predictedComponents,img):
    groupedNodes = groupHorizontalLeafNodes(boxes,texts,predictedComponents,img)
    parentNodes = createLeavesParents(groupedNodes)
    return parentNodes

def createRoot(parentNodes):
    parentNode = node()
    parentNode.nodeType = "LinearLayoutVertical"
    parentNodes = setWeightsAndMarginsVertical(parentNodes)
    parentNode.childNodes = parentNodes
    return parentNode
    
def buildHierarchy(boxes,texts,predictedComponents,img):
    parentNodes = buildParentNodes(boxes,texts,predictedComponents,img)
    rootNode = createRoot(parentNodes)
    return rootNode

def mapToXml(parentNode,appName):
    # map and out xml file
    return
    
def generateXml(boxes,texts,predictedComponents,img,appName):
    parentNode=buildHierarchy(boxes,texts,predictedComponents,img)
    mapToXml(parentNode,appName)
    # To test.
    printHierarchy(parentNode,appName)
    return

# TO test.
'''
        " rightMargin = "+str(parentNode.rightMargin)+
        " leftMargin = "+str(parentNode.leftMargin)+
        " topMargin = "+str(parentNode.topMargin)+
        " bottomMargin = "+str(parentNode.bottomMargin)+
        " gravity = "+parentNode.gravity+
        " weight = "+str(parentNode.weight)+
        " backgroundColor = "+parentNode.backgroundColor+
        " textColor = "+parentNode.textColor+
'''
def printNode(fTo,parentNode):        
    fTo.write(parentNode.nodeType+" ("+" x = "+ str(parentNode.x)+
        " y = "+str(parentNode.y)+
        " text = "+parentNode.text+
        " imagePath = "+parentNode.imagePath+
        " height = "+str(parentNode.height)+
        " width = "+str(parentNode.width)+" )\n")
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
    