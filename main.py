from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.skelMainScreen as skelMainscreen
import GUI.uploadWindow as uploadWindow
from GUI.createProjDialog import createProjectDialog



class mainScreen (QMainWindow, skelMainscreen.Ui_mainWindow):
    def __init__(self):
        super(mainScreen, self).__init__()
        self.state = "INS_PIC"
        self.startUp()
        
    def createUploadUI(self):
        self.uploadWidget = uploadWindow.uploadWindow()
        self.centralwidget.setLayout(self.uploadWidget.layoutScroll)
        self.addDockWidget(Qt.DockWidgetArea(2), self.uploadWidget.dockDesign)
    
    def startUp(self):
        self.mainDialoge = createProjectDialog()
        self.mainDialoge.show()
        self.mainDialoge.activateWindow()
        self.setupUi(self)
        self.createUploadUI()
        self.actionRun.triggered.connect(self.uploadWidget.scrollarea.populateProjDir)
