# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import os

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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(400, 274)
        self.verticalLayoutWidget = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 20, 160, 161))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.label_5 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.verticalLayoutWidget_2 = QtGui.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(130, 20, 221, 161))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.projectNameLine = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.projectNameLine.setObjectName(_fromUtf8("projectNameLine"))
        self.verticalLayout_2.addWidget(self.projectNameLine)
        self.packageNameLine = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.packageNameLine.setObjectName(_fromUtf8("lineEdit"))
        self.verticalLayout_2.addWidget(self.packageNameLine)
        self.projectDirectoryL = ClickableLineEdit(self.verticalLayoutWidget_2)
        self.projectDirectoryL.setObjectName(_fromUtf8("projectDirectoryL"))
        # self.projectDirectoryL.mousePressEvent.connect(self.clearAndChooseDir)
        self.verticalLayout_2.addWidget(self.projectDirectoryL)
        self.designComboBox = QtGui.QComboBox(self.verticalLayoutWidget_2)
        self.designComboBox.setObjectName(_fromUtf8("comboBox"))
        designModes = ("Hand Darwing", "Screenshot", "PSD File")
        self.designComboBox.addItems(designModes)
        self.designComboBox.currentIndexChanged.connect(self.selectionchange)
        self.verticalLayout_2.addWidget(self.designComboBox)
        self.closeAllBtn = QtGui.QPushButton(Dialog)
        self.closeAllBtn.setGeometry(QtCore.QRect(270, 210, 111, 41))
        self.closeAllBtn.setObjectName(_fromUtf8("closeAllBtn"))
        self.createProjectBtn = QtGui.QPushButton(Dialog)
        self.createProjectBtn.setGeometry(QtCore.QRect(120, 210, 121, 41))
        self.createProjectBtn.setObjectName(_fromUtf8("createProjectBtn"))
        self.warningLbl = QtGui.QLabel(Dialog)
        self.warningLbl.setGeometry(QtCore.QRect(40, 180, 300, 17))
        self.warningLbl.setText("")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.closeAllBtn.clicked.connect(self.closeAll)
        self.createProjectBtn.clicked.connect(self.startProject)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label_2.setText(_translate("Dialog", "Project Name:", None))
        self.label_5.setText(_translate("Dialog", "Project Directory:", None))
        self.label_3.setText(_translate("Dialog", "Package Name:", None))
        self.label.setText(_translate("Dialog", "Design Type", None))
        self.closeAllBtn.setText(_translate("Dialog", "Close", None))
        self.createProjectBtn.setText(_translate("Dialog", "Create Project", None))
    
    def closeAll(self):
        exit()

    def selectionchange(self,i):
        print("Items in the list are :")
            
        for count in range(self.designComboBox.count()):
            print(self.designComboBox.itemText(count))
        print("Current index",i,"selection changed ",self.designComboBox.currentText())
    
class ClickableLineEdit(QtGui.QLineEdit):
    
    # clicked = QtCore.Signal()

    def mousePressEvent(self, event):
        super(ClickableLineEdit, self).mousePressEvent(event)
        self.clearAndChooseDir()
        # self.clicked.emit()

    def clearAndChooseDir(self):
        self.setText("")
        path = os.path.dirname(os.path.realpath(__file__))
        file_path = str(QtGui.QFileDialog.getExistingDirectory(self, 
                    caption='Select Directory', directory=path,
                    options=QtGui.QFileDialog.ShowDirsOnly))
        self.setText(file_path)
        self.curDir = file_path
 