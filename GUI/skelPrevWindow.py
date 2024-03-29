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
        self.allxmlVerticalLayout = QtWidgets.QVBoxLayout()
        self.xmlTabsHLayout = QtWidgets.QHBoxLayout()
        self.xmlTabs = QtWidgets.QTabWidget(self.xmlTabsverticalLayoutWidget)
        self.xmlTabsHLayout.addWidget(self.xmlTabs)

        self.xmlcomponentHLayout = QtWidgets.QHBoxLayout()
        self.compXMLBrowser = QtWidgets.QTextBrowser(self.xmlTabsverticalLayoutWidget)
        self.compXMLBrowser.setStyleSheet("background-color: \"white\";\n"           
            "border: 5px solid  rgb(66, 138, 255);\n"
            "color: rgb(45, 123, 250);\n"
            "font-weight: bold;\n"
            "border-radius: 20%;")
        # self.compXMLBrowser.setGeometry(QRect(0, 0, Constants.MONITOR_WIDTH*0.3, Constants.MONITOR_HEIGHT*0.65))
        self.compXMLBrowser.setAlignment(QtCore.Qt.AlignCenter)                      
        self.xmlcomponentHLayout.addWidget(self.compXMLBrowser)
        self.allxmlVerticalLayout.addLayout(self.xmlTabsHLayout)
        self.allxmlVerticalLayout.addLayout(self.xmlcomponentHLayout)

        self.activeImgVerticalLayoutWidget = QtWidgets.QWidget(prev)
        self.activeImgverticalLayout = QtWidgets.QVBoxLayout()

        self.activityListVerticalLayoutWidget = QtWidgets.QWidget()
        self.listScrolVerticalLayout = QtWidgets.QVBoxLayout()
        self.scrollArea = QtWidgets.QScrollArea(self.activityListVerticalLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.activitysScrollArea = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.activitysScrollArea)
        self.scrollArea.setMaximumWidth(300)
        self.listScrolVerticalLayout.addWidget(self.scrollArea)
        self.activitysHLayouts = []
        self.activitiesList = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.activitiesList)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.activitiesList)
        self.activitiesList.setLayout(self.verticalLayout)
        self.verticalLayout.setAlignment(QtCore.Qt.AlignTop)

        self.correctionWidget = QtWidgets.QWidget(prev)
        self.correctionLayout = QtWidgets.QVBoxLayout()

        self.compInfoLayout = QtWidgets.QHBoxLayout()
        self.verticalLayoutWidget = QtWidgets.QWidget()
        self.lblVLayout = QtWidgets.QVBoxLayout()
        self.compTypeLbl = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.compTypeLbl.setText("Component Type:")
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
        model_pred = [ k for k in Constants.MODEL_PRED]
        model_pred.sort()
        self.compTypeComboBox.addItems(model_pred)
        self.compoBoxLayout.addWidget(self.compTypeComboBox)
        self.compTypeComboBox.setEnabled(False)
        self.compInfoLayout.addLayout(self.compoBoxLayout)
        self.correctionLayout.addLayout(self.compInfoLayout)

        self.rightWidget = QtWidgets.QWidget(prev)
        self.rightHLayout = QtWidgets.QVBoxLayout()
        self.rightHLayout.addLayout(self.correctionLayout)
        self.rightHLayout.addLayout(self.listScrolVerticalLayout)

        self.mainHLayout.addLayout(self.rightHLayout)
        self.mainHLayout.addLayout(self.activeImgverticalLayout)
        self.mainHLayout.addLayout(self.allxmlVerticalLayout)
