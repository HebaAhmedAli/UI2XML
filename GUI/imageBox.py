from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class imageBox(QWidget):
    def __init__(self, index, width, height):
        super(imageBox, self).__init__()
        self.srcPath = ""
        self.groupBox = QGroupBox()
        # self.groupBox.setMinimumWidth(width + 45)
        # self.groupBox.setMinimumHeight(height + 165)
        self.groupBox.setMaximumWidth(width + 40)
        self.groupBox.setMaximumHeight(height + 165)

        #self.groupBox.setStyleSheet("""background-color: #acf3da;
        #border: 1px solid #4d0056""")
        self.fullImageBoxLay = QVBoxLayout()
        self.checkboxsLay = QWidget()
        self.buttonsBox = QWidget()

        self.buttonsLayout = QVBoxLayout()
        self.checkBoxs = QVBoxLayout()
        self.Hor = QHBoxLayout()
        self.imageLabel = QLabel()

        self.imageNameLine = QLineEdit()
        self.hasActionBar = QCheckBox("Action Bar")
        self.staticList = QCheckBox("Static List")
        self.checkBoxs.addWidget(self.hasActionBar)
        self.checkBoxs.addWidget(self.staticList)
        self.deleteImage = delButton(self, index)

        self.cropImage = cropButton(self, index)
        self.buttonsLayout.addWidget(self.deleteImage)
        self.buttonsLayout.addWidget(self.cropImage)
        self.checkboxsLay.setLayout(self.checkBoxs)
        self.buttonsBox.setLayout(self.buttonsLayout)
        self.Hor.addWidget(self.checkboxsLay)
        self.Hor.addWidget(self.buttonsBox)

        # self.checked = False
        self.row = 0
        self.col = 0
        # print(index)
        self.index = index
    # TODO: row and column can be calculated from the index
    def setImage (self, image, label, row, col, width, height, isGrid =0):
        self.row = row
        self.col = col
        self.srcPath = image
        print(self.srcPath)
        pixmapimage = QPixmap(self.srcPath).scaled(width, height)
        self.imageLabel.setPixmap(QPixmap(pixmapimage))
        self.imageNameLine.setText(label)
        self.imageNameLine.setAlignment(Qt.AlignHCenter)
        self.imageLabel.setAlignment(Qt.AlignHCenter)
        self.fullImageBoxLay.addWidget(self.imageLabel)
        self.fullImageBoxLay.addWidget(self.imageNameLine)

        self.fullImageBoxLay.addLayout(self.Hor)
        self.groupBox.setLayout(self.fullImageBoxLay)
        return self.groupBox

    def resizeImg (self,index, row, col, width, height, isGrid =0 ):
        self.index = index
        self.deleteImage.index=index
        self.row = row
        self.col = col
        pixmapimage = QPixmap(self.srcPath).scaled(width, height)
        self.imageLabel.setPixmap(QPixmap(pixmapimage))
        self.fullImageBoxLay.addLayout(self.Hor)
        self.groupBox.setLayout(self.fullImageBoxLay)
        self.groupBox.setMaximumWidth(width + 40)
        self.groupBox.setMaximumHeight(height + 165)
        return self.groupBox

    def changeImge(selfself, imagePath):
        print("tl3t")
        # pixmapimage = QPixmap(self.srcPath).scaled(width, height)
        # self.imageLabel.setPixmap(QPixmap(pixmapimage))

class delButton(QPushButton):
    deleted = pyqtSignal(int)
    def __init__(self, parent, imageIndex):
        super(delButton, self).__init__(parent)
        iconImage = QIcon()
        iconImage.addPixmap(QPixmap("Resources/Images/delete-white.png"), QIcon.Normal, QIcon.Off)
        self.setIcon(iconImage)
        #self.setText("Delete")
        self.setStyleSheet("""
        background-color:rgba(0,0,0,0)""")
        self.resize(50,50)

        self.index = imageIndex
        self.clicked.connect(self.deleteImageBox)

    def deleteImageBox(self):
        self.deleted.emit(self.index)

class cropButton(QPushButton):
    crop = pyqtSignal(int)
    def __init__(self, parent, imageIndex):
        super(cropButton, self).__init__(parent)
        iconImage = QIcon()
        iconImage.addPixmap(QPixmap("Resources/Images/crop-white.png"), QIcon.Normal, QIcon.Off)
        self.setIcon(iconImage)
        #self.setText("Delete")
        self.setStyleSheet("""
        background-color:rgba(0,0,0,0)""")
        self.resize(50,50)

        self.index = imageIndex
        self.clicked.connect(self.cropImageBox)

    def cropImageBox(self):
        self.crop.emit(self.index)

