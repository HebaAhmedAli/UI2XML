from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.utils as utils
import Constants


class activityListItem(QWidget):
    #activate = pyqtSignal(str)
    def __init__(self, imgpath, imgName):
        super(activityListItem, self).__init__()
        self.allHLayout = QHBoxLayout()
        self.imgpath = imgpath
        self.imageLabel = QLabel()
        self.imageNameLine = QLabel()
        pixmapimage = QPixmap(imgpath).scaled(50, 50)
        self.viewImg = QPushButton()
        #self.viewImg.clicked.connect(self.sendMe)
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
            "border: 5px solid  rgb(66, 138, 255);\n"
            "color: 5px solid  \"black\";\n"
            "border-radius: 20%;")
        self.textBrowser.setGeometry(QRect(0, 0, Constants.MONITOR_WIDTH*0.3, Constants.MONITOR_HEIGHT*0.85))
        self.textBrowser.setAlignment(Qt.AlignCenter)                      
        vBoxlayout.addWidget(self.xmlWidget)
        self.setLayout(vBoxlayout)


class activityListItem(QListWidgetItem):
    def __init__(self, imgpath, imgName):
        super(activityListItem, self).__init__()
        self.imgPath = imgpath
        # self.allVLayout = QHBoxLayout()
        self.icon = QIcon()
        self.pmImg = QPixmap(imgpath)
        self.icon.addPixmap(self.pmImg, QIcon.Normal, QIcon.On)
        # self.icon.pixmap(QSize(100,50))
        self.setIcon(self.icon)
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(self.pmImg)
        # self.allVLayout.addWidget(self.imageLabel)
        self.lbl = QLabel()
        self.setText(imgName)
        self.setSizeHint(QSize(150,65))
        self.setBackground(QBrush(QColor("white")))
        # self.allVLayout.addWidget(self.lbl)
        # self.setFixedSize(150,50)
        # self.setData(imgName)
        # self.addWidget(self.lbl)