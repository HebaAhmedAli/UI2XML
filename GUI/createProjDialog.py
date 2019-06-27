from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.skelCreateProjDialog as skelCreateProjDialog
import GUI.utils as utils
import os

class createProjectDialog(QDialog, skelCreateProjDialog.Ui_Dialog):

    def __init__(self):
        super(createProjectDialog, self).__init__()
        self.setupUi(self)
        self.activateWindow()
        path = os.path.dirname(os.path.realpath(__file__))
        self.projectDirectoryL.setText(str(path))
        self.projectDirectoryL.curDir = path
        self.createProjectBtn.clicked.connect(self.startProject)

    def startProject(self):
        if(len(str(self.projectNameLine.text()).strip())==0):
            self.warningLbl.setText("Insert Project Name, please!")
            return
        if(len(str(self.packageNameLine.text()).strip())==0):
            self.warningLbl.setText("Insert Package Name, please!")
            return
        if(len(str(self.projectDirectoryL.text()).strip())==0):
            self.warningLbl.setText("Insert project Directory, please!")
            return
        if(not os.path.exists(self.projectDirectoryL.text())):
            self.warningLbl.setText("Insert correct project Directory, please!")
            return
        utils.projCreationDetails.append(str(self.projectNameLine.text()).strip())
        utils.projCreationDetails.append(str(self.packageNameLine.text()).strip())
        utils.projCreationDetails.append(str(self.designComboBox.currentText()))
        utils.projCreationDetails.append(str(self.projectDirectoryL.curDir))
        print("Project Creation Details: ")
        print(utils.projCreationDetails)
        self.close()