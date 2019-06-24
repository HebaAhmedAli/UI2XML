import sys
sys.path.append('../')
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os
import skelPreviewWind 
from tabs import xmlTab
import Constants

class previewWindow(QDialog, skelPreviewWind.previewWindowSkel):
    def __init__(self, mainWindow):
        super(previewWindow, self).__init__(mainWindow)
        self.setupUi(self)
        # For testing
        '''
        self.mp = {"main.png": ([[19, 19, 27, 27], [190, 135, 145, 124], [43, 311, 479, 63], [43, 405, 478, 64]],
                ['ImageButton_0_0_0', 'ImageView_0_1_0', 'EditText_0_2_0', 'EditText_0_3_0'],
                ['ImageButton', 'ImageView', 'EditText', 'EditText'],
                ["activity_twitter.xml", "activity_twitter1.xml"])}
        '''
        self.mp = Constants.mapToGui
        print(self.mp)
        self.projDir = mainWindow.projectDir + "/" + mainWindow.projectName
        self.imgsNames = []
        self.imgsNames = self.addImageTabs()
        self.updateXMLTab()

    def addImageTabs(self):
        imgsDir = self.projDir
        for imgpath in os.listdir(imgsDir):
            endI = imgpath.rfind('.', 0, len(imgpath)) + 1
            imgName = imgpath[:endI-3]
            imgExten = imgpath[endI:]
            imgExten = imgExten.lower()
            imgExtens = ["jpg", "jpeg", "png"]
            if len(imgExten) == len(imgpath) :
                continue
            if( not (imgExten in imgExtens)):
                windDialog = QWidget()
                QMessageBox.critical(windDialog, "Format Error",str(imgpath) + " has inappropriate Image format." )
                print("Inappropriate Image format")
                continue
            imgName = imgName+"."+imgExten
            if(not self.mp[imgName]):
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
        for xmlFile in self.xmlFiles:
            tab = xmlTab()
            text=open(str(xmlDir+"/"+xmlFile)).read()
            tab.textBrowser.setPlainText(text)
            self.xmlTabs.addTab(tab, xmlFile[:-4])