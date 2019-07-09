# Constants
BATCH_SIZE = 64
EPOCHS = 5#15
VOCAB_SIZE_CLASSIFICATION =  16
IMAGE_SIZE_CLASSIFICATION = 150
DIRECTORY = 'data/ScreenShots/ourTest/output'
ICONS_PATH = 'Resources/Images/'

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
MODEL_PRED = ("CheckBox","CheckedTextView","EditText","ImageButton",
              "RadioButton","SeekBar","Switch","ImageView","Button","TextView")
MONITOR_WIDTH = 0
MONITOR_HEIGHT = 0

# Globals
boxToGui = []
predictedToGui = []
idToGui = []
xmlFilesToGui = []
inWhichFile = [] # Contains activity file name, or action bar file name, or list view id.
mapToGui = {}
imagesPath = ""
designMode = DESIGN_MODES[0]
noContors = 0
listId = 0
noOfLayouts = 0
myParentColor = ""
textBrowserWidth = 0.42
androidPath = "/app/src/main"
timeFile=open('time.txt', 'w+')
