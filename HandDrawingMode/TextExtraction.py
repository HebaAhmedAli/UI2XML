import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="../UI2XML/data/UI2XML-f9d1f0273970.json"

from google.cloud import vision

client = vision.ImageAnnotatorClient()
# Extract text from given image or box.
def extractText(content):
    textExtracted = []
    txtBoxes=[]
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    # Ignoring the first element which contains all the text
    for i in range(1, len(texts)):
        text = texts[i]
        textExtracted.append(text.description)
        vert = []
        for vertex in text.bounding_poly.vertices:
            vert.append((vertex.x,vertex.y))
        x = vert[0][0]
        y = vert[0][1]
        w = abs(x-vert[2][0])
        h = abs(y-vert[2][1])
        txtBoxes.append([x,y,w,h])
    return textExtracted,txtBoxes


    