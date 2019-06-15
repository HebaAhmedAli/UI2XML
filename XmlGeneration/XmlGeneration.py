import sys
sys.path.append('../')
import Utils
import Constants
import XmlGeneration.JavaGeneration as JavaGeneration
import os
import cv2
import operator
import re

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
        self.backgroundColor = "white"
        self.textColor = "black"
        self.imagePath = ""
        self.height = ""  # ex: fixed no , wrap_content ,match_parent
        self.width = ""   # ex: fixed no , wrap_content ,match_parent
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
    if not root:
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
                groupedNodes[i].weight = 1 # TODO: set width or hight = 0 in mapping.
                return groupedNodes
            else:
                nextY = groupedNodes[i+1].y
            ratio = (nextY - (groupedNodes[i].y)) / screenDim
            weight = getWeightFromRatio(ratio,0.15)
        groupedNodes[i].weight = weight # TODO: set width or hight = 0 in mapping.
    return groupedNodes


# set nodeType , text , color , x, y , width , hight , imagePath here.
def createLeafNode(box,text,predictedComponent,img):
    leafNode = node()
    leafNode.x = box[0]
    leafNode.y = box[1]
    leafNode.width = box[2]
    leafNode.height = box[3]
    finalText = " ".join(re.findall(r"[a-zA-Z0-9]+", text))
    leafNode.text = finalText
    leafNode.nodeType = predictedComponent
    if predictedComponent == 'android.widget.ImageView' or predictedComponent == 'android.widget.ImageButton':
        if not os.path.exists(Constants.DIRECTORY+'/drawable'):
            os.makedirs(Constants.DIRECTORY+'/drawable')
        cropImg = img[leafNode.y:leafNode.y+leafNode.height, leafNode.x:leafNode.x+leafNode.width]
        cv2.imwrite(Constants.DIRECTORY+'/drawable/'+"pic_"+str(leafNode.x)+'_'+str(leafNode.y)+'.png',cropImg)
        leafNode.imagePath = "pic_"+str(leafNode.x)+'_'+str(leafNode.y)
    if predictedComponent == 'android.widget.TextView' or predictedComponent == 'android.widget.Button':
        firstColor,secondColor = Utils.getMostAndSecondMostColors()
        leafNode.backgroundColor = firstColor
        leafNode.textColor = secondColor
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
            groupedNodesVertical.append(createParentNodeVertical(backetNodes,imgH,"LinearLayoutVertical"))
        indexUnvisited=getFirstUnvisitedIndex(visited)
    return groupedNodesVertical

def createParentNodeVertical(groupedNodes,imgH,parentType):
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
    groupedNodes = setWeights(groupedNodes,'y',imgH,False)
    parentNode.childNodes = groupedNodes
    return parentNode
 
def createParentNodeHorizontal(groupedNodes,imgW):
    parentNode = node()
    parentNode.nodeType = "LinearLayoutHorizontal"
    #parentNode.width = "match_parent"
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
    parentNode.height = maxY - minY
    if len(groupedNodes) == 1 :
        if abs(groupedNodes[0].x+0.5*groupedNodes[0].width - imgW/2) <= 30:
            parentNode.gravity = "center"
        parentNode.childNodes = groupedNodes
        return parentNode
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

def createRoot(parentNodes,imgH,asIs):
    parentNode = node()
    parentNode.nodeType = "LinearLayoutVertical"
    parentNodes = sorted(parentNodes, key=operator.attrgetter('y'))
    if asIs == False:
        parentNodes = groupListViewAndRadio(parentNodes,imgH)
    else:
        parentNodes = groupRadio(parentNodes,imgH)
    parentNodes = setWeights(parentNodes,'y',imgH,True)
    parentNode.childNodes = parentNodes
    return parentNode
    
def buildHierarchy(boxes,texts,predictedComponents,img):
    parentNodes = buildParentNodes(boxes,texts,predictedComponents,img)
    rootNode = createRoot(parentNodes,img.shape[0],False)
    rootNodeAsIs = createRoot(parentNodes,img.shape[0],True)
    return rootNode,rootNodeAsIs

