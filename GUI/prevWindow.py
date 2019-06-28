from PyQt5 import QtWidgets, QtGui, QtCore
import os
import imagesize 
from GUI.skelPrevWindow import  previewWindowSkel
#from GUI.tabs import xmlTab
from GUI.componentHighlight import componentHighlight
import GUI.utils as utils

class previewWindow(QtWidgets.QWidget, previewWindowSkel):
    def __init__(self):
        super(previewWindow, self).__init__()
        self.setupUi(self)
        
    #     # For testing
    #     self.index = 0
        self.highlights = []
    #     self.mp = {'main.jpg':
    #                    ([[19, 19, 27, 27], [190, 135, 145, 124], [43, 311, 479, 63], [43, 405, 478, 64],
    #                      [81, 557, 384, 46], [170, 634, 211, 31], [116, 844, 329, 27]],
    #                     ['ImageButton_0_0_0', 'ImageView_0_1_0', 'EditText_0_2_0', 'EditText_0_3_0', 'Button_0_4_0',
    #                      'Button_0_5_0', 'Button_0_6_0'],
    #                     ['ImageButton', 'ImageView', 'EditText', 'EditText', 'Button', 'Button', 'Button'],
    #                     ['activity_nasa.xml'])}

    #     # self.projDir = mainWindow.projectDir + "/" + mainWindow.projectName
    #     self.imgsNames = []
    #     #self.imgsNames = self.addImageTabs()
    #     # imageDir = self.projDir + "/main.png"
        #self.addActiveImage(imageDir)
        self.activeImageWidget = QtWidgets.QWidget()
        self.pixmapX = 300
        self.pixmapY = 600
        qvbox = QtWidgets.QVBoxLayout(self.activeImageWidget)
        imageLabel = QtWidgets.QLabel(self.activeImgVerticalLayoutWidget)
        imgDir = "/home/fatema/PycharmProjects/UI2XML/GUI/main.jpg"
        
        pixmapimage = QtGui.QPixmap(imgDir).scaled(self.pixmapX, self.pixmapY)
        imageLabel.setPixmap(QtGui.QPixmap(pixmapimage))
        # imageLabel.setAlignment(Qt.AlignHCenter)
        qvbox.addWidget(imageLabel)
        imageboxs = [[19, 19, 27, 27], [190, 135, 145, 124], [43, 311, 479, 63], [43, 405, 478, 64],
                     [81, 557, 384, 46], [170, 634, 211, 31], [116, 844, 329, 27]]
        imgW, imgH = imagesize.get(imgDir)
        print(imgW, imgH)
        for compBox in imageboxs:
            scaledCompBox =  self.calculateScaledBox(compBox, imgW, imgH)
            errorMargin = 10
            high = componentHighlight(self.activeImageWidget, scaledCompBox[2]+errorMargin, scaledCompBox[3]+errorMargin)
            high.move(scaledCompBox[0]+errorMargin, scaledCompBox[1]+errorMargin)
            self.highlights.append(high)
            print(compBox)
        self.activeImgverticalLayout.addWidget(self.activeImageWidget)
        # self.updateXMLTab()

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


    def addImageTabs(self):
        imgsDir = self.projDir
        for imgpath in os.listdir(imgsDir):
            endI = imgpath.rfind('.', 0, len(imgpath)) + 1
            imgName = imgpath[:endI - 3]
            imgExten = imgpath[endI:]
            imgExten = imgExten.lower()
            imgExtens = ["jpg", "jpeg", "png"]
            if len(imgExten) == len(imgpath):
                continue
            if (not (imgExten in imgExtens)):
                windDialog = QtWidgets.QWidget()
                QtWidgets.QMessageBox.critical(windDialog, "Format Error", str(imgpath) + " has inappropriate Image format.")
                print("Inappropriate Image format")
                continue
            imgName = imgName + "." + imgExten
            if (not self.mp[imgName]):
                continue
            self.imgObj = self.mp[imgName]
            self.imgBoxes = self.imgObj[0]
            self.boxesIDs = self.imgObj[1]
            self.boxesPred = self.imgObj[2]
            self.xmlFiles = self.imgObj[3]
            # self.ptrs = self.imgObj[4]
            # self.imagetabs.addTab(imageTab(imgsDir+"/"+imgpath), imgName)
            self.imgsNames.append(imgName)

    def updateXMLTab(self):
        xmlDir = self.projDir + "/layouts"
        '''for xmlFile in self.xmlFiles:
            tab = xmlTab()
            text = open(str(xmlDir + "/" + xmlFile)).read()
            tab.textBrowser.setPlainText(text)
            self.xmlTabs.addTab(tab, xmlFile[:-4])
            '''
