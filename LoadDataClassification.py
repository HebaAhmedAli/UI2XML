import Preprocessing
import numpy as np
from keras.utils import to_categorical
import cv2
import os
import pytesseract as pt
from keras.preprocessing import image
import Utils

# For Features.

# Extract text from given image or box.
def isText(img):
    textExtracted=""
    #TODO: (we may need to merge the extracted text before return it)
    textExtracted = pt.image_to_string(img)
    if textExtracted == "":
      return 0
    else:
      return 1


# Extract boxes from given image.
def extractShapeFeatures(img,resizedImg):
    allShapeFeatures = []
    edges,_=Preprocessing.preProcessEdges(img)
    edgesResized,grayImgResized = Preprocessing.preProcessEdges(resizedImg)
    # normalizedNoOfEdges, normalizedNoOfLines, maxHorzLineLength/150, noOfSlopedLines/noOfLines
    allShapeFeatures += Utils.getLinesEdgesFeatures(edgesResized)
    # widthResizingRatio, hightResizingRatio
    allShapeFeatures += Utils.getResizeRatios(img)
    # LBP hist, HOG hist(hist of gradients 8 directions), 5 gray hist range.
    allShapeFeatures += Utils.describeLBP(grayImgResized)
    allShapeFeatures += Utils.descripeHog(grayImgResized)
    allShapeFeatures += Utils.describe5Gray(grayImgResized)
    (_, contours , _) = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    if len(contours) == 0:
      print("noContors: ")
      return [0,0,0,0,0,0]
    cnt = max(contours, key = cv2.contourArea)
    # ifSquare, circularity, noOfVerNormalized, areaCntRatio, perCntRatio, aspectRatio
    allShapeFeatures += Utils.detectShapeAndFeature(cnt)
    return allShapeFeatures
  
def imageReadColors(imgPath=None):
    img = image.load_img(imgPath)
    img = np.array(img,dtype='float32')  
    return img

def loadVocab(vocabPath):
    keyStrings=set()
    with open(vocabPath, "r") as ins:
        for line in ins:
            keyStrings.update([line[:-1]])
    invVocab = dict(enumerate(sorted(keyStrings)))
    vocab = {v:k for k,v in invVocab.items()}
    print("vocabulary length = "+str(len(vocab)))
    print("inv vocabulary length = "+str(len(invVocab)))
    return vocab, invVocab

def loadData(imagesPath,vocab,start,end):
    root,directories,files=next(os.walk(imagesPath))
    Y=[]
    X=[]
    auxFeatures=[]
    i=0
    for file in files:
        if i>=start and i<end:
            feature=[]
            index=file.find('-')
            y=file[index+1:-4]
            x=Preprocessing.imageReadAndPreprocessingClassification(imagesPath+file)
            xColors=imageReadColors(imagesPath+file)
            xShapesAndText = cv2.imread(imagesPath+file)
            try:
              resizedImg = cv2.resize(xShapesAndText, (150,150))
            except Exception as e:
              continue
            X.append(x)
            Y.append(to_categorical(vocab[y], num_classes=len(vocab)))
            xColors=imageReadColors(imagesPath+file)
            xShapesAndText = cv2.imread(imagesPath+file)
            feature+=Utils.getNoOfColorsAndBackGroundRGB(xColors)
            feature.append(isText(xShapesAndText))
            feature+=extractShapeFeatures(xShapesAndText,resizedImg)
            auxFeatures.append(np.array(feature,dtype='float32'))
        elif i>= end:
            break
        i+=1
    print("X shape = "+str(np.array(X).shape))
    print("Y shape = "+str(np.array(Y).shape))
    return np.array(X), np.array(Y), np.array(auxFeatures)
