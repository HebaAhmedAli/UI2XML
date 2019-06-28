from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def alertUser(header, error):
    windDialog = QWidget()
    QMessageBox.critical(windDialog, header, error)
    print(error)

def getFileNameFromPath(fileDir):
    startI = fileDir.rfind('/', 0, len(fileDir)) + 1
    fileFullName = fileDir[startI:]
    endI = fileFullName.rfind('.', 0, len(fileFullName))
    fileName = fileFullName[startI:endI]
    fileExten = fileFullName[endI+1:]
    fileExten = fileExten.lower()
    return fileFullName, fileName, fileExten
