# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'try.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class previewWindowSkel(object):
    def setupUi(self, prev):
        
        self.verticalLayoutWidget = QtGui.QWidget(prev)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(539, 10, 301, 551))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.xmlTabs = QtGui.QTabWidget(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.xmlTabs)
        self.verticalLayoutWidget_2 = QtGui.QWidget(prev)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(280, 10, 261, 551))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayoutWidget_3 = QtGui.QWidget(prev)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(9, 10, 271, 551))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.scrollArea = QtGui.QScrollArea(self.verticalLayoutWidget_3)
        self.scrollArea.setWidgetResizable(True)
        self.imgsScrollArea = QtGui.QWidget()
        self.imgsScrollArea.setGeometry(QtCore.QRect(0, 0, 267, 547))
        self.scrollArea.setWidget(self.imgsScrollArea)
        self.verticalLayout_3.addWidget(self.scrollArea)

