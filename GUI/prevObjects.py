from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.utils as utils
import Constants


class activityListItem(QHBoxLayout):
    def __init__(self, imgpath, imgName):
        super(activityListItem, self).__init__()
        self.allVLayout = QVBoxLayout()
        self.imageBoxLay = QVBoxLayout()
        self.nameBoxLay = QVBoxLayout()
        self.imageLabel = QLabel()
        self.imageNameLine = QLabel()
        pixmapimage = QPixmap(imgpath).scaled(50, 50)
        self.imageLabel.setPixmap(QPixmap(pixmapimage))
        self.imageNameLine.setText(imgName)
        self.imageNameLine.setAlignment(Qt.AlignHCenter)
        self.imageLabel.setAlignment(Qt.AlignHCenter)
        self.imageBoxLay.addWidget(self.imageLabel)
        self.nameBoxLay.addWidget(self.imageNameLine)
        self.addLayout(self.imageBoxLay)
        self.addLayout(self.nameBoxLay)


class xmlTab(QWidget):
    def __init__(self):
        super(xmlTab, self).__init__()
        vBoxlayout	= QVBoxLayout()
        self.xmlWidget = QWidget()
        self.textBrowser = QTextBrowser(self.xmlWidget)
        self.textBrowser.setStyleSheet("background-color: \"white\";\n"           
            "border: 5px solid  rgb(66, 138, 255);\n"
            "color: 5px solid  \"black\";\n"
            "border-radius: 20%;")
        self.textBrowser.setGeometry(QRect(0, 0, Constants.MONITOR_WIDTH*Constants.textBrowserWidth, Constants.MONITOR_HEIGHT*0.85))
        self.textBrowser.setAlignment(Qt.AlignCenter)                      
        vBoxlayout.addWidget(self.xmlWidget)
        self.setLayout(vBoxlayout)