def getTypeAndOriAndID(parentNode,tabsString):
    if parentNode.nodeType == 'LinearLayoutVertical':
        return 'LinearLayout\n'+tabsString+'\t'+'android:orientation = "vertical"'\
                '\n'+tabsString+'\t'
    elif parentNode.nodeType == 'LinearLayoutHorizontal':
        return 'LinearLayout\n'+tabsString+'\t'+'android:orientation = "horizontal"'\
                '\n'+tabsString+'\t'
    parentNode.id =  Constants.ID
    toReturn = parentNode.nodeType[15:len(parentNode.nodeType)]+'\n'+tabsString+'\t'+'android:id = "@+id/'+parentNode.nodeType[15:len(parentNode.nodeType)]+str(parentNode.id) \
                +'"\n'+tabsString+'\t'                
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
        'android:textColor = "@android:color/'+parentNode.textColor+'"'+'\n'+tabsString+'\t'+\
        'android:background = "@android:color/'+parentNode.backgroundColor+'"'+'\n'+tabsString+'\t'
        
    if (parentNode.nodeType == 'android.widget.RadioButton' or parentNode.nodeType == 'android.widget.CheckBox')\
    and parentNode.text != "":
        attributeString += "android:text = "+'"'+parentNode.text.replace('"','t')+'"'+'\n'+tabsString+'\t'
        
 
    if parentNode.nodeType == 'android.widget.ImageView'or parentNode.nodeType == 'android.widget.ImageButton':
        attributeString += "android:src = "+'"'+"@drawable/"+parentNode.imagePath+'"'+'\n'+tabsString+'\t'
        
    if parentNode.nodeType == 'android.widget.ImageButton' or parentNode.nodeType == 'android.widget.Button':
         attributeString += "android:onClick = "+'"'+"clickMe"+str(Constants.ID-1)+'"'+'\n'+tabsString+'\t'
         
    if parentNode.nodeType == 'android.widget.Button':
        attributeString+= 'android:gravity = "center'+'"'+'\n'+tabsString+'\t'
    return attributeString

def printSpecialCaseListView(parentNode,tabsString,imgH):
    attributeString = ""
    
    if parentNode.nodeType == 'android.widget.TextView':
        attributeString +='android:textColor = "@android:color/'+parentNode.textColor+'"'+'\n'+tabsString+'\t'+\
        'android:background = "@android:color/'+parentNode.backgroundColor+'"'+'\n'+tabsString+'\t'+\
        "android:text = "+'"'+parentNode.text.replace('"','t')+'"'+'\n'+tabsString+'\t'
        
    if parentNode.nodeType == 'android.widget.ImageView'or parentNode.nodeType == 'android.widget.ImageButton':
        attributeString += "android:src = "+'"'+"@drawable/"+parentNode.imagePath+'"'+'\n'+tabsString+'\t'
      
    return attributeString

def printListViewChildNode(parentNode,myParentType,tabs,imgH):
    tabsString=""
    for i in range(tabs):
        tabsString+='\t'
    returnString=""
    returnString+= tabsString+'<'+getTypeAndOriAndID(parentNode,tabsString)+\
                  getWeightWidthHeightGravity(myParentType,parentNode.height,parentNode.width\
                                    ,parentNode.gravity,parentNode.weight,tabsString)+\
                                    printSpecialCaseListView(parentNode,tabsString,imgH)+'>\n'                                  
    for i in range(len(parentNode.childNodes)) :                                   
        returnString += printListViewChildNode(parentNode.childNodes[i],parentNode.nodeType,2,imgH)
    returnString+= tabsString+"</"+ getType(parentNode.nodeType)+'>'+'\n'
                                    
    return returnString

def printNodeXml(fTo,parentNode,myParentType,tabs,imgH,actionBarOp):    
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
        fTo.write(tabsString+'<'+getTypeAndOriAndID(parentNode,tabsString)+\
                  getWeightWidthHeightGravity(myParentType,parentNode.height,parentNode.width\
                                    ,parentNode.gravity,parentNode.weight,tabsString)+\
                                    printSpecialCase(parentNode,tabsString,imgH)+'>\n')
    if len(parentNode.childNodes)==0:
        fTo.write(tabsString+"</"+ getType(parentNode.nodeType)+'>'+'\n')
        return
    
    if parentNode.nodeType == 'android.widget.ListView':
        fToListView=open(Constants.DIRECTORY+'/layout/'+'list_view_'+str(Constants.ID-1)+'.xml', 'w+')
        fileOuput = '<?xml version = "1.0" encoding = "utf-8"?>\n'+\
        '<LinearLayout xmlns:android = "http://schemas.android.com/apk/res/android"\n'\
        +'\t'+'xmlns:app = "http://schemas.android.com/apk/res-auto"\n'\
        +'\t'+'xmlns:tools = "http://schemas.android.com/tools"\n'\
        +'\t'+'android:layout_width = "match_parent"\n'\
        +'\t'+'android:layout_height = "match_parent"\n'\
        +'\t'+'android:orientation = "vertical"'+'>\n'
        fToListView.write(fileOuput)            
        fToListView.write(printListViewChildNode(parentNode.childNodes[0],parentNode.nodeType,1,imgH))
        fToListView.write("</LinearLayout>"+'\n')    
        fToListView.close()    
        
    else:
        if actionBarOp == 'A' and tabs == 0:
            fToActionBar=open(Constants.DIRECTORY+'/layout/'+'action_bar_'+myParentType+'.xml', 'w+')
            fileOuput = '<?xml version = "1.0" encoding = "utf-8"?>\n'+\
                '<LinearLayout xmlns:android = "http://schemas.android.com/apk/res/android"\n'\
                +'\t'+'xmlns:app = "http://schemas.android.com/apk/res-auto"\n'\
                +'\t'+'xmlns:tools = "http://schemas.android.com/tools"\n'\
                +'\t'+'android:layout_width = "match_parent"\n'\
                +'\t'+'android:layout_height = "wrap_content"\n'\
                +'\t'+'android:orientation = "horizontal"'+'>\n'
            fToActionBar.write(fileOuput) 
            for i in range(0,len(parentNode.childNodes[0].childNodes)):
                printNodeXml(fToActionBar,parentNode.childNodes[0].childNodes[i],parentNode.childNodes[0].nodeType,1,imgH,actionBarOp)
            fToActionBar.write("</LinearLayout>"+'\n')    
            fToActionBar.close() 
            for i in range(1,len(parentNode.childNodes)):
                printNodeXml(fTo,parentNode.childNodes[i],parentNode.nodeType,tabs+1,imgH,actionBarOp)
        else:
            for i in range(len(parentNode.childNodes)):
                printNodeXml(fTo,parentNode.childNodes[i],parentNode.nodeType,tabs+1,imgH,actionBarOp)
    fTo.write(tabsString+"</"+ getType(parentNode.nodeType)+'>'+'\n')
        
