from PyQt4.QtCore import *
from PyQt4.QtGui import *

class delButton(QPushButton):
    def __init__(self, parent):
        super(delButton, self).__init__(parent)
        self.setText("Delete me!")
        self.clicked.connect(self.deleteImageBox)
    def deleteImageBox(self):
        print("iam deleting")
        self.parent.setParent(None)


