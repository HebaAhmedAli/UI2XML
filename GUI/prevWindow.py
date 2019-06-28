from PyQt5 import QtWidgets, QtGui, QtCore
import os
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
        errorMargin = 13
        for i in imageboxs:
            high = componentHighlight(self.activeImageWidget, i[2], i[3])
            high.move(i[0]+errorMargin, i[1]+errorMargin)
            self.highlights.append(high)
        self.activeImgverticalLayout.addWidget(self.activeImageWidget)




        # self.updateXMLTab()

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