def mapToXml(parentNode,appName,imgH,actionBarOp):
    if not os.path.exists(Constants.DIRECTORY+'/layout'):
            os.makedirs(Constants.DIRECTORY+'/layout') 
    fTo=open(Constants.DIRECTORY+'/layout/'+'activity_'+appName+'.xml', 'w+')
    printNodeXml(fTo,parentNode,appName,0,imgH,actionBarOp)
    return

def mapToXmlAsIs(parentNode,appName,imgH,actionBarOp):
    if not os.path.exists(Constants.DIRECTORY+'/layoutAsIs'):
            os.makedirs(Constants.DIRECTORY+'/layoutAsIs') 
    fTo=open(Constants.DIRECTORY+'/layoutAsIs/'+'activity_'+appName+'.xml', 'w+')
    printNodeXml(fTo,parentNode,appName,0,imgH,actionBarOp)
    return
    
def generateXml(boxes,texts,predictedComponents,img,appName,actionBarOp):
    parentNode,parentNodeAsIs=buildHierarchy(boxes,texts,predictedComponents,img)
    mapToXml(parentNode,appName,img.shape[0],actionBarOp)
    JavaGeneration.generateJava(parentNode,appName,actionBarOp)
    mapToXmlAsIs(parentNodeAsIs,appName,img.shape[0],'N')
    # To test.
    # printHierarchy(parentNode,appName)
    return

def groupListViewAndRadio(groupedNodes,imgH):
    groupedNodesNew = []
    i = 0
    while i<len(groupedNodes):
        patternToSearch = extractPatternOfNode(groupedNodes[i])
        lastIndex = getLastPatternIndex(i,groupedNodes,patternToSearch)
        if lastIndex != i:
            childs = groupedNodes[i:lastIndex+1]
            if patternToSearch ==  'android.widget.RadioButton':
                groupedNodesNew.append(createParentNodeVertical(childs,imgH,'android.widget.RadioGroup'))
                i = lastIndex
            elif lastIndex-i>=3 and patternToSearch.find('android.widget.TextView') != -1:
                groupedNodesNew.append(createParentNodeVertical(childs,imgH,'android.widget.ListView'))
                i = lastIndex
            else:
                groupedNodesNew.append(groupedNodes[i])
        else:
            groupedNodesNew.append(groupedNodes[i])
        i+=1
    return groupedNodesNew

def groupRadio(groupedNodes,imgH):
    groupedNodesNew = []
    i = 0
    while i<len(groupedNodes):
        patternToSearch = extractPatternOfNode(groupedNodes[i])
        lastIndex = getLastPatternIndex(i,groupedNodes,patternToSearch)
        if lastIndex != i and patternToSearch ==  'android.widget.RadioButton':
            childs = groupedNodes[i:lastIndex+1]
            groupedNodesNew.append(createParentNodeVertical(childs,imgH,'android.widget.RadioGroup'))
            i = lastIndex
        else:
            groupedNodesNew.append(groupedNodes[i])
        i+=1
    return groupedNodesNew

def extractPatternOfNode(parentNode):
    pattern = ""
    for i in range(len(parentNode.childNodes)):
        pattern += parentNode.childNodes[i].nodeType
        if parentNode.childNodes[i].nodeType == 'android.widget.RadioButton':
            return parentNode.childNodes[i].nodeType
    return pattern
        
def getLastPatternIndex(firstIndex,groupedNodes,pattern):
    for i in range(firstIndex+1,len(groupedNodes)):
        if extractPatternOfNode(groupedNodes[i]) != pattern:
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

    