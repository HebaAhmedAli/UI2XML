from PyQt5 import QtWidgets, QtGui, QtCore
import os
import imagesize 
from GUI.skelPrevWindow import previewWindowSkel
from GUI.prevObjects import xmlTab, activityListItem
from GUI.componentHighlight import componentHighlight
import GUI.utils as utils
import Constants
import Utils

class previewWindow(QtWidgets.QWidget, previewWindowSkel):
    def __init__(self, parent):
        super(previewWindow, self).__init__(parent)
        self.setupUi(self)
        self.state = "UpdateCmpts"
        self.connectBtnState = False
        self.pixmapX = Constants.MONITOR_WIDTH*0.3
        self.pixmapY = Constants.MONITOR_HEIGHT*0.8
        self.updateBtn.clicked.connect(self.updateCompType)
        self.connectBtn.clicked.connect(self.connectToActivity)
        self.compTypeComboBox.currentIndexChanged.connect(self.enableUpdateBtn)
        self.changedCompIdx = None
        self.changedCompName = None
        self.mapAfterCorrecting = {}
        # The backend output
        self.imgsOutputInfo = Constants.mapToGui
        self.userCorrection = {}
        self.mapConnect = {}
        mainName = self.initActivitiesList()
        self.mainActivityDir = Constants.imagesPath+"/"+ mainName
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
        self.connectBtn.setEnabled(False)

        if self.connectBtnState :
            endI = imgName.rfind('.', 0, len(imgName))
            self.connectingActivityLbl.setText(imgName[:endI-2]+imgName[endI:])
            startI = self.activeImgDir.rfind('/', 0, len(self.activeImgDir))+1
            activeImgName = self.activeImgDir[startI:]
            self.mapConnect.update({self.highlights[self.changedCompIdx].idName:[activeImgName, imgName]})
            self.connectBtnState = False
            for activ in self.activitysHLayouts:
                activ.viewImg.setText("View")
                if(activ.imgpath == self.activeImgDir):
                    activ.viewImg.setEnabled(True)
            self.connectingActivityLbl.setText("")
        else:    
            if self.state == "UpdateCmpts":
                self.updateMapAfterCorrecting(self.activeImgDir)
                self.compTypeComboBox.setEnabled(False)
                self.compXMLBrowser = QtWidgets.QTextBrowser(self.xmlTabsverticalLayoutWidget)
                self.compXMLBrowser.setStyleSheet("background-color: \"white\";\n"           
                    "border: 5px solid  rgb(66, 138, 255);\n"
                    "color: rgb(45, 123, 250);\n"
                    "font-weight: bold;\n"
                    "border-radius: 20%;")                 
                self.xmlcomponentHLayout.addWidget(self.compXMLBrowser)
            self.compOriginalLbl.setText("")
            self.clearActiveImg()
            self.activeImgDir = imgPath

            self.updateActiveImg(imgPath)
            self.xmlTabs = QtWidgets.QTabWidget(self.xmlTabsverticalLayoutWidget)
            self.xmlTabsHLayout.addWidget(self.xmlTabs)
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
        self.imgsOutputInfo.get(imgName)[2] = compPreds
        if(len(compCorrectedPreds)>0):
            #self.mapAfterCorrecting.update({imgName :(compBoxes, compIDs, compCorrectedPreds)})
             self.mapAfterCorrecting.update( {imgName :[compBoxes, compIDs, compCorrectedPreds,
                Constants.mapToGui.get(imgName)[5]]})

    def viewCompDetails(self, index, compName):
        self.changedCompIdx = index
        self.changedCompName = compName
        if(self.state == "UpdateCmpts"):
            self.compTypeComboBox.setEnabled(True)
            compIdxinList = self.compTypeComboBox.findText(compName, QtCore.Qt.MatchFixedString)
            if compIdxinList >= 0:
                self.compTypeComboBox.setCurrentIndex(compIdxinList)
            startI = self.activeImgDir.rfind('/', 0, len(self.activeImgDir))+1
            imgName = self.activeImgDir[startI:]
            componentXML = Utils.getXmlOfComponent(index, imgName)
            self.compXMLBrowser.setPlainText(componentXML)
        elif (self.state == "ConnectCmpts"):
            self.connectBtnState = False
            for activ in self.activitysHLayouts:
                activ.viewImg.setText("View")
                activ.viewImg.setEnabled(True)
            self.connectBtn.setEnabled(True)
            self.connectingActivityLbl.setText("")

        self.updateBtn.setEnabled(False)
        self.compOriginalLbl.setText(compName)

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
        self.state = "ConnectCmpts"
        self.mapConnect = {}
        self.xmlcomponentHLayout.removeWidget(self.compXMLBrowser)
        del self.compXMLBrowser

        self.compTypeComboBox.setParent(None)
        del self.compTypeComboBox
        self.connectingActivityLbl = QtWidgets.QLabel()
        self.compoBoxLayout.addWidget(self.connectingActivityLbl)
        self.compNewTypeLbl.setText("Connected To :")
        self.connectingActivityLbl.setText("")
        self.onViewBtnClicked(self.mainActivityDir)

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
        self.xmlTabsHLayout.removeWidget(self.xmlTabs)
        for tab in self.activeImgXMLtabs:
            tab.setParent(None)
            del tab
        del self.xmlTabs
        if self.state != "ConnectCmpts": # Connect mode doesn't have component xml browser
            self.xmlcomponentHLayout.removeWidget(self.compXMLBrowser)
            del self.compXMLBrowser


    def refreshWindowAfterUpdate(self):
        for (key, val) in Constants.mapToGui.items():
            self.imgsOutputInfo.update({key:val})
        Constants.mapToGui = self.imgsOutputInfo
        self.mapAfterCorrecting = {}
        self.onViewBtnClicked(self.mainActivityDir)
        
    def connectToActivity(self):
        for activ in self.activitysHLayouts:
            activ.viewImg.setText("Connect")
            if(activ.imgpath == self.activeImgDir):
                activ.viewImg.setEnabled(False)
        self.connectBtnState=True
        # self.changedCompIdx