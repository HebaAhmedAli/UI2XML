import pytesseract as pt

# Extract text from given image or box.
def extractText(croppedImage):
    textExtracted=""
    #TODO: (we may need to merge the extracted text before return it)
    textExtracted = pt.image_to_string(croppedImage)
    return textExtracted
    