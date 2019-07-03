import sys
sys.path.append('../')
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.skelCreateProjDialog as skelCreateProjDialog
import GUI.utils as utils
import os
import Constants
import shutil

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
        '''
        if(len(str(self.projectNameLine.text()).strip())==0):
            self.warningLbl.setText("Insert Project Name, please!")
            return
        '''
        if(len(str(self.projectDirectoryL.text()).strip())==0):
            self.warningLbl.setText("Insert project Directory, please!")
            return
        if(not os.path.exists(self.projectDirectoryL.text())):
            self.warningLbl.setText("Insert correct project Directory, please!")
            return
        directory = str(self.projectDirectoryL.curDir)
        Constants.PROJECT_NAME = directory.split('/')[-1]
        if os.path.exists(directory+'/temp'):
            shutil.rmtree(directory+'/temp')
            os.makedirs(directory+'/temp')
        else:
            os.makedirs(directory+'/temp')
        Constants.imagesPath = directory+'/temp'
        Constants.PACKAGE = str(self.packageNameLine.text()).strip()
        Constants.designMode = str(self.designComboBox.currentText())
        self.close()