from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.utils as utils
import Constants



class activityListItem(QHBoxLayout):
    activate = pyqtSignal(str)
    def __init__(self, imgpath, imgName):
        super(activityListItem, self).__init__()
        self.allVLayout = QVBoxLayout()
        self.allVLayoutWidget = QWidget()
        self.allVLayoutWidget.setLayout(self.allVLayout)
        self.imageBoxLay = QVBoxLayout()
        self.nameBoxLay = QVBoxLayout()
        self.viewBtnLay = QVBoxLayout()
        self.imgpath = imgpath
        self.imageLabel = QLabel(self.allVLayoutWidget)
        self.imageNameLine = QLabel(self.allVLayoutWidget)
        pixmapimage = QPixmap(imgpath).scaled(50, 50)
        self.viewImg = QPushButton(self.allVLayoutWidget)
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
        self.textBrowser.setMinimumHeight(Constants.MONITOR_HEIGHT*0.65)
        self.textBrowser.setMinimumWidth(Constants.MONITOR_WIDTH*0.3)
        self.textBrowser.setAlignment(Qt.AlignCenter)                      
        vBoxlayout.addWidget(self.textBrowser)
        self.setLayout(vBoxlayout)
        self.compXMLBrowser = QTextBrowser(self.xmlWidget)
        self.compXMLBrowser.setStyleSheet("background-color: \"white\";\n"           
            "border: 5px solid  rgb(66, 138, 255);\n"
            "color: rgb(45, 123, 250);\n"
            "font-weight: bold;\n"
            "border-radius: 20%;")
        # self.compXMLBrowser.setGeometry(QRect(0, 0, Constants.MONITOR_WIDTH*0.3, Constants.MONITOR_HEIGHT*0.65))
        self.compXMLBrowser.setAlignment(Qt.AlignCenter)                      
        vBoxlayout.addWidget(self.compXMLBrowser)
        # self.setLayout(vBoxlayout)