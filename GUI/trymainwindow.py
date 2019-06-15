from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
import os
import try_ui

class footer():
    def __init__(self):
        x = 0

class secondtry (QMainWindow,  try_ui.Ui_mainWindow):

    def __init__(self):
        super(secondtry, self).__init__()
        self.setupUi(self)
       # self.connect(self.view, SIGNAL("dropped"), self.pictureDropped)
        self.directory = ""
        self.indexColumn = 0
        self.indexRow = 0
        self.maxrowsize = 6

        self.setDirectory("D:/computer 4th year/GP/temp-directory")

        self.gridData = QWidget()
        self.Layout = QVBoxLayout()
        self.Layout.setAlignment(Qt.AlignTop)
        self.horLays = []
        '''self.gridLayout.addWidget(self.newImageLabel('221.jpg', 'ndara'), 0, 0)
        self.gridLayout.addWidget(self.newImageLabel('aabdos1.jpg', 'abdo1'), 0, 1)
        self.gridLayout.addWidget(self.newImageLabel('aabdo2', 'aabdo2'), 1, 0)
        self.gridLayout.addWidget(self.newImageLabel('logo.png', 'logo'), 1, 1)
        self.gridLayout.addWidget(self.newImageLabel('221.jpg', 'ndara'), 2, 0)
        self.gridLayout.addWidget(self.newImageLabel('aabdos1.jpg', 'abdo1'), 2, 1)
        self.gridLayout.addWidget(self.newImageLabel('aabdo2', 'aabdo2'), 3, 0)
        self.gridLayout.addWidget(self.newImageLabel('logo.png', 'logo'), 3, 1)
        '''
        self.gridData.setLayout(self.Layout)
        self.scrollarea = QScrollArea()
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
        #lay.addWidget(self.statusbarwindow)

        self.dockPictuers.setMinimumWidth(200)
        self.dockDesign.setMinimumWidth(200)

    def setDirectory(self,url):
        self.directory= url

    #D:\computer 4th year\GP\temp-directory

    def newImageLabel (self,image,label):

        #groupBox = QGridLayout("")
        groupBox= QGroupBox()
        layout = QVBoxLayout()
        Hor = QHBoxLayout()
        self.imageLabel = QLabel()
        self.text = QLabel()
        self.checkbox = QCheckBox("Action Bar")
        self.button = QPushButton("D")
        pixmapimage = QPixmap(image).scaled(201, 268)
        self.imageLabel.setPixmap(QPixmap(pixmapimage))

        self.text.setText(label)

        self.text.setAlignment(Qt.AlignHCenter)

        self.imageLabel.setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.imageLabel)
        layout.addWidget(self.text)
        Hor.addWidget(self.checkbox)
        Hor.addWidget(self.button)
        layout.addLayout(Hor)
        groupBox.setLayout(layout)
        return groupBox


    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
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

                #print(url)
                startI = url.rfind('/', 0, len(url)) + 1
                endI = url.rfind('.', 0, len(url))
                s = url[startI: endI]
                self.GroupBox = QGroupBox()
                length = len(self.horLays)
                newimage = imageBox()

                print(length)
                if length == 0:
                    newLine = QHBoxLayout()
                    self.horLays.append(newLine)
                    imagebox = newimage.setImage(url, s, 0, 0)
                    self.horLays[0].addWidget(imagebox)
                    self.horLays[0].setAlignment(Qt.AlignLeft)
                    self.indexColumn = 1
                    self.Layout.addLayout(self.horLays[0])

                elif (self.horLays[length -1]).count() < self.maxrowsize -1 :
                    imagebox = newimage.setImage(url, s, self.indexRow, self.indexColumn)
                    self.horLays[self.indexRow].addWidget(imagebox)
                    self.indexColumn = 1
                else:
                    imagebox = newimage.setImage(url, s, self.indexRow, self.indexColumn)
                    self.horLays[self.indexRow].addWidget(imagebox)
                    self.indexColumn = 0
                    self.indexRow = self.indexRow +1
                    newLine = QHBoxLayout()

                    self.horLays.append(newLine)
                    self.horLays[self.indexRow].setAlignment(Qt.AlignLeft)
                    self.Layout.addLayout(self.horLays[self.indexRow])
                #self.gridLayout.addWidget(self.newImageLabel(url, s), self.indexRow ,self.indexColumn)

                #self.indexColumn = self.indexColumn+1
                #print (self.indexColumn)
                #if self.indexColumn == self.maxrowsize :
                #    self.indexColumn=0
                #    self.indexRow =self.indexRow + 1

    '''def mousePressEvent(self, QMouseEvent):
        for i in range (0 , 10000) :
            print (QMouseEvent.pos())

    '''

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

    def deletebutton(self):
        print("iam deleting")
        self.groupBox.setParent(None)

class delButton(QPushButton):
    def __init__(self, parent):
        super(delButton, self).__init__(parent)
        self.setText("D!")
        self.clicked.connect(self.printSomething)
    def printSomething(self):
        print("iam deleting")
        self.parent.setParent(None)

app = QApplication(sys.argv)
dialog = secondtry()
dialog.show()
sys.exit(app.exec_())

