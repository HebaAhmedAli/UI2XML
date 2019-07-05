# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modelLoading.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import qdarkstyle

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(140, 140, 231, 51))
        Dialog.setStyleSheet("""background-color:#515781;""")
        
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(240, 180, 600, 70))
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self._gif = QtWidgets.QLabel(Dialog)
        movie = QtGui.QMovie("Resources/Images/load.gif")
        self._gif.setMovie(movie)
        self._gif.move(400, 300)
        movie.start()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Generating Code"))
        self.label.setText(_translate("Dialog", "Please Wait!"))
        self.label_2.setText(_translate("Dialog", "We are generating your Code :D"))

class loading(QtWidgets.QDialog,Ui_Dialog):
    def __init__(self):
        super(loading, self).__init__()
        self.setupUi(self)

app = QtWidgets.QApplication(sys.argv)
window = loading()
window.showMaximized()

# setup stylesheet
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

# run
window.show()
app.exec_()