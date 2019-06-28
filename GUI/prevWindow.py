from PyQt5 import QtWidgets, QtGui, QtCore
import os
import imagesize 
from GUI.skelPrevWindow import  previewWindowSkel
#from GUI.tabs import xmlTab
from GUI.componentHighlight import componentHighlight
import GUI.utils as utils

class previewWindow(QtWidgets.QWidget, previewWindowSkel):
    def __init__(self):
        super(previewWindow, self).__init__()
        self.setupUi(self)
        
    #     # For testing
        self.highlights = []
        self.activeImageWidget = QtWidgets.QWidget()
        self.pixmapX = 300
        self.pixmapY = 600
        qvbox = QtWidgets.QVBoxLayout(self.activeImageWidget)
        imageLabel = QtWidgets.QLabel(self.activeImgVerticalLayoutWidget)
        imgDir = "/home/fatema/PycharmProjects/UI2XML/GUI/main.jpg"
        
        pixmapimage = QtGui.QPixmap(imgDir).scaled(self.pixmapX, self.pixmapY)
        imageLabel.setPixmap(QtGui.QPixmap(pixmapimage))
        qvbox.addWidget(imageLabel)
        imageboxs = [[19, 19, 27, 27], [190, 135, 145, 124], [43, 311, 479, 63], [43, 405, 478, 64],
                     [81, 557, 384, 46], [170, 634, 211, 31], [116, 844, 329, 27]]
        imgW, imgH = imagesize.get(imgDir)
        print(imgW, imgH)
        for compBox in imageboxs:
            scaledCompBox =  self.calculateScaledBox(compBox, imgW, imgH)
            errorMargin = 10
            high = componentHighlight(self.activeImageWidget, scaledCompBox[2]+errorMargin, scaledCompBox[3]+errorMargin)
            high.move(scaledCompBox[0]+errorMargin, scaledCompBox[1]+errorMargin)
            self.highlights.append(high)
            print(compBox)
        self.activeImgverticalLayout.addWidget(self.activeImageWidget)

    def calculateScaledBox(self, originalBox, imgW, imgH):
        scaledBox = []
        x1 = self.pixmapX*(originalBox[0]/imgW)
        y1 = self.pixmapY*(originalBox[1]/imgH)
        originalX2 = originalBox[0]+originalBox[2]
        originalY2 = originalBox[1]+originalBox[3]
        x2 = self.pixmapX*(originalX2/imgW)
        y2 = self.pixmapY*(originalY2/imgH)
        scaledBox.append(x1)
        scaledBox.append(y1)
        scaledBox.append(x2-x1)
        scaledBox.append(y2-y1)
        return scaledBox

