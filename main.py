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
        self.mainDialoge = createProjectDialog()
        self.mainDialoge.show()
        self.mainDialoge.activateWindow()
        self.setupUi(self)
        self.createUploadUI()

    def createUploadUI(self):
        uploadWidget = uploadWindow.uploadWindow()
        self.centralwidget.setLayout(uploadWidget.layoutScroll)
        self.addDockWidget(Qt.DockWidgetArea(2), uploadWidget.dockDesign)