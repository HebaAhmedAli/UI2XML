# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import createDialog 

class createProjectDialog(QDialog, createDialog.Ui_Dialog):
    started = pyqtSignal(list)

    def __init__(self):
        super(createProjectDialog, self).__init__()
        self.setupUi(self)
        self.activateWindow()

    def startProject(self):
        projCreationDetails = []
        if(len(str(self.projectNameLine.text()).strip())==0):
            self.warningLbl.setText("Insert Project Name, please!")
            return
        if(len(str(self.packageNameLine.text()).strip())==0):
            self.warningLbl.setText("Insert Package Name, please!")
            return
        if(len(str(self.projectDirectoryL.text()).strip())==0):
            self.warningLbl.setText("Insert project Directory, please!")
            return
        projCreationDetails.append(str(self.projectNameLine.text()).strip())
        projCreationDetails.append(str(self.packageNameLine.text()).strip())
        projCreationDetails.append(str(self.designComboBox.currentText()))
        projCreationDetails.append(str(self.projectDirectoryL.curDir))
        self.started.emit(projCreationDetails)