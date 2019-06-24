from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os

class imageObj(QWidget):
    def __init__(self, imagepath):
        super(imageTab, self).__init__()
        hBoxlayout	= QHBoxLayout()
        self.imageLabel = QLabel()
        pixmapimage = QPixmap(imagepath).scaled(400,650)
        self.imageLabel.setPixmap(QPixmap(pixmapimage))
        self.imageLabel.setAlignment(Qt.AlignCenter)
        hBoxlayout.addWidget(self.imageLabel)
        self.labelName = QLabel("blue")
        self.labelName.setAlignment(Qt.AlignCenter)
        hBoxlayout.addWidget(self.labelName)        
        self.setLayout(vBoxlayout)

class xmlTab(QWidget):
    def __init__(self):
        super(xmlTab, self).__init__()
        vBoxlayout	= QVBoxLayout()
        self.xmlWidget = QWidget()
        self.textBrowser = QTextBrowser(self.xmlWidget)
        self.textBrowser.setStyleSheet("background-color: \"white\";\n"
            "color: rgb(156,156,156);\n"
            "border: 5px solid  rgb(66, 138, 255);\n"
            "border-radius: 20%;")
        self.textBrowser.setGeometry(QRect(0, 0, 300, 600))
        self.textBrowser.setAlignment(Qt.AlignCenter)                      
        vBoxlayout.addWidget(self.xmlWidget)
        self.setLayout(vBoxlayout)