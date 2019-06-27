from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.skelMainScreen as skelMainscreen
import GUI.uploadWindow as uploadWindow
from GUI.createProjDialog import createProjectDialog
import  GUI.prevWindow as prevWindow



class mainScreen (QMainWindow, skelMainscreen.Ui_mainWindow):
    def __init__(self):
        super(mainScreen, self).__init__()
        self.state = "INS_PIC"
        self.setupUi(self)
        # self.startUp()
        # self.createUploadUI()
        # self.actionRun.triggered.connect(self.uploadWidget.populateProjDir)
        prev = prevWindow.previewWindow()
        self.centralwidget.setLayout(prev.mainHLayout)
        
    def createUploadUI(self):
        self.uploadWidget = uploadWindow.uploadWindow()
        self.centralwidget.setLayout(self.uploadWidget.layoutScroll)
        self.addDockWidget(Qt.DockWidgetArea(2), self.uploadWidget.dockDesign)
    
    def startUp(self):
        self.mainDialoge = createProjectDialog()
        self.mainDialoge.show()
        self.mainDialoge.activateWindow()
