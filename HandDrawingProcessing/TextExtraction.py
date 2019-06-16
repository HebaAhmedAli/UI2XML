from google.cloud import vision

client = vision.ImageAnnotatorClient()
# Extract text from given image or box.
def extractText(content):
    #TODO: (we may need to merge the extracted text before return it)
    textExtracted = []
    txtBoxes=[]
    
    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Ignoring the first element which contains all the text
    for i in range(1, len(texts)):
        text = texts[i]
        # print('\n"{}"'.format(text.description))
        textExtracted.append(text.description)
        # vertices = (['({},{})'.format(vertex.x, vertex.y)
        #             for vertex in text.bounding_poly.vertices])
        vert = []
        for vertex in text.bounding_poly.vertices:
            vert.append((vertex.x,vertex.y))
        x = vert[0][0]
        y = vert[0][1]
        w = abs(x-vert[2][0])
        h = abs(y-vert[2][1])
        txtBoxes.append([x,y,w,h])
    # For testing purpose
    print(textExtracted)
    print(txtBoxes)

    return textExtracted,txtBoxes
    