import sys
sys.path.append('../')
import BoxesExtraction as BoxesExtraction
import TextExtraction as TextExtraction

# Extract the boxes and text from given image -extracted comonents-.
def extractComponents(image):
    extratctedBoxes=BoxesExtraction.extractBoxes(image)
    extractedText=[] # List of strings coreesponding to the text in each box.
     # Note: If the box doesn't contain text its index in the extractedText list should contains empty string.
    for i in range(len(extratctedBoxes)):
        extractedText+=TextExtraction.extractText(image)
    return extratctedBoxes,extractedText
