from PyQt4.QtCore import *
from PyQt4.QtGui import *

class delButton(QPushButton):
    delete = pyqtSignal(int)
    def __init__(self, parent, imageIndex):
        super(delButton, self).__init__(parent)
        self.setText("Delete me!")
        self.index = imageIndex
        self.clicked.connect(self.deleteImageBox)

    def deleteImageBox(self):
        print("iam deleting")
        self.delete.emit(self.index)
        self.parent.setParent(None)

class convertButton(QPushButton):
    def __init__(self, parent):
        super(convertButton, self).__init__(parent)
        self.setText("Viola!")
        self.clicked.connect(self.convertToXML)

    def convertToXML(self):
        print("iam converting")
        self.parent.setParent(None)


