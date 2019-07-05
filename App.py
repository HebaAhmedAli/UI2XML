import sys
import qdarkstyle
from PyQt5.QtWidgets import *
from Main import mainScreen

# create the application and the main window
app = QApplication(sys.argv)
window = mainScreen()
window.showMaximized()


# setup stylesheet
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

# run
window.show()
app.exec_()