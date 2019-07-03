from PyQt5 import QtWidgets, QtGui, QtCore
import os
import imagesize 
from GUI.skelPrevWindow import previewWindowSkel
#from GUI.tabs import xmlTab
from GUI.prevObjects import xmlTab, activityListItem
from GUI.componentHighlight import componentHighlight
import GUI.utils as utils
import Constants
# import Utils

class previewWindow(QtWidgets.QWidget, previewWindowSkel):
    # updateCompSig = QtCore.pyqtSignal(str)
    def __init__(self, parent):
        super(previewWindow, self).__init__(parent)
        self.setupUi(self)
        self.state = "UpdateCmpts"
        self.connectBtnState = False
        self.pixmapX = Constants.MONITOR_WIDTH*0.3
        self.pixmapY = Constants.MONITOR_HEIGHT*0.84
        self.updateBtn.clicked.connect(self.updateCompType)
        self.connectBtn.clicked.connect(self.connectToActivity)
        self.compTypeComboBox.currentIndexChanged.connect(self.enableUpdateBtn)
        self.changedCompIdx = None
        self.changedCompName = None
        self.mapAfterCorrecting = {}
        # The backend output
        # self.imgsOutputInfo = Constants.mapToGui
        self.lol = {"mainND.jpg": [[[19, 19, 27, 27], [190, 135, 145, 124], [43, 311, 479, 63], [43, 405, 478, 64],
                [81, 557, 384, 46], [170, 634, 211, 31], [116, 844, 329, 27]],
                ['ImageButton_0_0_0', 'ImageView_0_1_0', 'EditText_0_2_0', 'EditText_0_3_0', 'ImageView_0_1_0', 'EditText_0_2_0', 'EditText_0_3_0'],
                ['ImageButton', 'ImageView', 'EditText', 'EditText', 'ImageButton', 'EditText', 'EditText'],
                ["activity.xml"]],
                
                'switchND.png': [[[26, 28, 41, 31], [117, 25, 105, 36], [555, 25, 17, 37], [228, 125, 145, 144], [173, 281, 255, 50], [129, 337, 341, 38],
                [0, 426, 300, 63], [26, 509, 41, 41], [117, 513, 204, 31], [21, 604, 51, 38], [116, 606, 239, 32], [500, 600, 74, 47], [28, 695, 37, 43],
                [117, 699, 159, 32], [506, 695, 73, 44],[0, 799, 300, 63], [25, 881, 44, 43], [116, 885, 184, 32]],
                ['ImageView_0_0_0', 'TextView_0_0_1', 'ImageView_0_0_2', 'ImageView_0_1_0', 'TextView_0_2_0', 'TextView_0_3_0', 'TextView_0_4_0',
                'ImageView_0_5_0', 'TextView_0_5_1', 'ImageView_0_6_0', 'TextView_0_6_1', 'Switch_0_6_2', 'ImageView_0_7_0', 'TextView_0_7_1',
                'Switch_0_7_2', 'TextView_0_8_0', 'ImageView_0_9_0', 'TextView_0_9_1'],
                ['ImageView', 'TextView', 'ImageView', 'ImageButton', 'TextView', 'TextView', 'TextView', 'ImageView', 'TextView', 'ImageView',
                'TextView', 'Button', 'ImageView', 'TextView', 'Switch', 'TextView', 'ImageView', 'TextView'],
                ['activity.xml', 'activity2.xml']]
                }
        self.imgsOutputInfo = self.lol
        self.userCorrection = {}
        self.mapConnect = {}
        mainName = self.initActivitiesList()
        self.mainActivityDir = Constants.imagesPath+"/"+ mainName
        # TODO: Handle if mainActivityName is None
        self.updateActiveImg(self.mainActivityDir)
        self.updateXMLTab(self.imgsOutputInfo[mainName][3])

    def initActivitiesList(self):
        projDir = Constants.imagesPath
        mainActivityName = "main"
        for imgName in self.imgsOutputInfo:
            endI = imgName.rfind('.', 0, len(imgName))
            if(mainActivityName==imgName[:endI-2]):
                mainActivityName = imgName
            imgDir = projDir+"/"+imgName
            self.userCorrection.update(imgName=[])
            imgName = imgName[:endI-2]+imgName[endI:]
            self.activityHLayout = activityListItem(imgDir, imgName)
            self.activityHLayout.activate.connect(self.onViewBtnClicked)
            self.activityHLayout.setAlignment(QtCore.Qt.AlignLeft)
            self.activitysHLayouts.append(self.activityHLayout)
            self.verticalLayout.addLayout(self.activityHLayout)
        self.mainActivityDir = projDir+"/"+mainActivityName
        self.activeImgDir = self.mainActivityDir
        return mainActivityName

    def calculateScaledBox(self, originalBox, imgW, imgH):
        scaledBox = []
        x1 = self.pixmapX*(originalBox[0]/imgW)
        y1 = self.pixmapY*(originalBox[1]/imgH)
        originalX2 = originalBox[0]+originalBox[2]
        originalY2 = originalBox[1]+originalBox[3]
        x2 = self.pixmapX*(originalX2/imgW)
        y2 = self.pixmapY*(originalY2/imgH)
        scaledBox.append(x1)
        scaledBox.append(y1)
        scaledBox.append(x2-x1)
        scaledBox.append(y2-y1)
        return scaledBox

    @QtCore.pyqtSlot(str)
    def onViewBtnClicked(self, imgPath):
        startI = imgPath.rfind('/', 0, len(imgPath))+1
        imgName = imgPath[startI:]

        if self.connectBtnState :
            startI = self.activeImgDir.rfind('/', 0, len(self.activeImgDir))+1
            activeImgName = self.activeImgDir[startI:]
            self.mapConnect.update({self.highlights[self.changedCompIdx].idName:[activeImgName, imgName]})
            self.connectBtnState = False
            for activ in self.activitysHLayouts:
                activ.viewImg.setText("View")
                if(activ.imgpath == self.activeImgDir):
                    activ.viewImg.setEnabled(True)
        else:    
            if self.state == "UpdateCmpts":
                self.updateMapAfterCorrecting(self.activeImgDir)
            self.compOriginalLbl.setText("")
            self.compTypeComboBox.setEnabled(False)
            self.clearActiveImg()
            self.activeImgDir = imgPath

            self.updateActiveImg(imgPath)
            self.xmlTabs = QtWidgets.QTabWidget(self.xmlTabsverticalLayoutWidget)
            self.xmlTabsverticalLayout.addWidget(self.xmlTabs)
            self.updateXMLTab(self.imgsOutputInfo[imgName][3])

    def updateMapAfterCorrecting(self, imgpath):
        startI = imgpath.rfind('/', 0, len(imgpath))+1
        imgName = imgpath[startI:]
        compBoxes = []
        compIDs = []
        compCorrectedPreds = []
        compPreds = []
        if imgName in self.mapAfterCorrecting:
            compBoxes = self.mapAfterCorrecting[imgName][0]
            compIDs = self.mapAfterCorrecting[imgName][1]
            compCorrectedPreds = self.mapAfterCorrecting[imgName][2]
        for component in self.highlights:
            if(component.changed):
                if(component.idName in compIDs):
                    idx = compIDs.index(component.idName)
                    compCorrectedPreds[idx] = 'android.widget.'+component.predicted
                else:
                    compBoxes.append(component.box)
                    compIDs.append(component.idName)
                    compCorrectedPreds.append('android.widget.'+component.predicted)
            compPreds.append(component.predicted)
            component.setParent(None)
            del component
        print("k  ",imgName, compPreds)
        self.imgsOutputInfo.get(imgName)[2] = compPreds
        if(len(compCorrectedPreds)>0):
            self.mapAfterCorrecting.update({imgName :(compBoxes, compIDs, compCorrectedPreds)})
            # self.mapAfterCorrecting.update( {imgName :[compBoxes, compIDs, compCorrectedPreds,
            #     Constants.mapToGui.get(imgName)[5]]})

    def viewCompDetails(self, index, compName):
        self.changedCompIdx = index
        self.changedCompName = compName
        if(self.state == "UpdateCmpts"):
            self.compTypeComboBox.setEnabled(True)
            compIdxinList = self.compTypeComboBox.findText(compName, QtCore.Qt.MatchFixedString)
            if compIdxinList >= 0:
                self.compTypeComboBox.setCurrentIndex(compIdxinList)
        elif (self.state == "ConnectCmpts"):
            self.connectBtnState = False
            for activ in self.activitysHLayouts:
                activ.viewImg.setText("View")
                activ.viewImg.setEnabled(True)
            self.compTypeComboBox.setEnabled(False)
            self.connectBtn.setEnabled(True)

        self.updateBtn.setEnabled(False)
        self.compOriginalLbl.setText(compName)
        # startI = self.activeImgDir.rfind('/', 0, len(self.activeImgDir))+1
        # imgName = self.activeImgDir[startI:]
        # componentXML = Utils.getXmlOfComponent(index, imgName)
        componentXML = "YALL\nLLLLLL\nLL\n\n\n\nLLLLAHWE"
        # curTab = self.xmlTabs.currentWidget()
        for tab in self.activeImgXMLtabs:
            tab.compXMLBrowser.setPlainText(componentXML)

    def enableUpdateBtn(self):
        self.updateBtn.setEnabled(True)
   
    def updateCompType(self):
        self.changedCompName = self.compTypeComboBox.currentText()
        self.highlights[self.changedCompIdx].predicted=self.changedCompName
        self.highlights[self.changedCompIdx].changed=True
        self.updateBtn.setEnabled(False)

    def updateXMLTab(self, xmlFiles):
        xmlDir = Constants.imagesPath[:-5] + Constants.androidPath + "/res/layout"
        self.activeImgXMLtabs = []
        for xmlFile in xmlFiles:
            tab = xmlTab()
            text=open(str(xmlDir+"/"+xmlFile)).read()
            tab.textBrowser.setPlainText(text)
            self.activeImgXMLtabs.append(tab)
            self.xmlTabs.addTab(tab, xmlFile[:-4])

    def updateActiveImg(self, imagePath):
        startI = imagePath.rfind('/', 0, len(imagePath))+1
        imgName = imagePath[startI:]
        self.activeImageWidget = QtWidgets.QWidget()
        self.activeImageLayout = QtWidgets.QVBoxLayout(self.activeImageWidget)
        self.imageLabel = QtWidgets.QLabel()
        self.pixmapimage = QtGui.QPixmap(imagePath).scaled(self.pixmapX, self.pixmapY)
        self.imageLabel.setPixmap(QtGui.QPixmap(self.pixmapimage))
        self.activeImageLayout.addWidget(self.imageLabel)
        compBoxes = self.imgsOutputInfo[imgName][0]
        compIDs = self.imgsOutputInfo[imgName][1]
        compPreds = self.imgsOutputInfo[imgName][2]
        self.highlights = []
        imgW, imgH = imagesize.get(imagePath)
        for idx in range(0,len(compBoxes)):
            if self.state == "ConnectCmpts" and \
                    not (compPreds[idx] == "Button" or compPreds[idx] == "ImageButton"):
                continue
            compBox =compBoxes[idx]
            compId = compIDs[idx]
            compPred = compPreds[idx]
            scaledCompBox =  self.calculateScaledBox(compBox, imgW, imgH)
            if compPreds[idx] == Constants.MODEL_PRED[2]:
                scaledCompBox[1] = scaledCompBox[1] - 15
                scaledCompBox[3] = scaledCompBox[3] + 15
            high = componentHighlight(self.activeImageWidget, scaledCompBox, compBox, compId, compPred, len(self.highlights))
            
            high.showComp.connect(self.viewCompDetails)
            self.highlights.append(high)
        self.activeImgverticalLayout.addWidget(self.activeImageWidget)

    def generateUpdatedXML(self):
        self.updateMapAfterCorrecting(self.activeImgDir)
        return self.mapAfterCorrecting

    def connectCmptsStart(self):
        #todo call update function to the rest components
        self.state = "ConnectCmpts"
        self.mapConnect = {}   
        self.onViewBtnClicked(self.mainActivityDir)
        # self.convertMapToLists()

    def convertConnectMapToLists(self):
        connectedActivities = []
        for key, value in self.mapConnect.items():
            lst = [key, value[0], value[1]]
            connectedActivities.append(lst)
        return connectedActivities

    def clearActiveImg(self):
        self.imageLabel.setParent(None)
        del self.pixmapimage
        self.activeImageLayout.removeWidget(self.imageLabel)
        del self.imageLabel
        self.activeImgverticalLayout.removeWidget(self.activeImageWidget)
        self.xmlTabsverticalLayout.removeWidget(self.xmlTabs)
        for tab in self.activeImgXMLtabs:
            tab.setParent(None)
            del tab
        del self.xmlTabs

    def refreshWindowAfterUpdate(self):
        # self.imgsOutputInfo = Constants.mapToGui
        self.imgsOutputInfo = self.lol
        self.mapAfterCorrecting = {}
        self.onViewBtnClicked(self.mainActivityDir)
        
    def connectToActivity(self):
        for activ in self.activitysHLayouts:
            activ.viewImg.setText("Connect")
            if(activ.imgpath == self.activeImgDir):
                activ.viewImg.setEnabled(False)
        self.connectBtnState=True
        # self.changedCompIdx