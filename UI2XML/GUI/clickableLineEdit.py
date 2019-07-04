from PyQt5 import QtCore, QtGui, QtWidgets
import os    

class clickableLineEdit(QtWidgets.QLineEdit):
    
    def __init__(self,parent):
        super(clickableLineEdit, self).__init__(parent)

    def mousePressEvent(self, event):
        super(clickableLineEdit, self).mousePressEvent(event)
        self.clearAndChooseDir()
        # self.clicked.emit()

    def clearAndChooseDir(self):
        self.setText("")
        path = os.path.dirname(os.path.realpath(__file__))
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_path = str(QtWidgets.QFileDialog.getExistingDirectory(self, 
                    caption='Select Directory', directory=path,
                    options=options))
        self.setText(file_path)
        self.curDir = file_path
 