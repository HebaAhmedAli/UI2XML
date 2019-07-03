from PyQt5 import QtWidgets, QtGui, QtCore
import os
import imagesize 
from GUI.skelPrevWindow import previewWindowSkel
#from GUI.tabs import xmlTab
from GUI.prevObjects import xmlTab, activityListItem
from GUI.componentHighlight import componentHighlight
import GUI.utils as utils
import Constants
import Utils

class previewWindow(QtWidgets.QWidget, previewWindowSkel):
    # updateCompSig = QtCore.pyqtSignal(str)
    def __init__(self, parent):
        super(previewWindow, self).__init__(parent)
        self.setupUi(self)
        self.pixmapX = Constants.MONITOR_WIDTH*0.3
        self.pixmapY = Constants.MONITOR_HEIGHT*0.8
        self.updateBtn.clicked.connect(self.updateCompType)
        # self.connectBtn.clicked.connect(self.generateUpdatedXML)
        self.compTypeComboBox.currentIndexChanged.connect(self.enableUpdateBtn)
        self.changedCompIdx = None
        self.changedCompName = None
        self.mapAfterCorrecting = {}
        # The backend output
        self.imgsOutputInfo = Constants.mapToGui
        self.userCorrection = {}
        mainActivityName = self.initActivitiesList()
        # TODO: Handle if mainActivityName is None
        self.updateActiveImg(self.mainActivityDir)
        self.updateXMLTab(self.imgsOutputInfo[mainActivityName][3])

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
        #if self.activeImgDir==imgPath:
         #   return
        self.updateMapAfterCorrecting()
        self.activeImgDir = imgPath
        del self.pixmapimage
        self.activeImageLayout.removeWidget(self.imageLabel)
        del self.imageLabel
        self.compOriginalLbl.setText("")
        self.compTypeComboBox.setEnabled(False)
        startI = imgPath.rfind('/', 0, len(imgPath))+1
        imgName = imgPath[startI:]

        self.activeImgverticalLayout.removeWidget(self.activeImageWidget)
        self.updateActiveImg(imgPath)
        self.xmlTabsverticalLayout.removeWidget(self.xmlTabs)
        for tab in self.activeImgXMLtabs:
            tab.setParent(None)
            del tab
        del self.xmlTabs
        self.xmlTabs = QtWidgets.QTabWidget(self.xmlTabsverticalLayoutWidget)
        self.xmlTabsverticalLayout.addWidget(self.xmlTabs)
        self.updateXMLTab(self.imgsOutputInfo[imgName][3])

    def updateMapAfterCorrecting(self):
        startI = self.activeImgDir.rfind('/', 0, len(self.activeImgDir))+1
        imgName = self.activeImgDir[startI:]
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
        self.compTypeComboBox.setEnabled(True)
        compIdxinList = self.compTypeComboBox.findText(compName, QtCore.Qt.MatchFixedString)
        if compIdxinList >= 0:
            self.compTypeComboBox.setCurrentIndex(compIdxinList)
        self.updateBtn.setEnabled(False)
        self.compOriginalLbl.setText(compName)
        self.changedCompIdx = index
        self.changedCompName = compName
        startI = self.activeImgDir.rfind('/', 0, len(self.activeImgDir))+1
        imgName = self.activeImgDir[startI:]
        componentXML = Utils.getXmlOfComponent(index, imgName)
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
            compBox =compBoxes[idx]
            compId = compIDs[idx]
            compPred = compPreds[idx]
            scaledCompBox =  self.calculateScaledBox(compBox, imgW, imgH)
            if compPreds[idx] == Constants.MODEL_PRED[2]:
                scaledCompBox[1] = scaledCompBox[1] - 15
                scaledCompBox[3] = scaledCompBox[3] + 15
            high = componentHighlight(self.activeImageWidget, scaledCompBox, compBox, compId, compPred, idx)
            high.showComp.connect(self.viewCompDetails)
            self.highlights.append(high)
        self.activeImgverticalLayout.addWidget(self.activeImageWidget)

    def generateUpdatedXML(self):
        self.updateMapAfterCorrecting()
        return self.mapAfterCorrecting

    def refreshWindowAfterUpdate(self):
        self.imgsOutputInfo = Constants.mapToGui
        self.mapAfterCorrecting = {}
        self.onViewBtnClicked(self.mainActivityDir)
        