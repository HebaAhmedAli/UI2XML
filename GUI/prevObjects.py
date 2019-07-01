from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.utils as utils



class activityListItem(QWidget):
    activate = pyqtSignal(str)
    def __init__(self, imgpath, imgName):
        super(activityListItem, self).__init__()
        self.allHLayout = QHBoxLayout()
        self.imgpath = imgpath
        self.imageLabel = QLabel()
        self.imageNameLine = QLabel()
        pixmapimage = QPixmap(imgpath).scaled(50, 50)
        self.viewImg = QPushButton()
        self.viewImg.clicked.connect(self.sendMe)
        self.viewImg.setText("View")
        self.imageLabel.setPixmap(QPixmap(pixmapimage))
        self.imageNameLine.setText(imgName)
        self.imageNameLine.setAlignment(Qt.AlignHCenter)
        self.imageLabel.setAlignment(Qt.AlignHCenter)
        self.allHLayout.addWidget(self.imageLabel)
        self.allHLayout.addWidget(self.imageNameLine)
        self.allHLayout.addWidget(self.viewImg)


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
        self.textBrowser.setGeometry(QRect(0, 0, 500, 600))
        self.textBrowser.setAlignment(Qt.AlignCenter)                      
        vBoxlayout.addWidget(self.xmlWidget)
        self.setLayout(vBoxlayout)