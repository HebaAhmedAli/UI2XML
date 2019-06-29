# Constants
BATCH_SIZE = 64
EPOCHS = 5#15
VOCAB_SIZE_CLASSIFICATION =  16
IMAGE_SIZE_CLASSIFICATION = 150
DIRECTORY = 'data/ScreenShots/ourTest/output'
ID = 0
PACKAGE = ''
PROJECT_NAME = "gp"
DEBUG_MODE = True
HAND_DRAWN = False
featureSize = 286
DYNAMIC = True
DESIGN_MODES = ("Screenshots", "Hand Darwing",  "PSD File")
IMG_EXTN = ("jpg", "jpeg", "png")
MODEL_NAME = 'UI2XMLclassificationAllFeaturesAC_98_92.h5'

# Globals
boxToGui = []
predictedToGui = []
idToGui = []
xmlFilesToGui = []
mapToGui = {}
imagesPath = ""
designMode = DESIGN_MODES[0]
noContors = 0
listId = 0
noOfLayouts = 0
myParentColor = ""
