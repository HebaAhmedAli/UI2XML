from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



class imageBox(QWidget):
    def __init__(self, index):
        super(imageBox, self).__init__()
        self.srcPath = ""
        self.groupBox = QGroupBox()
        self.fullImageBoxLay = QVBoxLayout()
        self.checkboxsLay = QWidget()
        self.checkBoxs = QVBoxLayout()
        self.Hor = QHBoxLayout()
        self.imageLabel = QLabel()


        self.imageNameLine = QLineEdit()
        self.hasActionBar = QCheckBox("Action Bar")
        self.staticList = QCheckBox("Static List")
        self.checkBoxs.addWidget(self.hasActionBar)
        self.checkBoxs.addWidget(self.staticList)

        self.deleteImage = delButton(self, index)
        self.checkboxsLay.setLayout(self.checkBoxs)
        self.Hor.addWidget(self.checkboxsLay)
        self.Hor.addWidget(self.deleteImage)

        # self.checked = False
        self.row = 0
        self.col = 0
        print(index)
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
        return self.groupBox


class delButton(QPushButton):
    deleted = pyqtSignal(int)
    def __init__(self, parent, imageIndex):
        super(delButton, self).__init__(parent)
        self.setText("Delete me!")
        self.index = imageIndex
        self.clicked.connect(self.deleteImageBox)

    def deleteImageBox(self):
        print("iam deleting")
        self.deleted.emit(self.index)
