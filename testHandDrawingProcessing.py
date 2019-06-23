import HandDrawingProcessing.ComponentsExtraction as ComponentsExtraction
from keras.preprocessing import image
import XmlGeneration.XmlGeneration as XmlGeneration
import numpy as np
import Constants
import cv2
import os
import copy
import Utils
import io
from PIL import Image

imagesPath='data/HandDrawn'

def processSave(subdir, file):
    Constants.DIRECTORY = 'data/HandDrawn/output'
    Constants.HAND_DRAWN = True
    xImage = np.array(Utils.genTable(300,300))
    Image.fromarray(xImage.astype(np.uint8)).save(Constants.DIRECTORY+'/drawable/'+"pic_x.png")
    if not os.path.exists(Constants.DIRECTORY):
        os.makedirs(Constants.DIRECTORY)
    path = subdir+'/' +file
    img = cv2.imread(path)
    imgCopy = copy.copy(img)
    imgXML = image.load_img(subdir+'/' +file)
    imgXML = np.array(imgXML,dtype='float32')
    with io.open(path, 'rb') as image_file:
        img4Txt = image_file.read()
    file = file.replace('.jpeg','.jpg')
    # TODO: Remove last parameter after testing.
    boxes, boxesTranslated, texts, predictedComponents,myImageBox = ComponentsExtraction.extractComponents(img,imgCopy,img4Txt,file)
    myImage = imgXML[myImageBox[1]:myImageBox[1]+myImageBox[3]+1,myImageBox[0]:myImageBox[0]+myImageBox[2]+1]
    XmlGeneration.generateXml(boxesTranslated,texts,predictedComponents,myImage,file[:-5],file[len(file)-5])
    margin = 10
    if Constants.DEBUG_MODE == True :
        
        if not os.path.exists(subdir+'/compOutputs'+file[:-4]):
            os.makedirs(subdir+'/compOutputs'+file[:-4])
        if not os.path.exists(subdir+'/boxOutputs'):
            os.makedirs(subdir+'/boxOutputs')
    height= img.shape[0]
    width= img.shape[1]
    if Constants.DEBUG_MODE == True :
        j = 0
        fTo=open(subdir+'/compOutputs'+file[:-4]+'/texts.txt', 'w+')
        for x,y,w,h in boxes:
            # testing: print the cropped in folder
            crop_img = imgCopy[max(0,y - margin):min(height,y + h + margin), max(x - margin,0):min(width,x + w + margin)]
            #cv2.imwrite(subdir + "/compOutputs"+file[:-4]+'/'+str(j) + str(file[len(file)-4:len(file)]),crop_img)
            cv2.imwrite(subdir + "/compOutputs"+file[:-4]+'/'+str(j)+'-'+ predictedComponents[j] + str(file[len(file)-4:len(file)]),crop_img)
            fTo.write(str(j)+'- '+texts[j]+'\n')
            j+=1
        cv2.imwrite(subdir+"/boxOutputs/"+file,img)

subdir, dirs, _= next(os.walk(imagesPath))
for direc in dirs:
    _,_, files= next(os.walk(subdir+'/'+direc))
    for file in files:
        imgPath = os.path.join(subdir, file)
        if (".png" in imgPath or ".jpeg" in imgPath or ".jpg" in imgPath) and ('._' not in imgPath):
            processSave(subdir+'/'+direc, file)
