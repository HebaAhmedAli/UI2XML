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
        self.mainHLayout = QtWidgets.QHBoxLayout()
        self.xmlTabsverticalLayoutWidget = QtWidgets.QWidget(prev)
        self.xmlTabsverticalLayout = QtWidgets.QVBoxLayout()
        self.xmlTabs = QtWidgets.QTabWidget(self.xmlTabsverticalLayoutWidget)
        self.xmlTabsverticalLayout.addWidget(self.xmlTabs)

        self.activeImgVerticalLayoutWidget = QtWidgets.QWidget(prev)
        self.activeImgverticalLayout = QtWidgets.QVBoxLayout()

        self.activityListVerticalLayoutWidget = QtWidgets.QWidget()
        self.listScrolVerticalLayout = QtWidgets.QHBoxLayout()
        self.scrollArea = QtWidgets.QScrollArea(self.activityListVerticalLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.activitysScrollArea = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.activitysScrollArea)
        self.listScrolVerticalLayout.addWidget(self.scrollArea)
        self.activitysHLayouts = []
        self.activitiesList = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.activitiesList)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.activitiesList)
        self.activitiesList.setLayout(self.verticalLayout)


        self.correctionWidget = QtWidgets.QWidget(prev)
        self.correctionLayout = QtWidgets.QVBoxLayout()

        self.compInfoLayout = QtWidgets.QHBoxLayout()
        self.verticalLayoutWidget = QtWidgets.QWidget()
        self.lblVLayout = QtWidgets.QVBoxLayout()
        self.compTypeLbl = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.compTypeLbl.setText("Component Name:")
        self.lblVLayout.addWidget(self.compTypeLbl)
        self.compNewTypeLbl = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.compNewTypeLbl.setText("Component New Type:")
        self.lblVLayout.addWidget(self.compNewTypeLbl)
        self.compInfoLayout.addLayout(self.lblVLayout)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget()
        self.compoBoxLayout = QtWidgets.QVBoxLayout()
        self.compOriginalLbl = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.compOriginalLbl.setText("")
        self.compoBoxLayout.addWidget(self.compOriginalLbl)
        self.compTypeComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.compTypeComboBox.addItems(Constants.MODEL_PRED)
        self.compoBoxLayout.addWidget(self.compTypeComboBox)
        self.compTypeComboBox.setEnabled(False)
        self.compInfoLayout.addLayout(self.compoBoxLayout)
        self.correctionLayout.addLayout(self.compInfoLayout)

        self.buttonsLayout = QtWidgets.QHBoxLayout()
        self.updateBtn = QtWidgets.QPushButton()
        self.updateBtn.setText("Change")
        self.updateBtn.setEnabled(False)
        self.buttonsLayout.addWidget(self.updateBtn)
        self.connectBtn = QtWidgets.QPushButton()
        self.connectBtn.setText("Connect")
        # self.connectBtn.setEnabled(False)
        self.buttonsLayout.addWidget(self.connectBtn)
        self.correctionLayout.addLayout(self.buttonsLayout)
        # self.verticalLayoutWidget.setMinimumHeight(Constants.MONITOR_HEIGHT/3)

        self.rightWidget = QtWidgets.QWidget(prev)
        self.rightHLayout = QtWidgets.QVBoxLayout()
        self.rightHLayout.addLayout(self.correctionLayout)
        self.rightHLayout.addLayout(self.listScrolVerticalLayout)

        self.mainHLayout.addLayout(self.rightHLayout)
        self.mainHLayout.addLayout(self.activeImgverticalLayout)
        self.mainHLayout.addLayout(self.xmlTabsverticalLayout)
