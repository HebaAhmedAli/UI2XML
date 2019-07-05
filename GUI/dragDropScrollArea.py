import sys
sys.path.append('../')
from PyQt5 import QtCore, QtGui, QtWidgets
import GUI.utils as utils
from GUI.imageBox import imageBox
import Constants
import os
import GUI.cropImage as cropImage

class dragDropScroll(QtWidgets.QScrollArea):
    donePopulating = QtCore.pyqtSignal
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        self.horizontalLayouts = []
        self.imageBoxes = []
        self.numOfImages = 0
        self.maxRowSize = 4

        self.imageBox_W = (Constants.MONITOR_WIDTH - 30 * self.maxRowSize)/self.maxRowSize - 20         #201
        if self.imageBox_W < 180:
            self.imageBox_W = 180
            self.maxRowSize = 4
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
        print(fileExten,Constants.designMode)
        if( Constants.designMode == Constants.DESIGN_MODES[0] or Constants.designMode == Constants.DESIGN_MODES[1]):
            if( not (fileExten in Constants.IMG_EXTN)):
                utils.alertUser("Format Error", str(filePath) + " has inappropriate Image format.")
                return False
        if( Constants.designMode == Constants.DESIGN_MODES[2]):
            if(not (fileExten == "psd")):
                utils.alertUser("Format Error", str(filePath) + " has inappropriate PSD format.")
                return False
        return True

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
            newimage = imageBox(self.numOfImages, self.imageBox_W, self.imageBox_H)
            newimage.deleteImage.deleted.connect(self.on_deleteButton_clicked)
            newimage.cropImage.crop.connect(self.on_cropButton_clicked)
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
        imageBox_W = (Constants.MONITOR_WIDTH - 7* self.maxRowSize)/self.maxRowSize - 20  # 201
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
            if (idx +1) / (indexRow +1) >= self.maxRowSize:
                indexRow = indexRow + 1
                indexCol = 0
            imagebox = self.imageBoxes[idx].resizeImg(idx,  newIndexRow, newIndexCol, imageBox_W, imageBox_H)
            if (idx +1) / (newIndexRow +1) >= maxRowSize :
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

    def on_cropButton_clicked(self, index):
        self.cropDialog = cropImage.cropImageDialog(self.imageBoxes[index].srcPath, index)
        self.cropDialog.show()
        self.cropDialog.activateWindow()
        self.chanageGridSize(self.maxRowSize)

    def AddImages(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        paths, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "Select images to add", "main",
                                                          "All Files (*);;JPG (*.JPG);;PNG (*.PNG)",
                                                          options=options)
        if paths:
            self.pictureDropped(paths)

    def ChangeGrid4(self):
        self.chanageGridSize(4)

    def ChangeGrid6(self):
        self.chanageGridSize(6)

    def ChangeGrid8(self):
        self.chanageGridSize(8)
