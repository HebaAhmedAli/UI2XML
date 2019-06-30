# Constants
BATCH_SIZE = 64
EPOCHS = 5#15
VOCAB_SIZE_CLASSIFICATION =  16
IMAGE_SIZE_CLASSIFICATION = 150
DIRECTORY = 'data/ScreenShots/output'
ID = 0
PACKAGE = ''
PROJECT_NAME = "gp"
DEBUG_MODE = True
HAND_DRAWN = False
DYNAMIC = True
DESIGN_MODES = ("Screenshots", "Hand Darwing",  "PSD File")
IMG_EXTN = ("jpg", "jpeg", "png")
MODEL_PRED = ("CheckBox","CheckedTextView","EditText","ImageButton","NumberPicker",
            "ProgressBarHorizontal","ProgressBarVertical","RadioButton","RatingBar","SeekBar",
            "Spinner","Switch","ToggleButton","ImageView","Button","TextView",)

# Globals
boxToGui = []
predictedToGui = []
idToGui = []
xmlFilesToGui = []
mapToGui = {}
imagesPath = ""
designMode = DESIGN_MODES[0]
