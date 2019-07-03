from PyQt5 import QtWidgets, QtGui, QtCore

class componentHighlight(QtWidgets.QPushButton):
    showComp = QtCore.pyqtSignal(int, str)
    def __init__(self, parent, scaledCompBox, box, idName, predType, idx):
        super(componentHighlight, self).__init__(parent)
        self.installEventFilter(self)
        self.idName = idName
        self.box = box
        self.index = idx
        self.predicted = predType
        self.changed = False
        errorMargin = 10
        self.setFixedSize(scaledCompBox[2]+errorMargin, scaledCompBox[3]+errorMargin)
        self.move(scaledCompBox[0]+errorMargin, scaledCompBox[1]+errorMargin)

        self.setStyleSheet("""background-color:rgba(0,0,0,0);
        border: 0px solid rgb(0,0,255);""")

    def eventFilter(self, object, event):

        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.showComp.emit(self.index, self.predicted)
            return True

        if event.type() == QtCore.QEvent.HoverMove:
            self.setStyleSheet("""background-color:rgba(0,0,0,0);
                   border: 3px solid rgb(0,0,255);""")
            return True
        elif event.type() == QtCore.QEvent.HoverLeave:
            self.setStyleSheet("""background-color:rgba(0,0,0,0);
            border: 0px solid rgb(0,0,255);""")
            return True
        return False

    def changePred(self, newType):
        self.predicted=newType
        self.changed=True