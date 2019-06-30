# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import sys
sys.path.append('../')
from PyQt5 import QtCore, QtWidgets, QtWidgets
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

class skelChangeCompPred(object):
    def setupUi(self, Dialog):

        Dialog.resize(400, 150)
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 20, 160, 50))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.compTypeLbl = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.verticalLayout.addWidget(self.compTypeLbl)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(160, 20, 220, 50))
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.compTypeComboBox = QtWidgets.QComboBox(self.verticalLayoutWidget_2)
        self.compTypeComboBox.addItems(Constants.MODEL_PRED)
        self.verticalLayout_2.addWidget(self.compTypeComboBox)
        self.updateBtn = QtWidgets.QPushButton(Dialog)
        self.updateBtn.setGeometry(QtCore.QRect(100, 100, 150, 41))
        self.closeAllBtn = QtWidgets.QPushButton(Dialog)
        self.closeAllBtn.setGeometry(QtCore.QRect(270, 100, 111, 41))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.compTypeLbl.setText(_translate("Dialog", "Component Name:", None))
        self.closeAllBtn.setText(_translate("Dialog", "Close", None))
        self.updateBtn.setText(_translate("Dialog", "Update Component", None))

class correctPredDialog(QtWidgets.QWidget, skelChangeCompPred):
    opa = QtCore.pyqtSignal(str)
    def __init__(self):
        super(correctPredDialog, self).__init__()
        self.setupUi(self)
        self.closeAllBtn.clicked.connect(self.closeAll)
        self.updateBtn.clicked.connect(self.changePred)


    def closeAll(self):
        self.close()

    def changePred(self):
        # get the combobox
        # print(self.compTypeComboBox.currentText())
        self.opa.emit(self.compTypeComboBox.currentText())
        self.close()