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
    def __init__(self, parent):
        super(previewWindow, self).__init__(parent)
        self.setupUi(self)
        self.pixmapX = Constants.MONITOR_WIDTH/3
        self.pixmapY = Constants.MONITOR_HEIGHT*0.87
        # The backend output
        # imgsOutputInfo = Constants.mapToGui
        self.imgsOutputInfo = {"mainND.jpg": ([[19, 19, 27, 27], [190, 135, 145, 124], [43, 311, 479, 63], [43, 405, 478, 64],
                [81, 557, 384, 46], [170, 634, 211, 31], [116, 844, 329, 27]],
                ['ImageButton_0_0_0', 'ImageView_0_1_0', 'EditText_0_2_0', 'EditText_0_3_0', 'ImageView_0_1_0', 'EditText_0_2_0', 'EditText_0_3_0'],
                ['ImageButton', 'ImageView', 'EditText', 'EditText', 'ImageView', 'EditText', 'EditText'],
                ["activity.xml", "activity2.xml"]),
                "kolND.jpg": ([[19, 19, 27, 27], [190, 135, 145, 124], [43, 311, 479, 63], [43, 405, 478, 64]],
               ['ImageButton_0_0_0', 'ImageView_0_1_0', 'EditText_0_2_0', 'EditText_0_3_0', 'ImageView_0_1_0', 'EditText_0_2_0', 'EditText_0_3_0'],
                ['ImageButton', 'ImageView', 'EditText', 'EditText', 'ImageView', 'EditText', 'EditText'],
                ["activity.xml", "activity2.xml"])
                }
        self.userCorrection = {}
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

        mainActivityDir = projDir+"/"+mainActivityName
        self.activeImgDir=mainActivityDir
        self.activeImageWidget = QtWidgets.QWidget()
        self.activeImageLayout = QtWidgets.QVBoxLayout(self.activeImageWidget)
        self.imageLabel = QtWidgets.QLabel(self.activeImgVerticalLayoutWidget)
        self.pixmapimage = QtGui.QPixmap(mainActivityDir).scaled(self.pixmapX, self.pixmapY)
        self.imageLabel.setPixmap(QtGui.QPixmap(self.pixmapimage))
        self.activeImageLayout.addWidget(self.imageLabel)
        compBoxes = self.imgsOutputInfo[mainActivityName][0]
        compIDs = self.imgsOutputInfo[mainActivityName][1]
        compPreds = self.imgsOutputInfo[mainActivityName][2]
        self.highlights = []
        imgW, imgH = imagesize.get(mainActivityDir)
        for idx in range(0,len(compBoxes)):
            compBox =compBoxes[idx]
            compId = compIDs[idx]
            compPred = compPreds[idx]
            scaledCompBox =  self.calculateScaledBox(compBox, imgW, imgH)
            if compPreds[idx] == "EditText":
                scaledCompBox[1] = scaledCompBox[1] - 15
                scaledCompBox[3] = scaledCompBox[3] + 15
            high = componentHighlight(self.activeImageWidget, scaledCompBox, compBox, compId, compPred)
            self.highlights.append(high)
        self.activeImgverticalLayout.addWidget(self.activeImageWidget)
        self.updateXMLTab(self.imgsOutputInfo[mainActivityName][3])

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
        print("k",imgPath)
        if self.activeImgDir==imgPath:
            return
        startI = imgPath.rfind('/', 0, len(imgPath))+1
        imgName = imgPath[startI:]
        self.activeImgDir = imgPath
        for h in self.highlights:
            h.setParent(None)
            del h
        # del self.highlights
        del self.pixmapimage
        self.imageLabel.setParent(None)
        del self.imageLabel
        self.imageLabel = QtWidgets.QLabel(self.activeImgVerticalLayoutWidget)
        self.pixmapimage = QtGui.QPixmap(self.activeImgDir).scaled(self.pixmapX, self.pixmapY)
        self.imageLabel.setPixmap(QtGui.QPixmap(self.pixmapimage))
        self.activeImageLayout.addWidget(self.imageLabel)
        compBoxes = self.imgsOutputInfo[imgName][0]
        compIDs = self.imgsOutputInfo[imgName][1]
        compPreds = self.imgsOutputInfo[imgName][2]
        self.highlights = []
        imgW, imgH = imagesize.get(self.activeImgDir)
        for idx in range(0,len(compBoxes)):
            compBox =compBoxes[idx]
            compId = compIDs[idx]
            compPred = compPreds[idx]
            scaledCompBox =  self.calculateScaledBox(compBox, imgW, imgH)
            if compPreds[idx] == "EditText":
                scaledCompBox[1] = scaledCompBox[1] - 15
                scaledCompBox[3] = scaledCompBox[3] + 15
            high = componentHighlight(self.activeImageWidget, scaledCompBox, compBox, compId, compPred)
            self.highlights.append(high)
        self.activeImgverticalLayout.addWidget(self.activeImageWidget)
    

    def updateXMLTab(self, xmlFiles):
        xmlDir = Constants.imagesPath + "/output/main/res/layout"
        for xmlFile in xmlFiles:
            tab = xmlTab()
            text=open(str(xmlDir+"/"+xmlFile)).read()
            tab.textBrowser.setPlainText(text)
            self.xmlTabs.addTab(tab, xmlFile[:-4])