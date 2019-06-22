from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Buttons import delButton,convertButton



class imageBox(QWidget):
    def __init__(self, index):
        super(imageBox, self).__init__()
        self.path = ""
        self.label =""
        self.groupBox = QGroupBox()
        self.layout = QVBoxLayout()
        self.Hor = QHBoxLayout()
        self.imageLabel = QLabel()
        #self.imageLabel.minimumWidth = 50
        self.text = QLabel()
        self.checkbox = QCheckBox("Action Bar")
        self.deleteImage = delButton(self, index)
        self.convetImage = convertButton(self)
        self.checked = False
        self.row = 0
        self.col = 0
        print(index)
        self.index = index
        #self.button.clicked.connect(self.deletebutton)

    def setImage (self, image, label, row, col, width, height, isGrid =0):
        self.row = row
        self.col = col
        self.path = image
        self.label = label
        pixmapimage = QPixmap(self.path ).scaled(width, height)
        self.imageLabel.setPixmap(QPixmap(pixmapimage))
        self.text.setText(self.label)
        self.text.setAlignment(Qt.AlignHCenter)
        self.imageLabel.setAlignment(Qt.AlignHCenter)
        self.layout.addWidget(self.imageLabel)
        self.layout.addWidget(self.text)
        self.Hor.addWidget(self.checkbox)
        self.Hor.addWidget(self.deleteImage)
        self.layout.addLayout(self.Hor)
        self.groupBox.setLayout(self.layout)
        return self.groupBox

    def resizeImg (self,index, row, col, width, height, isGrid =0 ):
        self.index = index
        self.deleteImage.setindex(index)
        self.row = row
        self.col = col
        pixmapimage = QPixmap(self.path).scaled(width, height)
        self.imageLabel.setPixmap(QPixmap(pixmapimage))
        return self.groupBox

    def delimg(self):
        self.groupBox.setParent(None)