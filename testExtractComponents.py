import ComponentsExtraction.ComponentsExtraction as ComponentsExtraction
import ModelClassification.Model as Model
import LoadDataClassification
import numpy as np


vocab,invVocab = LoadDataClassification.loadVocab('data/vocab_classification.txt')

imagesPath='data/ScreenShots'

# TODO: Loop on the wanted images and call this function on.
# Take the loop that loops on the folders.
image=[] # TODO: Contains the image.
ComponentsExtraction.extractComponents(image)
imagePath=""
Model.makeAprediction(invVocab,'data/SampleData/1-android.widget.RadioButton.png')