from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import GUI.skelMainScreen as skelMainscreen
import GUI.uploadWindow as uploadWindow
from GUI.createProjDialog import createProjectDialog
import  GUI.prevWindow as prevWindow
import  GUI.utils as utils
# from keras.models import load_model
# import ScreenShots
# import HandDrawing
# import Psd
# import LoadDataClassification
import Constants


class mainScreen(QMainWindow, skelMainscreen.Ui_mainWindow):
    def __init__(self):
        super(mainScreen, self).__init__()
        self.state = "INS_PIC"
        self.setupUi(self)
        self.startUp()
        self.createUploadUI()
        self.actionGenerateXML.triggered.connect(self.processImagesAccToMode)
        self.actionUpdateCmpts.triggered.connect(self.regenerateXMLafterCorrection)

    def createUploadUI(self):
        self.uploadWidget = uploadWindow.uploadWindow()
        self.lay = QHBoxLayout()
        self.centralwidget.setLayout(self.lay)
        self.lay.addLayout(self.uploadWidget.layoutScroll)
        # self.lay.addDockWidget(Qt.DockWidgetArea(2), self.uploadWidget.dockDesign)
    
    def startUp(self):
        Constants.MONITOR_WIDTH, Constants.MONITOR_HEIGHT = utils.getScreenDims()
        self.mainDialoge = createProjectDialog()
        self.mainDialoge.show()
        self.mainDialoge.activateWindow()
        self.mainDialoge.createProjectBtn.clicked.connect(self.enableRun)

    def enableRun(self):
        self.actionGenerateXML.setEnabled(True)

    def processImagesAccToMode(self):
        del self.mainDialoge
        self.uploadWidget.populateProjDir()
        self.actionGenerateXML.setEnabled(False)
        self.actionUpdateCmpts.setEnabled(True)
        self.prev = prevWindow.previewWindow(self)
        del self.uploadWidget.layoutScroll
        del self.uploadWidget
        self.lay.addLayout(self.prev.mainHLayout)
        return
        if Constants.designMode == Constants.DESIGN_MODES[0]:
            vocab,invVocab = LoadDataClassification.loadVocab('data/vocab_classification.txt')
            model = load_model('data/ourModel/UI2XMLclassification245000_98_91.h5') # 150 * 150
            ScreenShots.processAllImages(Constants.imagesPath,model,invVocab)
        elif Constants.designMode == Constants.DESIGN_MODES[1]:
            HandDrawing.processAllImages(Constants.imagesPath)
        '''
        else:    # TODO : Call psd.
        '''

    def regenerateXMLafterCorrection(self):
        updatedMap = self.prev.generateUpdatedXML()
        # self.prev.mainHLayout.setParent(None)
        # del self.prev.mainHLayout
        # del self.prev
        # self.prev = prevWindow.previewWindow(self)
        # self.actionConnectCmpts.setEnabled(True)