import sys
sys.path.append('../')
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.skelUploadWindow as  skelUploadWindow
import GUI.utils as utils
import Constants
import os
import cv2

class uploadWindow(QWidget, skelUploadWindow.Ui_uploadWindow):

    def __init__(self):
        super(uploadWindow, self).__init__()       
        self.setupUi(self)


    def populateProjDir(self):
        names=[]
        for image in self.scrollarea.imageBoxes:
            name = str(image.imageNameLine.text())
            endI = name.rfind('.', 0, len(name))
            if (not '.' in name or not name[endI+1:].lower() in Constants.IMG_EXTN):
                utils.alertUser("File name Error", name + " File name or extension not correct")
                return
            names.append(name[:endI])
        if(not "main" in names):
            utils.alertUser("Missing main", "Choose one of the files as your Main Activity")
            return
        
        # Creating Input folder for recognition
        fullProjDir = Constants.imagesPath
        print("Directory of project" + fullProjDir )
        if(not os.path.exists(fullProjDir)):
            os.mkdir(fullProjDir)
        # TODO: Handle PSD
        for image in self.scrollarea.imageBoxes:
            readImage = cv2.imread(image.srcPath)
            imageName = str(image.imageNameLine.text())
            endI = imageName.rfind('.', 0, len(imageName))
            exten = imageName[endI:]
            name = imageName[:endI]
            name = name.lower()
            if(image.hasActionBar.isChecked()):
                name = name + "A"
            else:
                name = name + "N"
            if(image.staticList.isChecked()):
                name = name + "S"
            else:
                name = name + "D"
            cv2.imwrite(fullProjDir + "/" + name + exten,readImage)
        self.removeUploadWid()

    def removeUploadWid(self):
        for image in self.scrollarea.imageBoxes:        
            image.deleteImage.click()
        for horizontalLayout in self.scrollarea.horizontalLayouts:
            horizontalLayout.setParent(None)
            del horizontalLayout
        del self.scrollarea.horizontalLayouts
        del self.scrollarea.imgsHLayoutsContainer
        self.scrollarea.setAcceptDrops(False)
        self.scrollarea.setParent(None)
        del self.scrollarea
        self.dockDesign.setParent(None)
        del self.dockDesign