from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.utils as utils



class activityListItem2(QWidget):
    activateMe = pyqtSignal(str)
    def __init__(self, imgpath, imgName):
        super(activityListItem, self).__init__()
        self.imgPath = imgpath
        # self.allVWidget = QPushButton()
        # self.allVWidget.setStyleSheet("""background-color:rgba(0,0,0,0);""")
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
        self.allVLayout.addLayout(self.imageBoxLay)
        self.allVLayout.addLayout(self.nameBoxLay)
        # self.allVWidget.setLayout(self.allVLayout)
        # self.clicked.connect(self.send)

    def send(self):
        print("bruuuuh")
        self.activateMe.emit(self.imgPath)
    


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