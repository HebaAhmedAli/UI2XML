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
  
def setWeights(groupedNodes,sortAttr,screenDim,root):
    groupedNodes = sorted(groupedNodes, key=operator.attrgetter(sortAttr))
    if len(groupedNodes) == 1 and sortAttr == 'x':
        if abs(groupedNodes[0].x+0.5*groupedNodes[0].width - screenDim/2) <= 30:
            groupedNodes[0].gravity = "center_horizontal"
        return groupedNodes
    ratio = 0
    weight = 0
    for i in range(len(groupedNodes)):
        if sortAttr == 'x':
            if i+1 >= len(groupedNodes):
                nextX = screenDim
            else:
                nextX = groupedNodes[i+1].x
            ratio = (nextX - (groupedNodes[i].x + groupedNodes[i].width)) / screenDim
            weight = getWeightFromRatio(ratio,0.2)
        else:
            if i+1 >= len(groupedNodes) and root: 
                nextY = screenDim
            elif i+1 >= len(groupedNodes) and not root: 
                groupedNodes[i].weight = 1 # TODO: set width or hight = 0 in mapping.
                return groupedNodes
            else:
                nextY = groupedNodes[i+1].y
            ratio = (nextY - (groupedNodes[i].y + groupedNodes[i].height)) / screenDim
            weight = getWeightFromRatio(ratio,0.1)
        groupedNodes[i].weight = weight # TODO: set width or hight = 0 in mapping.
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
    if predictedComponent == 'android.widget.ImageView' or predictedComponent == 'android.widget.ImageButton':
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

def groupVerticalLeafNodes(groupedNodesI,imgH):
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
            groupedNodesVertical.append(createParentNodeVertical(backetNodes,imgH))
        indexUnvisited=getFirstUnvisitedIndex(visited)
    return groupedNodesVertical

def createParentNodeVertical(groupedNodes,imgH):
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
    groupedNodes = setWeights(groupedNodes,'y',imgH,False)
    parentNode.childNodes = groupedNodes
    return parentNode
 
def createParentNodeHorizontal(groupedNodes,imgW):
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
    groupedNodes = setWeights(groupedNodes,'x',imgW,False)
    parentNode.childNodes = groupedNodes
    return parentNode

def createLeavesParents(groupedNodes,img):
    parentNodes = []
    for i in range(len(groupedNodes)):
        groupedNodesVertical = groupVerticalLeafNodes(groupedNodes[i],img.shape[0])
        parentNode = createParentNodeHorizontal(groupedNodesVertical,img.shape[1])
        parentNodes.append(parentNode)
    return parentNodes
    
def buildParentNodes(boxes,texts,predictedComponents,img):
    groupedNodes = groupHorizontalLeafNodes(boxes,texts,predictedComponents,img)
    parentNodes = createLeavesParents(groupedNodes,img)
    return parentNodes

def createRoot(parentNodes,imgH):
    parentNode = node()
    parentNode.nodeType = "LinearLayoutVertical"
    parentNodes = setWeights(parentNodes,'y',imgH,True)
    parentNode.childNodes = parentNodes
    return parentNode
    
def buildHierarchy(boxes,texts,predictedComponents,img):
    parentNodes = buildParentNodes(boxes,texts,predictedComponents,img)
    rootNode = createRoot(parentNodes,img.shape[0])
    return rootNode

def mapToXml(parentNode,appName):
    # map and out xml file
    # ems of EditText = width of node/16px, hint
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
        " backgroundColor = "+parentNode.backgroundColor+
        " textColor = "+parentNode.textColor+
'''
def printNode(fTo,parentNode):        
    fTo.write('<'+parentNode.nodeType+" ("+" x = "+ str(parentNode.x)+
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
    
def printSpecialCase(parentNode):
    attributeString = ""
    if parentNode.nodeType == 'android.widget.EditText':
        attributeString += "android:hint="+'"'+parentNode.text+'"'+'\n'+ \
        "android:ems="+'"'+parentNode.width // 16+'dp"'+'\n'
   
    if parentNode.nodeType == 'android.widget.TextView'or parentNode.nodeType == 'android.widget.Button':
        attributeString += "android:text="+'"'+parentNode.text+'"'+'\n'+ \
        "android:textSize="+'"'+int(parentNode.height * 4/3) +'"'+'\n'
    
    if parentNode.nodeType == 'android.widget.ImageView'or parentNode.nodeType == 'android.widget.ImageButton':
        attributeString += "android:src="+'"'+"@drawable/"+parentNode.imagePath+'"'+'\n'
        
    if parentNode.nodeType == 'android.widget.ImageButton' or parentNode.nodeType == 'android.widget.Button':
         attributeString += "android:onClick="+'"'+"clickMe"+Constants.ID+'"'+'\n'
        
        
    