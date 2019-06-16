import sys
sys.path.append('../')
import HandDrawingProcessing.BoxesExtraction as BoxesExtraction
import HandDrawingProcessing.TextExtraction as TextExtraction

# Extract the boxes and text from given image -extracted components-.
def extractComponents(image,imageCopy):
    extratctedBoxes=BoxesExtraction.extractBoxes(image)
    extractedText=[] # List of strings coreesponding to the text in each box.
    # Note: If the box doesn't contain text its index in the extractedText list should contains empty string.
    margin = 10
    height=image.shape[0]
    width=image.shape[1]
    for x,y,w,h in extratctedBoxes:
        croppedImage = imageCopy[max(0,y - margin):min(height,y + h + margin), max(x - margin,0):min(width,x + w + margin)]
        extractedText.append(TextExtraction.extractText(croppedImage))
    return extratctedBoxes,extractedText
