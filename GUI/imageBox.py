from PyQt4.QtCore import *
from PyQt4.QtGui import *
from delButton import delButton


class imageBox(QWidget):
    def __init__(self):
        super(imageBox, self).__init__()
        self.groupBox = QGroupBox()
        self.layout = QVBoxLayout()
        self.Hor = QHBoxLayout()
        self.imageLabel = QLabel()
        self.text = QLabel()
        self.checkbox = QCheckBox("Action Bar")
        self.button = delButton(self)
        self.checked = False
        self.row = 0
        self.col = 0
        #self.button.clicked.connect(self.deletebutton)

    def setImage (self, image, label, row, col):
        self.row = row
        self.col = col
        pixmapimage = QPixmap(image).scaled(201, 268)
        self.imageLabel.setPixmap(QPixmap(pixmapimage))

        self.text.setText(label)

        self.text.setAlignment(Qt.AlignHCenter)

        self.imageLabel.setAlignment(Qt.AlignHCenter)

        self.layout.addWidget(self.imageLabel)
        self.layout.addWidget(self.text)
        self.Hor.addWidget(self.checkbox)
        self.Hor.addWidget(self.button)
        self.layout.addLayout(self.Hor)
        self.groupBox.setLayout(self.layout)
        return self.groupBox
