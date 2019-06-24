#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from main import mainScreen
import sys

app = QApplication(sys.argv)
screen_resolution = app.desktop().screenGeometry()
width, height = screen_resolution.width(), screen_resolution.height()

dialog = mainScreen(width, height)
dialog.show()
sys.exit(app.exec_())

