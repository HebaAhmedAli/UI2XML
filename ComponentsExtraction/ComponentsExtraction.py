import sys
sys.path.append('../')
import ComponentsExtraction.BoxesExtraction as BoxesExtraction
import ComponentsExtraction.TextExtraction as TextExtraction

# Extract the boxes and text from given image -extracted comonents-.
def extractComponents(image, imageDir):
    extratctedBoxes=BoxesExtraction.extractBoxes(image), imageDir
    extractedText=[] # List of strings coreesponding to the text in each box.
     # Note: If the box doesn't contain text its index in the extractedText list should contains empty string.
    for i in range(len(extratctedBoxes)):
        extractedText+=TextExtraction.extractText(image)
    return extratctedBoxes,extractedText
