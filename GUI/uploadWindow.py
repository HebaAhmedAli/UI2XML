from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.skelUploadWindow as  skelUploadWindow
import os

class uploadWindow(QWidget, skelUploadWindow.Ui_uploadWindow):
    def __init__(self):
        super(uploadWindow, self).__init__()
        self.setupUi(self)

        self.dockDesign.setMinimumWidth(350)
        # self.mainDialoge = createProjectDialog()
        # self.mainDialoge.show()
        # self.mainDialoge.started.connect(self.start_Pro)
        # self.actionRun.triggered.connect(self.convertFiles)

