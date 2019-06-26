from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

designMode = "Screenshots"

def alertUser(header, error):
    windDialog = QWidget()
    QMessageBox.critical(windDialog, header, error )
    print(error)