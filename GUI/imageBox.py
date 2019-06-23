from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Buttons import delButton,convertButton



class imageBox(QWidget):
    def __init__(self, index):
        super(imageBox, self).__init__()
        self.srcPath = ""
        self.groupBox = QGroupBox()
        self.layout = QVBoxLayout()
        self.Hor = QHBoxLayout()
        self.imageLabel = QLabel()

        self.imageNameLine = QLineEdit()
        self.hasActionBar = QCheckBox("Action Bar")
        self.deleteImage = delButton(self, index)
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
        pixmapimage = QPixmap(self.srcPath ).scaled(width, height)
        self.imageLabel.setPixmap(QPixmap(pixmapimage))
        self.imageNameLine.setText(label)
        self.imageNameLine.setAlignment(Qt.AlignHCenter)
        self.imageLabel.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.imageLabel)
        self.layout.addWidget(self.imageNameLine)
        self.Hor.addWidget(self.hasActionBar)
        self.Hor.addWidget(self.deleteImage)
        self.layout.addLayout(self.Hor)
        self.groupBox.setLayout(self.layout)
        return self.groupBox

    def resizeImg (self,index, row, col, width, height, isGrid =0 ):
        self.index = index
        self.deleteImage.setindex(index)
        self.row = row
        self.col = col
        pixmapimage = QPixmap(self.srcPath).scaled(width, height)
        self.imageLabel.setPixmap(QPixmap(pixmapimage))
        return self.groupBox

    def delimg(self):
        self.groupBox.setParent(None)