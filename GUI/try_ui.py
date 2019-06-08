# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'try.ui'
#
# Created: Fri Feb 15 21:33:21 2019
#      by: PyQt4 UI code generator 4.11.1
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

class Ui_firstTry(object):
    def setupUi(self, firstTry):
        firstTry.setObjectName(_fromUtf8("firstTry"))
        firstTry.resize(800, 600)
        firstTry.setAcceptDrops(True)
        self.centralwidget = QtGui.QWidget(firstTry)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        firstTry.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(firstTry)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        firstTry.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(firstTry)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        firstTry.setStatusBar(self.statusbar)
        self.dockPictures = QtGui.QDockWidget(firstTry)
        self.dockPictures.setObjectName(_fromUtf8("dockPictures"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.dockPictures.setWidget(self.dockWidgetContents)
        firstTry.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockPictures)
        self.dockDesign = QtGui.QDockWidget(firstTry)
        self.dockDesign.setObjectName(_fromUtf8("dockDesign"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.dockDesign.setWidget(self.dockWidgetContents_2)
        firstTry.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockDesign)

        self.retranslateUi(firstTry)
        QtCore.QMetaObject.connectSlotsByName(firstTry)

    def retranslateUi(self, firstTry):
        firstTry.setWindowTitle(_translate("firstTry", "MainWindow", None))
        self.dockPictures.setWindowTitle(_translate("firstTry", "Desgin", None))
        self.dockDesign.setWindowTitle(_translate("firstTry", "Pictures", None))

