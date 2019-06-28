from PyQt5 import QtWidgets, QtGui, QtCore
import os
import imagesize 
from GUI.skelPrevWindow import  previewWindowSkel
#from GUI.tabs import xmlTab
import GUI.activityListItem as activityListItem
from GUI.componentHighlight import componentHighlight
import GUI.utils as utils
import Constants

class previewWindow(QtWidgets.QWidget, previewWindowSkel):
    def __init__(self):
        super(previewWindow, self).__init__()
        self.setupUi(self)
        self.pixmapX = 300
        self.pixmapY = 600
        # The backend output
        imgsOutputInfo = {"mainND.jpg": ([[19, 19, 27, 27], [190, 135, 145, 124], [43, 311, 479, 63], [43, 405, 478, 64]],
                ['ImageButton_0_0_0', 'ImageView_0_1_0', 'EditText_0_2_0', 'EditText_0_3_0'],
                ['ImageButton', 'ImageView', 'EditText', 'EditText'],
                ["activity_twitter.xml", "activity_twitter1.xml"]),
                "kolND.jpg": ([[19, 19, 27, 27], [190, 135, 145, 124], [43, 311, 479, 63], [43, 405, 478, 64]],
                ['ImageButton_0_0_0', 'ImageView_0_1_0', 'EditText_0_2_0', 'EditText_0_3_0'],
                ['ImageButton', 'ImageView', 'EditText', 'EditText'],
                ["activity_twitter.xml", "activity_twitter1.xml"])
                }
        
        projDir = Constants.imagesPath
        mainActivityName = "main"
        for imgName in imgsOutputInfo:
            endI = imgName.rfind('.', 0, len(imgName))
            if(mainActivityName==imgName[:endI-2]):
                mainActivityName = imgName
            imgDir = projDir+"/"+imgName
            imgName = imgName[:endI-2]+imgName[endI:]
            activityHLayout = activityListItem.activityListItem(imgDir, imgName)
            self.activitysHLayouts.append(activityHLayout)
            self.verticalLayout.addLayout(activityHLayout)

        mainActivityDir = projDir+"/"+mainActivityName
        self.activeImageWidget = QtWidgets.QWidget()
        activeImageLayout = QtWidgets.QVBoxLayout(self.activeImageWidget)
        imageLabel = QtWidgets.QLabel(self.activeImgVerticalLayoutWidget)
        pixmapimage = QtGui.QPixmap(mainActivityDir).scaled(self.pixmapX, self.pixmapY)
        imageLabel.setPixmap(QtGui.QPixmap(pixmapimage))
        activeImageLayout.addWidget(imageLabel)
        imageboxs = imgsOutputInfo[mainActivityName][0]
        self.highlights = []
        imgW, imgH = imagesize.get(mainActivityDir)
        print(imgW, imgH)
        for compBox in imageboxs:
            scaledCompBox =  self.calculateScaledBox(compBox, imgW, imgH)
            errorMargin = 10
            high = componentHighlight(self.activeImageWidget, scaledCompBox[2]+errorMargin, scaledCompBox[3]+errorMargin)
            high.move(scaledCompBox[0]+errorMargin, scaledCompBox[1]+errorMargin)
            self.highlights.append(high)
            print(compBox)
        self.activeImgverticalLayout.addWidget(self.activeImageWidget)

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

