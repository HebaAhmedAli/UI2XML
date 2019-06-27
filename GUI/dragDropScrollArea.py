from PyQt5 import QtCore, QtGui, QtWidgets
import GUI.utils as utils
from GUI.imageBox import imageBox
import screeninfo
import os

class dragDropScroll(QtWidgets.QScrollArea):
    donePopulating = QtCore.pyqtSignal
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
        self.imgsHLayoutsContainer = QtWidgets.QVBoxLayout()
        self.imgsHLayoutsContainer.setAlignment(QtCore.Qt.AlignTop)
        self.gridData.setLayout(self.imgsHLayoutsContainer)

        firstHLay = QtWidgets.QHBoxLayout()
        self.horizontalLayouts.append(firstHLay)
        self.horizontalLayouts[0].setAlignment(QtCore.Qt.AlignLeft)        
        self.imgsHLayoutsContainer.addLayout(self.horizontalLayouts[0])
        

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
        designModes = ("Hand Drawing", "Screenshots", "PSD File")
        extensions = {"imgExten": ["jpg", "jpeg", "png"],"psdExten":["psd"]}
        if( utils.designMode == designModes[0] or utils.designMode == designModes[1]):
            if( not (fileExten in extensions["imgExten"])):
                utils.alertUser("Format Error", str(filePath) + " has inappropriate Image format.")
                return False
        if( utils.designMode == designModes[2]):
            if(not (fileExten in extensions["psdExten"])):
                utils.alertUser("Format Error", str(filePath) + " has inappropriate PSD format.")
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
                utils.alertUser("File Error", str(filePath) + " path doesn't exist.")
                continue

            startI = filePath.rfind('/', 0, len(filePath)) + 1
            fileName = filePath[startI:]
            if(not self.matchFormat(filePath)):
                continue

            self.GroupBox = QtWidgets.QGroupBox()
            HLayoutCnt = len(self.horizontalLayouts)
            newimage = imageBox(self.numOfImages)
            newimage.deleteImage.deleted.connect(self.on_deleteButton_clicked)
            self.numOfImages = self.numOfImages + 1

            if (self.horizontalLayouts[HLayoutCnt -1]).count() >= self.maxRowSize  :
                self.indexColumn = 0
                self.indexRow = self.indexRow + 1

                newLine = QtWidgets.QHBoxLayout()
                self.horizontalLayouts.append(newLine)
                self.horizontalLayouts[self.indexRow].setAlignment(QtCore.Qt.AlignLeft)
                self.imgsHLayoutsContainer.addLayout(self.horizontalLayouts[self.indexRow])

            imagebox = newimage.setImage(filePath, fileName, self.indexRow, self.indexColumn, self.imageBox_W,
                                            self.imageBox_H, self.IsGrid)
            self.imageBoxes.append(newimage)
            self.horizontalLayouts[self.indexRow].addWidget(imagebox)
            self.indexColumn = self.indexColumn + 1

    def chanageGridSize(self, noImgPerRow, imgWidth=0, imgHight = 0):
        maxRowSize = noImgPerRow
        imageBox_W = (self.screenW - 440 - 7 * noImgPerRow) / noImgPerRow - 20  # 201
        if imageBox_W < 180:
            imageBox_W = 180
            maxRowSize = 7
        imageBox_H = int(imageBox_W * 4 / 3)  # 268

        indexRow = 0
        indexCol = 0
        newIndexRow = 0
        newIndexCol = 0
        newHorLayouts = []
        newLine = QtWidgets.QHBoxLayout()
        newHorLayouts.append(newLine)
        newHorLayouts[0].setAlignment(QtCore.Qt.AlignLeft)

        for imagebox in self.imageBoxes:
            imagebox.groupBox.setParent(None)

        for idx in range (0, self.numOfImages):
            if idx / (indexRow +1) >= self.maxRowSize:
                indexRow = indexRow + 1
                indexCol = 0
            imagebox = self.imageBoxes[idx].resizeImg(idx,  newIndexRow, newIndexCol, imageBox_W, imageBox_H)
            if idx / (newIndexRow +1) >= maxRowSize :
                newIndexRow = newIndexRow + 1
                newIndexCol = 0
                newLine = QtWidgets.QHBoxLayout()
                newHorLayouts.append(newLine)
                newHorLayouts[newIndexRow].setAlignment(QtCore.Qt.AlignLeft)

            newHorLayouts[newIndexRow].addWidget(imagebox)
            indexCol = indexCol + 1
            newIndexCol = newIndexCol + 1

        self.horizontalLayouts = newHorLayouts
        for idx in range (0, len(self.horizontalLayouts)):
            self.imgsHLayoutsContainer.addLayout(self.horizontalLayouts[idx])

        self.maxRowSize = maxRowSize
        self.imageBox_W = imageBox_W
        self.imageBox_H = imageBox_H
        self.indexColumn = newIndexCol
        self.indexRow = newIndexRow

    def on_deleteButton_clicked(self, index):
        print("Deleting Image num " + str(index))
        self.imageBoxes[index].groupBox.setParent(None)
        del self.imageBoxes[index]
        self.numOfImages = self.numOfImages -1
        self.chanageGridSize(self.maxRowSize)