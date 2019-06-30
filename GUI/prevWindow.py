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
        self.pixmapX = 400
        self.pixmapY = 700
        # The backend output
        imgsOutputInfo = {"mainND.jpg": ([[19, 19, 27, 27], [190, 135, 145, 124], [43, 311, 479, 63], [43, 405, 478, 64],
                [81, 557, 384, 46], [170, 634, 211, 31], [116, 844, 329, 27]],
                ['ImageButton_0_0_0', 'ImageView_0_1_0', 'EditText_0_2_0', 'EditText_0_3_0'],
                ['ImageButton', 'ImageView', 'EditText', 'EditText'],
                ["activity.xml", "activity2.xml"]),
                "kolND.jpg": ([[19, 19, 27, 27], [190, 135, 145, 124], [43, 311, 479, 63], [43, 405, 478, 64]],
                ['ImageButton_0_0_0', 'ImageView_0_1_0', 'EditText_0_2_0', 'EditText_0_3_0'],
                ['ImageButton', 'ImageView', 'EditText', 'EditText'],
                ["activity.xml", "activity2.xml"])
                }
        self.activitiesList.itemDoubleClicked.connect(self.updateActiveImg)
        projDir = Constants.imagesPath
        mainActivityName = "main"
        for imgName in imgsOutputInfo:
            endI = imgName.rfind('.', 0, len(imgName))
            if(mainActivityName==imgName[:endI-2]):
                mainActivityName = imgName
            imgDir = projDir+"/"+imgName
            imgName = imgName[:endI-2]+imgName[endI:]
            item = activityListItem(imgDir, imgName)
            self.activitiesList.addItem(item)

        mainActivityDir = projDir+"/"+mainActivityName
        self.activeImageWidget = QtWidgets.QWidget()
        self.activeImageLayout = QtWidgets.QVBoxLayout(self.activeImageWidget)
        self.imageLabel = QtWidgets.QLabel(self.activeImgVerticalLayoutWidget)
        self.pixmapimage = QtGui.QPixmap(mainActivityDir).scaled(self.pixmapX, self.pixmapY)
        self.imageLabel.setPixmap(QtGui.QPixmap(self.pixmapimage))
        self.activeImageLayout.addWidget(self.imageLabel)
        imageboxs = imgsOutputInfo[mainActivityName][0]
        self.highlights = []
        imgW, imgH = imagesize.get(mainActivityDir)
        for compBox in imageboxs:
            scaledCompBox =  self.calculateScaledBox(compBox, imgW, imgH)
            errorMargin = 10
            high = componentHighlight(self.activeImageWidget, scaledCompBox[2]+errorMargin, scaledCompBox[3]+errorMargin)
            high.move(scaledCompBox[0]+errorMargin, scaledCompBox[1]+errorMargin)
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
        xmlDir = Constants.imagesPath + "/layouts"
        for xmlFile in xmlFiles:
            tab = xmlTab()
            text=open(str(xmlDir+"/"+xmlFile)).read()
            tab.textBrowser.setPlainText(text)
            self.xmlTabs.addTab(tab, xmlFile[:-4])

    def updateActiveImg(self, item):
        print("recieving")
        print(item.imgPath)
        del self.pixmapimage
        for high in self.highlights:
            del high
        del self.highlights
        self.pixmapimage = QtGui.QPixmap(item.imgPath).scaled(self.pixmapX, self.pixmapY)
        self.imageLabel.setPixmap(QtGui.QPixmap(self.pixmapimage))
