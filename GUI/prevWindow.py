from PyQt5 import QtWidgets, QtGui, QtCore
import os
import imagesize 
from GUI.skelPrevWindow import  previewWindowSkel
#from GUI.tabs import xmlTab
from GUI.prevObjects import xmlTab, activityListItem
from GUI.componentHighlight import componentHighlight
import GUI.utils as utils
import Constants

class previewWindow(QtWidgets.QWidget, previewWindowSkel):
    def __init__(self):
        super(previewWindow, self).__init__()
        self.setupUi(self)
        self.pixmapX = Constants.MONITOR_WIDTH/3
        self.pixmapY = Constants.MONITOR_HEIGHT*0.87
        # The backend output
        imgsOutputInfo = Constants.mapToGui
        self.userCorrection = {}
        projDir = Constants.imagesPath
        mainActivityName = "main"
        for imgName in imgsOutputInfo:
            endI = imgName.rfind('.', 0, len(imgName))
            if(mainActivityName==imgName[:endI-2]):
                mainActivityName = imgName
            imgDir = projDir+"/"+imgName
            self.userCorrection.update(imgName=[])
            imgName = imgName[:endI-2]+imgName[endI:]
            activityHLayout = activityListItem(imgDir, imgName)
            activityHLayout.setAlignment(QtCore.Qt.AlignLeft)
            self.activitysHLayouts.append(activityHLayout)
            self.verticalLayout.addLayout(activityHLayout)
        mainActivityDir = projDir+"/"+mainActivityName
        self.activeImageWidget = QtWidgets.QWidget()
        activeImageLayout = QtWidgets.QVBoxLayout(self.activeImageWidget)
        imageLabel = QtWidgets.QLabel(self.activeImgVerticalLayoutWidget)
        pixmapimage = QtGui.QPixmap(mainActivityDir).scaled(self.pixmapX, self.pixmapY)
        imageLabel.setPixmap(QtGui.QPixmap(pixmapimage))
        activeImageLayout.addWidget(imageLabel)
        compBoxes = imgsOutputInfo[mainActivityName][0]
        compIDs = imgsOutputInfo[mainActivityName][1]
        compPreds = imgsOutputInfo[mainActivityName][2]
        self.highlights = []
        imgW, imgH = imagesize.get(mainActivityDir)
        for idx in range(0,len(compBoxes)):
            compBox =compBoxes[idx]
            compId = compIDs[idx]
            compPred = compPreds[idx]
            scaledCompBox =  self.calculateScaledBox(compBox, imgW, imgH)
            high = componentHighlight(self.activeImageWidget, scaledCompBox, compBox, compId, compPred)
            self.highlights.append(high)
        self.activeImgverticalLayout.addWidget(self.activeImageWidget)
        self.updateXMLTab(imgsOutputInfo[mainActivityName][3])

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
    

    def updateXMLTab(self, xmlFiles):
        xmlDir = Constants.imagesPath + "/app/src/main/res/layout"
        for xmlFile in xmlFiles:
            tab = xmlTab()
            text=open(str(xmlDir+"/"+xmlFile)).read()
            tab.textBrowser.setPlainText(text)
            self.xmlTabs.addTab(tab, xmlFile[:-4])