from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

designModes = ("Screenshots", "Hand Darwing",  "PSD File")
designMode = designModes[0]
projCreationDetails = []

def alertUser(header, error):
    windDialog = QWidget()
    QMessageBox.critical(windDialog, header, error)
    print(error)