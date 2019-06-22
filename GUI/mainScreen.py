from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os
from imageBox import imageBox
from createProjectDialog import createProjectDialog
import skeleton

class mainScreen (QMainWindow,  skeleton.Ui_mainWindow):

    def __init__(self):
        super(mainScreen, self).__init__()
        self.setupUi(self)
        # Placement of the uploaded image
        self.indexColumn = 0
        self.indexRow = 0
        self.maxRowSize = 1

        self.gridData = QWidget()
        self.Layout = QVBoxLayout()
        self.Layout.setAlignment(Qt.AlignTop)
        self.horizontalLayouts = []
        self.gridData.setLayout(self.Layout)
        self.numOfImages = 0
        self.projectDetails=[]

        # Upload Area scrollable
        self.scrollarea = QScrollArea()
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollarea.setWidget(self.gridData)

        newLine = QHBoxLayout()
        self.horizontalLayouts.append(newLine)
        self.Layout.addLayout(self.horizontalLayouts[0])
        self.horizontalLayouts[self.indexRow].setAlignment(Qt.AlignLeft)

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

    def setDirectory(self,url):
        self.directory= url


    def newImageLabel (self,image,label):

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

    def pictureDropped(self, l):
        for url in l:
            # TODO: Restrict uploads to images only
            if os.path.exists(url):
                startI = url.rfind('/', 0, len(url)) + 1
                endI = url.rfind('.', 0, len(url))
                s = url[startI: endI]
                self.GroupBox = QGroupBox()
                numOfHLayouts = len(self.horizontalLayouts)
                newimage = imageBox(self.numOfImages)
                newimage.deleteImage.deleted.connect(self.on_deleteButton_clicked)
                self.numOfImages = self.numOfImages+1
                imagebox = newimage.setImage(url, s, self.indexRow, self.indexColumn)
                self.horizontalLayouts[self.indexRow].addWidget(imagebox)

                if (self.horizontalLayouts[numOfHLayouts -1]).count() < self.maxRowSize -1 :
                    self.indexColumn = self.indexColumn + 1
                else:
                    self.indexColumn = 0
                    self.indexRow = self.indexRow + 1

                    newLine = QHBoxLayout()
                    self.horizontalLayouts.append(newLine)
                    self.horizontalLayouts[self.indexRow].setAlignment(Qt.AlignLeft)
                    self.Layout.addLayout(self.horizontalLayouts[self.indexRow])
                

    @pyqtSlot(int)
    def on_deleteButton_clicked(self, index):
        print("Deleting from parent")

    @pyqtSlot(list)    
    def start_Pro(self,creationList):
        print(creationList)
        self.projectDetails = creationList
        self.mainDialoge.close()

        