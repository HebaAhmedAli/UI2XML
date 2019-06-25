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
    def setupUi(self, prev, mainWindow):
        mainWindow.setAcceptDrops(False)

        self.verticalLayoutWidget = QtGui.QWidget(mainWindow.centralwidget)
        # self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 200, 551))
        self.verticalLayout = QtGui.QHBoxLayout(self.verticalLayoutWidget)

        self.imagetabs = QtGui.QTabWidget(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.imagetabs)

        self.xmlTabs = QtGui.QTabWidget(self.verticalLayoutWidget)
        # self.xmlTabs.setGeometry(QtCore.QRect(12, 0, 391, 521))
        self.verticalLayout.addWidget(self.xmlTabs)

        mainWindow.lay.addWidget(self.verticalLayoutWidget)
