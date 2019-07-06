# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'skelFinishDialog.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(742, 356)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 651, 311))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.horizontalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        # self.startProgBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        # self.startProgBtn.setFont(font)
        # # self.startProgBtn.setObjectName("startProgBtn")
        # self.horizontalLayout_3.addWidget(self.startProgBtn)
        self.closeProgBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.closeProgBtn.setFont(font)
        self.closeProgBtn.setObjectName("closeProgBtn")
        self.horizontalLayout_3.addWidget(self.closeProgBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Congratulation!\n"
"          You have successfully generated \n"
"               your project starter code."))
        # self.startProgBtn.setText(_translate("Dialog", "Start New Project"))
        self.closeProgBtn.setText(_translate("Dialog", "Close Program"))


