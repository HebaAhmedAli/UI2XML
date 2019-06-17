from PyQt4.QtCore import *
from PyQt4.QtGui import *
from mainScreen import mainScreen
import sys

app = QApplication(sys.argv)
dialog = mainScreen()
dialog.show()
sys.exit(app.exec_())