# -*- coding: utf-8 -*-

# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from GUI.dragDropScrollArea import dragDropScroll

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



class Ui_uploadWindow(object):
    def setupUi(self, uploadWind):
        self.verticalLayoutWidget = QtWidgets.QWidget()
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(19, 9, 361, 421))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.dockDesign = QtWidgets.QDockWidget()
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.dockDesign.setFont(font)
        self.dockDesign.setStyleSheet(_fromUtf8("\n"
        "color: \"white\";"))
        self.dockDesign.setObjectName(_fromUtf8("dockDesign"))
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.dockDesign.setWidget(self.dockWidgetContents)


        # Upload Area scrollable
        self.scrollarea = dragDropScroll()
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollarea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollarea.setWidget(self.scrollarea.gridData)

        self.layoutScroll = QtWidgets.QVBoxLayout()
        self.layoutScroll.addWidget(self.scrollarea)