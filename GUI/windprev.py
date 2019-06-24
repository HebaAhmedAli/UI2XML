# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
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

class previewWind(object):
    def setupUi(self, mainWindow):
        self.verticalLayoutWidget = QtGui.QWidget()
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 401, 551))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.imageTabs = QtGui.QTabWidget(self.verticalLayoutWidget)
        self.imageTabs.setObjectName(_fromUtf8("imageTabs"))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.imageTabs.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.imageTabs.addTab(self.tab_4, _fromUtf8(""))
        self.verticalLayout.addWidget(self.imageTabs)
        self.verticalLayoutWidget_2 = QtGui.QWidget()
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(399, 0, 401, 551))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.dockWidget_2 = QtGui.QDockWidget(self.verticalLayoutWidget_2)
        self.dockWidget_2.setObjectName(_fromUtf8("dockWidget_2"))
        self.dockWidgetContents_2 = QtGui.QWidget()
        self.dockWidgetContents_2.setObjectName(_fromUtf8("dockWidgetContents_2"))
        self.xmlTabs = QtGui.QTabWidget(self.dockWidgetContents_2)
        self.xmlTabs.setGeometry(QtCore.QRect(12, 0, 391, 521))
        self.xmlTabs.setObjectName(_fromUtf8("xmlTabs"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.textBrowser = QtGui.QTextBrowser(self.tab)
        self.textBrowser.setGeometry(QtCore.QRect(0, 0, 381, 491))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.xmlTabs.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.xmlTabs.addTab(self.tab_2, _fromUtf8(""))
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        self.verticalLayout_2.addWidget(self.dockWidget_2)
        
        self.retranslateUi()

    def retranslateUi(self):
        self.imageTabs.setTabText(self.imageTabs.indexOf(self.tab_3), _translate("MainWindow", "Tab 1", None))
        self.imageTabs.setTabText(self.imageTabs.indexOf(self.tab_4), _translate("MainWindow", "Tab 2", None))
        self.xmlTabs.setTabText(self.xmlTabs.indexOf(self.tab), _translate("MainWindow", "Tab 1", None))
        self.xmlTabs.setTabText(self.xmlTabs.indexOf(self.tab_2), _translate("MainWindow", "Tab 2", None))

