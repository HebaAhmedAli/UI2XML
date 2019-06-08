from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os
import urllib.request
import try_ui

class footer():
    def __init__(self):
        x=0





class secondtry (QMainWindow,  try_ui.Ui_firstTry):

    def __init__(self):
        super(secondtry, self).__init__()
        self.setupUi(self)
       # self.connect(self.view, SIGNAL("dropped"), self.pictureDropped)

        self.indexColumn =0
        self.indexRow =0
        self.maxrowsize = 6


        self.gridData = QWidget()
        self.gridLayout = QGridLayout()
        '''self.gridLayout.addWidget(self.newImageLabel('221.jpg', 'ndara'), 0, 0)
        self.gridLayout.addWidget(self.newImageLabel('aabdos1.jpg', 'abdo1'), 0, 1)
        self.gridLayout.addWidget(self.newImageLabel('aabdo2', 'aabdo2'), 1, 0)
        self.gridLayout.addWidget(self.newImageLabel('logo.png', 'logo'), 1, 1)
        self.gridLayout.addWidget(self.newImageLabel('221.jpg', 'ndara'), 2, 0)
        self.gridLayout.addWidget(self.newImageLabel('aabdos1.jpg', 'abdo1'), 2, 1)
        self.gridLayout.addWidget(self.newImageLabel('aabdo2', 'aabdo2'), 3, 0)
        self.gridLayout.addWidget(self.newImageLabel('logo.png', 'logo'), 3, 1)
        '''
        self.gridData.setLayout(self.gridLayout)
        self.scrollarea= QScrollArea()
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.scrollarea.setWidget(self.gridData)

        self.statusbarwindow = QStatusBar()
        self.statusbarwindow.setSizeGripEnabled(False)

        stylesheet = \
            "QLabel {\n" \
            + "color: red;\n" \
            + "}"
        self.statusbarwindow.setStyleSheet(stylesheet)
        lay = QVBoxLayout(self.centralwidget)
        lay.addWidget(self.scrollarea)
        lay.addWidget(self.statusbarwindow)





    def newImageLabel (self,image,label):

        #groupBox = QGridLayout("")
        groupBox= QGroupBox()
        layout = QVBoxLayout()
        self.imageLabel = QLabel()
        self.text = QLabel()

        pixmapimage = QPixmap(image).scaled(201, 268)
        self.imageLabel.setPixmap(QPixmap(pixmapimage))

        self.text.setText(label)

        self.text.setAlignment(Qt.AlignHCenter)

        self.imageLabel.setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.imageLabel)
        layout.addWidget(self.text)
        groupBox.setLayout(layout)
        return groupBox




    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self.pictureDropped( links)
        else:
            event.ignore()

    def pictureDropped(self, l):
        for url in l:
            if os.path.exists(url):



                self.gridLayout.addWidget(self.newImageLabel(url, 'ndara'), self.indexRow ,self.indexColumn)

                self.indexColumn = self.indexColumn+1
                print (self.indexColumn)
                if self.indexColumn == self.maxrowsize :
                    self.indexColumn=0
                    self.indexRow =self.indexRow+1







app = QApplication(sys.argv)
dialog = secondtry()
dialog.show()
sys.exit(app.exec_())

