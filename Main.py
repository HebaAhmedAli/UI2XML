from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.skelMainScreen as skelMainscreen
import GUI.uploadWindow as uploadWindow
from GUI.createProjDialog import createProjectDialog
import  GUI.prevWindow as prevWindow
from keras.models import load_model
import ScreenShots
import HandDrawing
import LoadDataClassification
import Constants

class mainScreen (QMainWindow, skelMainscreen.Ui_mainWindow):
    def __init__(self):
        super(mainScreen, self).__init__()
        self.state = "INS_PIC"
        self.setupUi(self)
        self.startUp()
        self.createUploadUI()
        self.actionRun.triggered.connect(self.processImagesAccToMode)
        #prev = prevWindow.previewWindow()
        #self.centralwidget.setLayout(prev.mainHLayout)
        
    def createUploadUI(self):
        self.uploadWidget = uploadWindow.uploadWindow()
        self.centralwidget.setLayout(self.uploadWidget.layoutScroll)
        self.addDockWidget(Qt.DockWidgetArea(2), self.uploadWidget.dockDesign)
    
    def startUp(self):
        self.mainDialoge = createProjectDialog()
        self.mainDialoge.show()
        self.mainDialoge.activateWindow()

    def processImagesAccToMode(self):
        self.uploadWidget.populateProjDir()
        if Constants.designMode == Constants.DESIGN_MODES[0]:
            vocab,invVocab = LoadDataClassification.loadVocab('data/vocab_classification.txt')
            model = load_model('data/ourModel/'+Constants.MODEL_NAME) # 150 * 150
            ScreenShots.processAllImages(Constants.imagesPath,model,invVocab)
        elif Constants.designMode == Constants.DESIGN_MODES[1]:
            HandDrawing.processAllImages(Constants.imagesPath)
        '''
        else:    # TODO : Call psd.
        '''