from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Buttons import delButton,convertButton



class imageBox(QWidget):
    def __init__(self, index):
        super(imageBox, self).__init__()
        self.groupBox = QGroupBox()
        # self.layout = QVBoxLayout()
        self.Hor = QHBoxLayout()
        self.imageLabel = QLabel()
        self.imageLabel.minimumWidth = 50
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

    def setImage (self, image, label, row, col):
        self.row = row
        self.col = col
        pixmapimage = QPixmap(image).scaled(50, 50)
        self.imageLabel.setPixmap(QPixmap(pixmapimage))

        self.text.setText(label)

        # self.text.setAlignment(Qt.AlignHCenter)

        # self.imageLabel.setAlignment(Qt.AlignHCenter)

        self.Hor.addWidget(self.imageLabel)
        self.Hor.addWidget(self.text)
        self.Hor.addWidget(self.checkbox)
        self.Hor.addWidget(self.deleteImage)
        self.Hor.addWidget(self.convetImage)
        # self.layout.addLayout(self.Hor)
        self.groupBox.setLayout(self.Hor)
        return self.groupBox
