from PyQt5 import QtCore, QtGui, QtWidgets
from GUI.utils import alertUser
from GUI.imageBox import imageBox
import screeninfo
import os

class dragDropScroll(QtWidgets.QScrollArea):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        self.screenW, self.screenH = self.getScreenDims()
        self.horizontalLayouts = []
        self.imageBoxes = []
        self.numOfImages = 0
        self.maxRowSize = 7

        self.imageBox_W = (self.screenW - 440 - 7* self.maxRowSize)/self.maxRowSize - 20         #201
        if self.imageBox_W < 180:
            self.imageBox_W = 180
            self.maxRowSize = 7
        self.imageBox_H = int(self.imageBox_W *4/3)    #268        

        # Placement of the uploaded image
        self.IsGrid = 1
        self.indexColumn = 0
        self.indexRow = 0
        self.createImgsArea()

    def createImgsArea(self):
        self.gridData = QtWidgets.QWidget()
        self.imgsLayout = QtWidgets.QVBoxLayout()
        self.imgsLayout.setAlignment(QtCore.Qt.AlignTop)
        self.gridData.setLayout(self.imgsLayout)

        firstHLay = QtWidgets.QHBoxLayout()
        self.horizontalLayouts.append(firstHLay)
        self.horizontalLayouts[0].setAlignment(QtCore.Qt.AlignLeft)        
        self.imgsLayout.addLayout(self.horizontalLayouts[0])
        

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.pictureDropped(links)
        else:
            event.ignore()
    
    def matchFormat(self, filePath):
        endIdx = filePath.rfind('.', 0, len(filePath)) + 1
        fileExten = filePath[endIdx:]
        fileExten = fileExten.lower()
        designModes = ("Hand Darwing", "Screenshot", "PSD File")
        extensions = {"imgExten": ["jpg", "jpeg", "png"],"psdExten":["psd"]}

        if( self.designMode == designModes[0] or self.designMode == designModes[1]):
            if( not (fileExten in extensions["imgExten"])):
                alertUser("Format Error", str(filePath) + " has inappropriate Image format.")
                return False
        if( self.designMode == designModes[2]):
            if(not (fileExten in extensions["psdExten"])):
                alertUser("Format Error", str(filePath) + " has inappropriate PSD format.")
                return False
        return True


    def getScreenDims(self):
        monitor = screeninfo.get_monitors()
        monitor = str(monitor)
        startI = monitor.rfind('(', 0, len(monitor))
        midI = monitor.rfind('x', 0, len(monitor))
        endI = monitor.find('+', 0, len(monitor))
        monitorW = int(monitor[startI+1:midI], 10)
        monitorH = int(monitor[midI+1:endI], 10)
        return monitorW, monitorH

    def pictureDropped(self, paths):
        for filePath in paths:
            if not os.path.exists(filePath):
                alertUser("File Error", str(filePath) + " path doesn't exist.")
                continue

            startI = filePath.rfind('/', 0, len(filePath)) + 1
            fileName = filePath[startI:]
            # if(not self.matchFormat(filePath)):
            #     continue

            self.GroupBox = QtWidgets.QGroupBox()
            HLayoutCnt = len(self.horizontalLayouts)
            newimage = imageBox(self.numOfImages)
            # newimage.deleteImage.deleted.connect(self.on_deleteButton_clicked)
            self.numOfImages = self.numOfImages + 1

            if (self.horizontalLayouts[HLayoutCnt -1]).count() >= self.maxRowSize  :
                self.indexColumn = 0
                self.indexRow = self.indexRow + 1

                newLine = QtWidgets.QHBoxLayout()
                self.horizontalLayouts.append(newLine)
                self.horizontalLayouts[self.indexRow].setAlignment(QtCore.Qt.AlignLeft)
                self.imgsLayout.addLayout(self.horizontalLayouts[self.indexRow])

            imagebox = newimage.setImage(filePath, fileName, self.indexRow, self.indexColumn, self.imageBox_W,
                                            self.imageBox_H, self.IsGrid)
            self.imageBoxes.append(newimage)
            self.horizontalLayouts[self.indexRow].addWidget(imagebox)
            self.indexColumn = self.indexColumn +1

