# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'try.ui'
#
# Created by: PyQt UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import Constants as Constants

class previewWindowSkel(object):
    def setupUi(self, prev):
        self.xmlTabsverticalLayoutWidget = QtWidgets.QWidget(prev)
        self.xmlTabsverticalLayout = QtWidgets.QVBoxLayout()
        self.xmlTabs = QtWidgets.QTabWidget(self.xmlTabsverticalLayoutWidget)

        self.xmlTabsverticalLayout.addWidget(self.xmlTabs)

        self.activeImgVerticalLayoutWidget = QtWidgets.QWidget(prev)
        self.activeImgverticalLayout = QtWidgets.QVBoxLayout()

        self.activityListVerticalLayoutWidget = QtWidgets.QWidget(prev)
        self.listScrolVerticalLayout = QtWidgets.QVBoxLayout()
        self.scrollArea = QtWidgets.QScrollArea(self.activityListVerticalLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.activitysScrollArea = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.activitysScrollArea)
        self.listScrolVerticalLayout.addWidget(self.scrollArea)
        #self.scrollArea.setMaximumWidth(300)
        self.activitysHLayouts = []

        self.activitiesList = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.activitiesList)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.activitiesList.setLayout(self.verticalLayout)

        self.mainHLayout = QtWidgets.QHBoxLayout()
        self.mainHLayout.addLayout(self.listScrolVerticalLayout)
        self.mainHLayout.addLayout(self.activeImgverticalLayout)
        self.mainHLayout.addLayout(self.xmlTabsverticalLayout)