from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.skelUploadWindow as  skelUploadWindow
import os

class uploadWindow(QWidget, skelUploadWindow.Ui_uploadWindow):
    def __init__(self):
        super(uploadWindow, self).__init__()       
        self.setupUi(self)

