from PyQt5 import QtWidgets, QtGui, QtCore

class componentHighlight(QtWidgets.QPushButton):

    def __init__(self, parent, width , height):
        super(componentHighlight, self).__init__(parent)
        self.installEventFilter(self)

        self.setFixedSize(width, height)
        self.setStyleSheet("""background-color:rgba(0,0,0,1);""")

    def eventFilter(self, object, event):

        if event.type() == QtCore.QEvent.MouseButtonPress:
            print ("You pressed the button")
            return True

        elif event.type() == QtCore.QEvent.HoverMove:
            self.setStyleSheet("""background-color:rgba(0,0,0,1);
                   border: 3px solid rgb(0,0,255);""")
            return True
        elif event.type() == QtCore.QEvent.HoverLeave:
            self.setStyleSheet("""background-color:rgba(0,0,0,1)""")
            return True
        return False

