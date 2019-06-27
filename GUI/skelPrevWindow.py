# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'try.ui'
#
# Created by: PyQt UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QWidget, QLineEdit, QPushButton, QGridLayout, QApplication, QTableWidget, QScrollArea
from PyQt5 import QtCore, QtGui

class previewWindowSkel(object):
    def setupUi(self, prev):
        self.gridTaps = QGridLayout(prev)
        self.gridTaps.setAlignment(QtCore.Qt.AlignCenter)

        # images activeimage   xmls

        self.verticalLayoutWidget_3 = QWidget()
        #self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(9, 10, 271, 551))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.scrollArea = QScrollArea(self.verticalLayoutWidget_3)
        self.scrollArea.setWidgetResizable(True)
        self.imgsScrollArea = QWidget()
        #self.imgsScrollArea.setGeometry(QtCore.QRect(0, 0, 267, 547))
        self.scrollArea.setWidget(self.imgsScrollArea)
        self.verticalLayout_3.addWidget(self.scrollArea)


        self.activeImageWidget = QWidget()
        # self.activeImageWidget.setGeometry(QtCore.QRect(280, 10, 261, 551))
        # self.verticalLayout_2 = QtGui.QVBoxLayout(self.activeImageWidget)

        self.verticalLayoutWidget = QWidget()
        # self.verticalLayoutWidget.setGeometry(QtCore.QRect(539, 10, 301, 551))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        # self.xmlTabs = QTabWidget(self.verticalLayoutWidget)
        # self.verticalLayout.addWidget(self.xmlTabs)

        # self.gridTaps.addWidget(self.verticalLayoutWidget_3, 1, 1)
        self.gridTaps.addWidget(self.activeImageWidget, 1, 1)
        # self.gridTaps.addWidget(self.verticalLayoutWidget, 1, 3)