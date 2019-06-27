# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'try.ui'
#
# Created by: PyQt UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import GUI.activityListItem as activityListItem

class previewWindowSkel(object):
    def setupUi(self, prev):
        # self.mainHLayout = QtWidgets.QHBoxLayout()
        # self.mainHWidget = QtWidgets.QWidget()
        # self.mainHWidget.setLayout(self.mainHLayout)

        # self.tabVLayout = QtWidgets.QVBoxLayout()
        # self.mainHLayout.addLayout(self.tabVLayout)
        # self.xmlTabWidget = QtWidgets.QTabWidget()

        # self.activeImageLayout = QtWidgets.QVBoxLayout()
        # self.mainHLayout.addLayout(self.activeImageLayout)
        # self.activeImage = QtWidgets.QWidget()
        # self.activeImage.setLayout(self.activeImageLayout)
        
        # self.imageList = QtWidgets.QVBoxLayout()
        # # self.imageList.setLayout(self.mainHLayout)
        # self.activitysHLayouts = []

        # firstactivityHLayout = QtWidgets.QHBoxLayout()
        # self.activitysHLayouts.append(firstactivityHLayout)
        # self.imageList.addLayout(self.activitysHLayouts[0])

        self.verticalLayoutWidget = QtWidgets.QWidget(prev)
        # self.verticalLayoutWidget.setGeometry(QtCore.QRect(539, 10, 301, 551))
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.xmlTabs = QtWidgets.QTabWidget(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.xmlTabs)
        tab = QtWidgets.QWidget()
        self.xmlTabs.addTab(tab, "Hope")

        
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(prev)
        # self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(280, 10, 261, 551))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        pixmapimage2 = QtGui.QPixmap("/home/fatema/PycharmProjects/UI2XML/GUI/main.jpg").scaled(300, 600)
        lab = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        lab.setPixmap(pixmapimage2)
        self.verticalLayout_2.addWidget(lab)



        self.verticalLayoutWidget_3 = QtWidgets.QWidget(prev)
        # self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(9, 10, 271, 551))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.scrollArea = QtWidgets.QScrollArea(self.verticalLayoutWidget_3)
        self.scrollArea.setWidgetResizable(True)
        self.activitysScrollArea = QtWidgets.QWidget()
        # self.activitysScrollArea.setGeometry(QtCore.QRect(0, 0, 267, 547))
        self.scrollArea.setWidget(self.activitysScrollArea)
        self.verticalLayout_3.addWidget(self.scrollArea)
        self.activitysHLayouts = []

        firstactivityHLayout = activityListItem.activityListItem()
        self.activitysHLayouts.append(firstactivityHLayout)
        self.scrollArea.setLayout(self.activitysHLayouts[0])

        self.activitiesList = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.activitiesList)
        self.activitiesList.setLayout(self.verticalLayout_4)

        self.mainHLayout = QtWidgets.QHBoxLayout()
        self.mainHLayout.addLayout(self.verticalLayout_3)
        self.mainHLayout.addLayout(self.verticalLayout_2)
        self.mainHLayout.addLayout(self.verticalLayout)