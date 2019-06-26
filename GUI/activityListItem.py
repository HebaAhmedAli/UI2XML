from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI



class activityListItem(QHBoxLayout):
    def __init__(self):
        super(activityListItem, self).__init__()
        self.imageBoxLay = QVBoxLayout()
        self.nameBoxLay = QVBoxLayout()
        self.imageLabel = QLabel()
        self.imageNameLine = QLabel()
        pixmapimage = QPixmap("/home/fatema/PycharmProjects/UI2XML/GUI/main.jpg").scaled(50, 50)
        self.imageLabel.setPixmap(QPixmap(pixmapimage))
        label = "main.jpg"
        self.imageNameLine.setText(label)
        self.imageNameLine.setAlignment(Qt.AlignHCenter)
        self.imageLabel.setAlignment(Qt.AlignHCenter)
        self.imageBoxLay.addWidget(self.imageLabel)
        self.nameBoxLay.addWidget(self.imageNameLine)
        self.addLayout(self.imageBoxLay)
        self.addLayout(self.nameBoxLay)
