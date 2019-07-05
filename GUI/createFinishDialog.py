import sys
sys.path.append('../')
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.skelFinishDialog as skelFinishDialog


class createFinishDialog(QDialog, skelFinishDialog.Ui_Dialog):

    def __init__(self):
        super(createFinishDialog, self).__init__()
        self.setupUi(self)
        self.activateWindow()