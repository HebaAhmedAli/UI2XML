from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.skelMainScreen as skelMainscreen
import GUI.uploadWindow as uploadWindow
from GUI.createProjDialog import createProjectDialog
import  GUI.prevWindow as prevWindow
import  GUI.utils as utils
from keras.models import load_model
import ScreenShots
import HandDrawing
import Psd
import LoadDataClassification
import Constants
import CodeGeneration.SwitchingActivities as SwitchingActivities
import subprocess
import os
import signal

class mainScreen(QMainWindow, skelMainscreen.Ui_mainWindow):
    def __init__(self):
        super(mainScreen, self).__init__()
        self.state = "INS_PIC"
        self.setupUi(self)
        self.startUp()
        self.createUploadUI()
        self.actionGenerateXML.triggered.connect(self.processImagesAccToMode)
        self.actionUpdateCmpts.triggered.connect(self.regenerateXMLafterCorrection)
        self.actionConnectCmpts.triggered.connect(self.connectComponents)
        self.actionFinish.triggered.connect(self.connectActivitiesResult)
        self.actionExit.triggered.connect(self.endProg)


    def createUploadUI(self):
        self.uploadWidget = uploadWindow.uploadWindow()
        self.lay = QHBoxLayout()
        self.centralwidget.setLayout(self.lay)
        self.lay.addLayout(self.uploadWidget.layoutScroll)
    
    def startUp(self):
        Constants.MONITOR_WIDTH, Constants.MONITOR_HEIGHT = utils.getScreenDims()
        self.mainDialoge = createProjectDialog()
        self.mainDialoge.show()
        self.mainDialoge.activateWindow()
        self.mainDialoge.createProjectBtn.clicked.connect(self.enableRun)
        self.statusbar.clearMessage()
        self.statusbar.showMessage("Choose the Android Studio project you already created")

    def enableRun(self):
        self.actionGenerateXML.setEnabled(True)
        self.statusbar.clearMessage()
        self.statusbar.showMessage("Drag and Drop or Click to upload your "+ Constants.designMode+ " Files")

    def processImagesAccToMode(self):
        error = self.uploadWidget.populateProjDir() 
        if error==-1:
            return
        proc = subprocess.Popen(args = ["python3", "GUI/modelLoading.py"])
        print(proc.pid)
        self.actionGenerateXML.setEnabled(False)
        self.actionUpdateCmpts.setEnabled(True)
        if Constants.designMode == Constants.DESIGN_MODES[0]:
             vocab, invVocab = LoadDataClassification.loadVocab('data/vocab_classification.txt')
             model = load_model('data/ourModel/' + Constants.MODEL_NAME)  # 150 * 150
             ScreenShots.processAllImages(Constants.imagesPath, model, invVocab)
        elif Constants.designMode == Constants.DESIGN_MODES[1]:
             HandDrawing.processAllImages(Constants.imagesPath)
        else:
             vocab, invVocab = LoadDataClassification.loadVocab('data/vocab_classification.txt')
             model = load_model('data/ourModel/' + Constants.MODEL_NAME)  # 150 * 150
             Psd.processAllPsds(Constants.imagesPath, model, invVocab)
        self.statusbar.clearMessage()
        os.kill(proc.pid, signal.SIGTERM)
        self.statusbar.showMessage("Click on component to know/change its type")
        self.prev = prevWindow.previewWindow(self)
        self.lay.addLayout(self.prev.mainHLayout)
        self.actionConnectCmpts.setEnabled(True)

    def regenerateXMLafterCorrection(self):
        self.statusbar.clearMessage()
        self.statusbar.showMessage("Continue Updating types or Connect Activities")
        updatedMap = self.prev.generateUpdatedXML()
        self.actionConnectCmpts.setEnabled(True)
        if Constants.designMode == Constants.DESIGN_MODES[0]:
            ScreenShots.updateAllImages(Constants.imagesPath,updatedMap)
        elif Constants.designMode == Constants.DESIGN_MODES[1]:
            HandDrawing.updateAllImages(Constants.imagesPath,updatedMap)
        else:
            Psd.updateAllImages(Constants.imagesPath,updatedMap)
        self.prev.refreshWindowAfterUpdate()

    def connectComponents(self):
        self.statusbar.showMessage("Choose buttons or image buttons connecting between activities")
        self.actionUpdateCmpts.setEnabled(False)
        self.actionConnectCmpts.setEnabled(False)
        self.actionFinish.setEnabled(True)
        self.prev.connectCmptsStart()
        self.state = "ConnectCmpts"

    def connectActivitiesResult(self):
        self.actionFinish.setEnabled(False)
        connectedMap = self.prev.convertConnectMapToLists()
        SwitchingActivities.switchActivities(connectedMap)
        print("MAP", connectedMap)
        self.close()

    def endProg(self):
        exit()