from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.skelMainScreen as skelMainscreen
import GUI.uploadWindow as uploadWindow
import  GUI.prevWindow as prevWindow



class mainScreen (QMainWindow,  skelMainscreen.Ui_mainWindow):
    def __init__(self):
        super(mainScreen, self).__init__()
        self.state = "INS_PIC"
        self.setupUi(self)
        self.projectDir = ""  #todo remove from here
        self.projectName = ""  #todo remove from here
        # self.createUploadUI()
        prev = prevWindow.previewWindow(self.centralwidget)

    def createUploadUI(self):
        uploadWidget = uploadWindow.uploadWindow()
        self.centralwidget.setLayout(uploadWidget.verticalLayout)
        self.addDockWidget(Qt.DockWidgetArea(2), uploadWidget.dockDesign)
