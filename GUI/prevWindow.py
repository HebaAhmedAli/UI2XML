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
        # imgsOutputInfo = Constants.mapToGui
        imgsOutputInfo = {"mainND.jpg": ([[19, 19, 27, 27], [190, 135, 145, 124], [43, 311, 479, 63], [43, 405, 478, 64],
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
        for imgName in imgsOutputInfo:
            endI = imgName.rfind('.', 0, len(imgName))
            if(mainActivityName==imgName[:endI-2]):
                mainActivityName = imgName
            imgDir = projDir+"/"+imgName
            self.userCorrection.update(imgName=[])
            imgName = imgName[:endI-2]+imgName[endI:]
            # activityHLayout = QtWidgets.QHBoxLayout()
            self.activitiesList.add_item(imgDir, imgName)
            # activityHLayout.addWidget(activityItem)
            # activityItem.activate.connect(self.onViewBtnClicked)
            # activityHLayout.setAlignment(QtCore.Qt.AlignLeft)
            # self.activitysHLayouts.append(activityItem.allHLayout)
            # self.verticalLayout.addWidget(activityItem.allHLayout)
            self.activitiesList.activated.connect(self.item_click)


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

    @QtCore.pyqtSlot(str)
    def item_click(self, i):
        print("imgPath")
        # mainActivityDir = Constants.imagesPath+"/"+mainActivityName
        # self.activeImageWidget = QtWidgets.QWidget()
        # activeImageLayout = QtWidgets.QVBoxLayout(self.activeImageWidget)
        # imageLabel = QtWidgets.QLabel(self.activeImgVerticalLayoutWidget)
        # pixmapimage = QtGui.QPixmap(mainActivityDir).scaled(self.pixmapX, self.pixmapY)
        # imageLabel.setPixmap(QtGui.QPixmap(pixmapimage))
        # activeImageLayout.addWidget(imageLabel)
        # compBoxes = imgsOutputInfo[mainActivityName][0]
        # compIDs = imgsOutputInfo[mainActivityName][1]
        # compPreds = imgsOutputInfo[mainActivityName][2]
        # self.highlights = []
        # imgW, imgH = imagesize.get(mainActivityDir)
        # for idx in range(0,len(compBoxes)):
        #     compBox =compBoxes[idx]
        #     compId = compIDs[idx]
        #     compPred = compPreds[idx]
        #     scaledCompBox =  self.calculateScaledBox(compBox, imgW, imgH)
        #     high = componentHighlight(self.activeImageWidget, scaledCompBox, compBox, compId, compPred)
        #     self.highlights.append(high)
        # self.activeImgverticalLayout.addWidget(self.activeImageWidget)
    

    def updateXMLTab(self, xmlFiles):
        xmlDir = Constants.imagesPath + "/output/main/res/layout"
        for xmlFile in xmlFiles:
            tab = xmlTab()
            text=open(str(xmlDir+"/"+xmlFile)).read()
            tab.textBrowser.setPlainText(text)
            self.xmlTabs.addTab(tab, xmlFile[:-4])