# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import sys
sys.path.append('../')
from PyQt5 import QtCore, QtWidgets, QtWidgets
import GUI.clickableLineEdit as clickableLineEdit
import os
import Constants

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):

        Dialog.resize(400, 274)
        # Dialog.setStyleSheet("""background-color:#515790;""")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 17, 160, 161))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        #self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        #self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.label_3)
        self.label_5 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.label_5)
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.label)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(130, 20, 221, 161))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        #self.projectNameLine = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        #self.verticalLayout_2.addWidget(self.projectNameLine)
        self.packageNameLine = QtWidgets.QLineEdit(self.verticalLayoutWidget_2)
        self.verticalLayout_2.addWidget(self.packageNameLine)
        self.projectDirectoryL = clickableLineEdit.clickableLineEdit(self.verticalLayoutWidget_2)
        self.verticalLayout_2.addWidget(self.projectDirectoryL)
        self.designComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.designComboBox.addItems(Constants.DESIGN_MODES)
        self.designComboBox.currentIndexChanged.connect(self.selectionchange)
        self.verticalLayout_2.addWidget(self.designComboBox)
        self.closeAllBtn = QtWidgets.QPushButton(Dialog)
        self.closeAllBtn.setGeometry(QtCore.QRect(270, 210, 111, 41))
        self.createProjectBtn = QtWidgets.QPushButton(Dialog)
        self.createProjectBtn.setGeometry(QtCore.QRect(120, 210, 121, 41))
        self.warningLbl = QtWidgets.QLabel(Dialog)
        self.warningLbl.setGeometry(QtCore.QRect(40, 180, 300, 17))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.closeAllBtn.clicked.connect(self.closeAll)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Create Project", None))
        #self.label_2.setText(_translate("Dialog", "Project Name:", None))
        self.label_5.setText(_translate("Dialog", "Project Directory:", None))
        self.label_3.setText(_translate("Dialog", "Package Name:", None))
        self.label.setText(_translate("Dialog", "Design Type:", None))
        self.closeAllBtn.setText(_translate("Dialog", "Close", None))
        self.createProjectBtn.setText(_translate("Dialog", "Create Project", None))
    
    def closeAll(self):
        exit()

    def selectionchange(self,i):
        1            
        for count in range(self.designComboBox.count()):
            1