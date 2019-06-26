#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import qdarkstyle
from PyQt5.QtWidgets import *
from main import mainScreen

# create the application and the main window
app = QApplication(sys.argv)
window = mainScreen()

# setup stylesheet
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

# run
window.show()
app.exec_()

