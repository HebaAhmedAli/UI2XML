from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.utils as utils



class activityListItem(QHBoxLayout):
    activate = pyqtSignal(str)
    def __init__(self, imgpath, imgName):
        super(activityListItem, self).__init__()
        self.allVLayout = QVBoxLayout()
        self.imageBoxLay = QVBoxLayout()
        self.nameBoxLay = QVBoxLayout()
        self.viewBtnLay = QVBoxLayout()
        self.imgpath = imgpath
        self.imageLabel = QLabel()
        self.imageNameLine = QLabel()
        pixmapimage = QPixmap(imgpath).scaled(50, 50)
        self.viewImg = QPushButton()
        self.viewImg.clicked.connect(self.send)
        self.viewImg.setText("View")
        self.imageLabel.setPixmap(QPixmap(pixmapimage))
        self.imageNameLine.setText(imgName)
        self.imageNameLine.setAlignment(Qt.AlignHCenter)
        self.imageLabel.setAlignment(Qt.AlignHCenter)
        self.imageBoxLay.addWidget(self.imageLabel)
        self.nameBoxLay.addWidget(self.imageNameLine)
        self.viewBtnLay.addWidget(self.viewImg)
        self.addLayout(self.imageBoxLay)
        self.addLayout(self.nameBoxLay)
        self.addLayout(self.viewBtnLay)

    def send(self):
        self.activate.emit(self.imgpath)
        print("yasatr")

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

class viewButton(QPushButton):
    activated = pyqtSignal()
    def __init__(self, imgPath):
        super(viewButton, self).__init__()
        self.setText("View me!")
        self.clicked.connect(self.activateImg)

    def activateImg(self):
        self.activated.emit()
        print("iam viewing")