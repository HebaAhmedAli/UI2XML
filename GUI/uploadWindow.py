from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import  GUI.skelUploadWindow as  skelUploadWindow
from screeninfo import get_monitors

class uploadWindow(QDialog, skelUploadWindow.Ui_uploadWindow):
    def __init__(self):
        super(uploadWindow, self).__init__()
        self.setupUi(self)

    # Placement of the uploaded image
        self.screenW, self.screenH = self.getScreenDims()
        self.IsGrid = 1
        self.indexColumn = 0
        self.indexRow = 0
        self.maxRowSize = 7

        self.imageBox_W = (self.screenW - 440 - 7* self.maxRowSize)/self.maxRowSize - 20         #201
        if self.imageBox_W < 180:
            self.imageBox_W = 180
            self.maxRowSize = 7
        # print(self.imageBox_W)
        self.imageBox_H = int(self.imageBox_W *4/3)    #268
        self.horizontalLayouts = []
        self.numOfImages = 0
        self.images = []

        newLine = QHBoxLayout()
        self.horizontalLayouts.append(newLine)
        self.horizontalLayouts[0].setAlignment(Qt.AlignLeft)
        self.Layout.addLayout(self.horizontalLayouts[0])

        self.statusbarwindow = QStatusBar()
        self.statusbarwindow.setSizeGripEnabled(False)

        # self.lay = QVBoxLayout(self.centralwidget)
        # self.lay.addWidget(self.scrollarea)

        self.dockDesign.setMinimumWidth(350)
        # self.mainDialoge = createProjectDialog()
        # self.mainDialoge.show()
        # self.mainDialoge.started.connect(self.start_Pro)
        # self.actionRun.triggered.connect(self.convertFiles)

    def getScreenDims(self):
        monitor = get_monitors()
        monitor = str(monitor)
        startI = monitor.rfind('(', 0, len(monitor))
        midI = monitor.rfind('x', 0, len(monitor))
        endI = monitor.find('+', 0, len(monitor))
        monitorW = int(monitor[startI+1:midI], 10)
        monitorH = int(monitor[midI+1:endI], 10)
        return monitorW, monitorH

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
                # endI = filePath.rfind('.', 0, len(filePath))
                fileName = filePath[startI:]
                if(not self.matchFormat(filePath)):
                    continue
                self.GroupBox = QGroupBox()
                HLayoutCnt = len(self.horizontalLayouts)
                newimage = imageBox(self.numOfImages)
                newimage.deleteImage.deleted.connect(self.on_deleteButton_clicked)
                self.numOfImages = self.numOfImages + 1

                if (self.horizontalLayouts[HLayoutCnt -1]).count() >= self.maxRowSize  :
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
        designModes = ("Hand Darwing", "Screenshot", "PSD File")
        extensions = {"imgExten": ["jpg", "jpeg", "png"],"psdExten":["psd"]}
        windDialog = QWidget()
        if( self.designMode == designModes[0] or self.designMode == designModes[1]):
            if( not (fileExten in extensions["imgExten"])):
                QMessageBox.critical(windDialog, "Format Error",str(filePath) + " has inappropriate Image format." )
                print("Inappropriate Image format")
                return False
        if( self.designMode == designModes[2]):
            if(not (fileExten in extensions["psdExten"])):
                QMessageBox.critical(windDialog, "Format Error",str(filePath) + " has inappropriate PSD format." )
                print("Inappropriate PSD format")
                return False
        return True

    def convertFiles(self):
        names=[]
        for image in self.images:
            name = str(image.imageNameLine.text())
            endI = name.rfind('.', 0, len(name))
            if (not '.' in name):
                windDialog = QWidget()
                QMessageBox.critical(windDialog, "File name Error", name + " File name or extension not correct" )
                print("No file marked as Main")
                return
            imgExten = ["jpg", "jpeg", "png"]
            if(not name[endI+1:].lower() in imgExten):
                windDialog = QWidget()
                QMessageBox.critical(windDialog, "File extension Error", name + " File extension not correct" )
                print("No file marked as Main")
                return
            names.append(name[:endI])
        if(not "main" in names):
            windDialog = QWidget()
            QMessageBox.critical(windDialog, "Missing main", "Choose one of the files as your Main Activity" )
            print("No file marked as Main")
            return
        
        # Creating Input folder for recognition
        dir = self.projectDir + "/" + self.projectName
        print("Directory of project" + dir )
        if(not os.path.exists(dir)):
            os.mkdir(dir)
        # TODO: Handle PSD
        for image in self.images:
            readImage = Image.open(image.srcPath)
            imageName = str(image.imageNameLine.text())
            endI = imageName.rfind('.', 0, len(imageName))
            exten = imageName[endI:]
            name = imageName[:endI]
            if(image.hasActionBar.isChecked()):
                name = name + "A"
            else:
                name = name + "N"
            if(image.staticList.isChecked()):
                name = name + "S"
            else:
                name = name + "D"
            readImage.save(self.projectDir + "/" + self.projectName + "/" + name + exten)
            # image.setParent(None)
        # TODO: Call the recognition for this directory
        for image in self.images:        
            image.deleteImage.click()
        for horizontalLayout in self.horizontalLayouts:
            horizontalLayout.setParent(None)
            del horizontalLayout
        del self.horizontalLayouts
        self.scrollarea.setParent(None)
        del self.scrollarea
        self.dockDesign.setParent(None)
        del self.dockDesign
        self.setAcceptDrops(False)
        self.lay.addWidget(previewWindow(self))



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
        self.projectName = creationList[0]
        self.packageName = creationList[1]
        self.designMode =  creationList[2]
        self.projectDir =  creationList[3]
        self.mainDialoge.close()
