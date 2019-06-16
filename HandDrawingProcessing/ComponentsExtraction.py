import sys
sys.path.append('../')
import HandDrawingProcessing.BoxesExtraction as BoxesExtraction
import HandDrawingProcessing.TextExtraction as TextExtraction

# Extract the boxes and text from given image -extracted components-.
def extractComponents(image,image4Txt):
    # TODO: Uncomment after testing and comment the lines after this.
    #extractedText, textPositions= TextExtraction.extractText(image4Txt) # List of strings coreesponding to the text in each box.
    extractedText = []
    textPositions = []
    extratctedBoxes = BoxesExtraction.extractBoxes(image, extractedText, textPositions)
    predictedComonents = ["" for i in range(len((extratctedBoxes)))] # TODO: Get this.
    return extratctedBoxes,extractedText,predictedComonents
