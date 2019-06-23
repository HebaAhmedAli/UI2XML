from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os
from imageBox import imageBox
from createProjectDialog import createProjectDialog
import skelMainscreen

class mainScreen (QMainWindow,  skelMainscreen.Ui_mainWindow):
    def __init__(self, width, height):
        super(mainScreen, self).__init__()
        self.state = "INS_PIC"
        self.setupUi(self)
        # Placement of the uploaded image
        self.screenW = width
        self.screenH = height
        self.IsGrid = 1
        self.indexColumn = 0
        self.indexRow = 0
        self.maxRowSize = 7

        self.imageBox_W = (width - 440 - 7* self.maxRowSize)/self.maxRowSize - 20         #201
        if self.imageBox_W < 180:
            self.imageBox_W = 180
            self.maxRowSize = 7
        # print(self.imageBox_W)
        self.imageBox_H = int(self.imageBox_W *4/3)    #268
        self.gridData = QWidget()
        self.Layout = QVBoxLayout()
        self.Layout.setAlignment(Qt.AlignTop)
        self.horizontalLayouts = []
        self.gridData.setLayout(self.Layout)
        self.numOfImages = 0
        self.projectDetails=[]
        self.images = []

        # Upload Area scrollable
        self.scrollarea = QScrollArea()
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollarea.setWidget(self.gridData)

        newLine = QHBoxLayout()
        self.horizontalLayouts.append(newLine)
        self.horizontalLayouts[0].setAlignment(Qt.AlignLeft)
        self.Layout.addLayout(self.horizontalLayouts[0])
        #self.horizontalLayouts[self.indexRow].setAlignment(Qt.AlignLeft)

        self.statusbarwindow = QStatusBar()
        self.statusbarwindow.setSizeGripEnabled(False)

        lay = QVBoxLayout(self.centralwidget)
        lay.addWidget(self.scrollarea)

        # self.dockPictuers.setMinimumWidth(350)
        self.dockDesign.setMinimumWidth(350)
        self.mainDialoge = createProjectDialog()
        self.mainDialoge.show()
        self.mainDialoge.started.connect(self.start_Pro)
        # text = open('activity_twitter.xml').read()
        # self.textBrowser.setPlainText(text)
        # path = "../data"
        # model = QFileSystemModel()
        # model.setRootPath((QDir.rootPath()))
        # self.treeView.setModel(model)
        # self.treeView.setRootIndex(model.index(path))

    def setDirectory(self, url):
        self.directory= url

    def newImageLabel (self, image, label):

        groupBox= QGroupBox()
        layout = QVBoxLayout()
        horizontalLay = QHBoxLayout()
        self.imageLabel = QLabel()
        self.text = QLabel()
        self.checkbox = QCheckBox("Action Bar")
        self.button = QPushButton("Delete me!")
        pixmapimage = QPixmap(image).scaled(201, 268)
        self.imageLabel.setPixmap(QPixmap(pixmapimage))

        self.text.setText(label)

        self.text.setAlignment(Qt.AlignHCenter)

        self.imageLabel.setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.imageLabel)
        layout.addWidget(self.text)
        horizontalLay.addWidget(self.checkbox)
        horizontalLay.addWidget(self.button)
        layout.addLayout(horizontalLay)
        groupBox.setLayout(layout)
        return groupBox

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.pictureDropped( links)
        else:
            event.ignore()

    def pictureDropped(self, paths):
        for filePath in paths:
            if os.path.exists(filePath):
                startI = filePath.rfind('/', 0, len(filePath)) + 1
                endI = filePath.rfind('.', 0, len(filePath))
                fileName = filePath[startI: endI]
                if(not self.matchFormat(filePath)):
                    continue
                self.GroupBox = QGroupBox()
                HLayoutCnt = len(self.horizontalLayouts)
                newimage = imageBox(self.numOfImages)
                newimage.deleteImage.deleted.connect(self.on_deleteButton_clicked)
                self.numOfImages = self.numOfImages + 1

                if (self.horizontalLayouts[HLayoutCnt -1]).count() < self.maxRowSize  :
                    imagebox = newimage.setImage(filePath, fileName, self.indexRow, self.indexColumn, self.imageBox_W,
                                                 self.imageBox_H, self.IsGrid)
                    self.images.append(newimage)
                    self.horizontalLayouts[self.indexRow].addWidget(imagebox)

                    self.indexColumn = self.indexColumn + 1
                else:
                    self.indexColumn = 0
                    self.indexRow = self.indexRow + 1

                    newLine = QHBoxLayout()
                    self.horizontalLayouts.append(newLine)
                    self.horizontalLayouts[self.indexRow].setAlignment(Qt.AlignLeft)
                    self.Layout.addLayout(self.horizontalLayouts[self.indexRow])
                    imagebox = newimage.setImage(filePath, fileName, self.indexRow, self.indexColumn, self.imageBox_W,
                                                 self.imageBox_H, self.IsGrid)
                    self.images.append(newimage)
                    self.horizontalLayouts[self.indexRow].addWidget(imagebox)
                    self.indexColumn = self.indexColumn +1

    def setImageDim (self, width, length):
        self.imageBox_W = width
        self.imageBox_W = length

    def chanageGridSize(self, noImgPerRow, imgWidth=0, imgHight = 0):
        maxRowSize = noImgPerRow
        imageBox_W = (self.screenW - 440 - 7 * noImgPerRow) / noImgPerRow - 20  # 201
        if imageBox_W < 180:
            imageBox_W = 180
            maxRowSize = 7
        # print(imageBox_W)
        imageBox_H = int(imageBox_W * 4 / 3)  # 268

        indexRow = 0
        indexCol = 0
        newIndexRow = 0
        newIndexCol = 0
        newHorLayouts = []
        newLine = QHBoxLayout()
        newHorLayouts.append(newLine)
        newHorLayouts[0].setAlignment(Qt.AlignLeft)

        for i in self.images:
            i.delimg()

        for i in range (0, self.numOfImages):
            if i / (indexRow +1) >= self.maxRowSize:
                indexRow = indexRow + 1
                indexCol = 0
            imagebox = self.images[i].resizeImg(i,  newIndexRow, newIndexCol, imageBox_W, imageBox_H)
            if i / (newIndexRow +1) >= maxRowSize :
                newIndexRow = newIndexRow + 1
                newIndexCol = 0
                newLine = QHBoxLayout()
                newHorLayouts.append(newLine)
                newHorLayouts[newIndexRow].setAlignment(Qt.AlignLeft)
                #self.Layout.addLayout(newHorLayouts[newIndexRow])

            #self.horizontalLayouts[indexRow].setParent(None)
            newHorLayouts[newIndexRow].addWidget(imagebox)
            indexCol = indexCol + 1
            newIndexCol = newIndexCol + 1

        self.horizontalLayouts = newHorLayouts
        for i in range (0, len(self.horizontalLayouts)):
            self.Layout.addLayout(self.horizontalLayouts[i])

        self.maxRowSize = maxRowSize
        self.imageBox_W = imageBox_W
        self.imageBox_H = imageBox_H
        self.indexColumn = newIndexCol
        self.indexRow = newIndexRow

    def matchFormat(self, filePath):
        endIdx = filePath.rfind('.', 0, len(filePath)) + 1
        fileExten = filePath[endIdx:]
        fileExten = fileExten.lower()
        print(fileExten)
        designType = self.projectDetails[2]
        designModes = ("Hand Darwing", "Screenshot", "PSD File")
        extensions = {"imgExten": ["jpg", "jpeg", "png"],"psdExten":["psd"]}
        w = QWidget()
        if(designType == designModes[0] or designType == designModes[1]):
            if( not (fileExten in extensions["imgExten"])):
                QMessageBox.critical(w, "Format Error",str(filePath) + " has inappropriate Image format." )
                print("Inappropriate Image format")
                return False
        if(designType == designModes[2]):
            if(not (fileExten in extensions["psdExten"])):
                QMessageBox.critical(w, "Format Error",str(filePath) + " has inappropriate PSD format." )
                print("Inappropriate PSD format")
                return False
        return True


    @pyqtSlot(int)
    def on_deleteButton_clicked(self, index):
        print("Deleting from parent")
        self.images[index].delimg()
        del self.images[index]
        self.numOfImages = self.numOfImages -1
        # print(len(self.images))
        self.chanageGridSize(self.maxRowSize)

    @pyqtSlot(list)    
    def start_Pro(self,creationList):
        print(creationList)
        self.projectDetails = creationList
        self.mainDialoge.close()
