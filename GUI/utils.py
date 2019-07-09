from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import screeninfo


def alertUser(header, error):
    windDialog = QWidget()
    QMessageBox.critical(windDialog, header, error)

def getFileNameFromPath(fileDir):
    startI = fileDir.rfind('/', 0, len(fileDir)) + 1
    fileFullName = fileDir[startI:]
    endI = fileFullName.rfind('.', 0, len(fileFullName))
    fileName = fileFullName[startI:endI]
    fileExten = fileFullName[endI+1:]
    fileExten = fileExten.lower()
    return fileFullName, fileName, fileExten

def getScreenDims():
    monitor = screeninfo.get_monitors()
    monitor = str(monitor)
    startI = monitor.rfind('(', 0, len(monitor))
    midI = monitor.rfind('x', 0, len(monitor))
    endI = monitor.find('+', 0, len(monitor))
    monitorW = int(monitor[startI+1:midI], 10)
    monitorH = int(monitor[midI+1:endI], 10)
    return monitorW, monitorH