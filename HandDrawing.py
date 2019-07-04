import HandDrawingMode.ComponentsExtraction as ComponentsExtraction
from keras.preprocessing import image
import CodeGeneration.XmlGeneration as XmlGeneration
import numpy as np
import Constants
import cv2
import os
import copy
import Utils
import io
from PIL import Image
import time

def processImage(subdir, file):
    xImage = np.array(Utils.genTable(300,300))
    if not os.path.exists(Constants.DIRECTORY+'/res/drawable'):
        os.makedirs(Constants.DIRECTORY+'/res/drawable')
    Image.fromarray(xImage.astype(np.uint8)).save(Constants.DIRECTORY+'/res/drawable/'+"pic_x.png")
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
    if file[len(file)-5] == 'D':
        Constants.DYNAMIC=True
    else:
        Constants.DYNAMIC=False
    parentNodesForGui = XmlGeneration.generateXml(boxesTranslated,texts,predictedComponents,myImage,file[:-6],file[len(file)-6])
    # Translate x and y and handle outside range.
    for i in range(len(Constants.boxToGui)):
        Constants.boxToGui[i] = [Constants.boxToGui[i][0]+myImageBox[0],Constants.boxToGui[i][1]+myImageBox[1],Constants.boxToGui[i][2],Constants.boxToGui[i][3]]
            
    Constants.mapToGui.update( {file :[Constants.boxToGui,Constants.idToGui,Constants.predictedToGui,Constants.xmlFilesToGui,Constants.inWhichFile,parentNodesForGui]})
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
            crop_img = imgCopy[max(0,y):min(height,y + h), max(x,0):min(width,x + w )]
            #cv2.imwrite(subdir + "/compOutputs"+file[:-4]+'/'+str(j) + str(file[len(file)-4:len(file)]),crop_img)
            cv2.imwrite(subdir + "/compOutputs"+file[:-4]+'/'+str(j)+'-'+ predictedComponents[j] + str(file[len(file)-4:len(file)]),crop_img)
            fTo.write(str(j)+'- '+texts[j]+'\n')
            j+=1
        cv2.imwrite(subdir+"/boxOutputs/"+file,img)

def updateImage(subdir,file,valMapFromGui):
    imgXML = image.load_img(subdir+'/' +file)
    imgXML = np.array(imgXML,dtype='float32')  
    file = file.replace('.jpeg','.jpg')  
    if file[len(file)-5] == 'D':
        Constants.DYNAMIC=True
    else:
        Constants.DYNAMIC=False
    parentNodesForGui = XmlGeneration.updateXml(valMapFromGui[3],valMapFromGui[0],valMapFromGui[2],valMapFromGui[1],imgXML,file[:-6],file[len(file)-6])
    Constants.mapToGui.update( {file : [Constants.boxToGui,Constants.idToGui,Constants.predictedToGui,Constants.xmlFilesToGui,Constants.inWhichFile,parentNodesForGui]})


def processAllImages(imagesPath):
    startTime = time.time()
    Constants.HAND_DRAWN = True
    Constants.DIRECTORY = imagesPath[:-5] + Constants.androidPath
    Constants.mapToGui = {}
    _,_, files= next(os.walk(imagesPath))
    for file in files:
        imgPath = os.path.join(imagesPath, file)
        if (".png" in imgPath or ".jpeg" in imgPath or ".jpg" in imgPath) and ('._' not in imgPath):
            processImage(imagesPath, file)
    print("Total time = ",time.time()-startTime)

def updateAllImages(imagesPath,mapUpdatedFromGui):
    Constants.HAND_DRAWN = True
    Constants.mapToGui = {}
    for (key, val) in mapUpdatedFromGui.items(): 
        imgPath = os.path.join(imagesPath, key)
        if (".png" in imgPath or ".jpeg" in imgPath or ".jpg" in imgPath) and ('._' not in imgPath):
            updateImage(imagesPath, key,val)

'''
imagesPath='data/HandDrawn/ourTest'
Constants.HAND_DRAWN = True
processAllImages(imagesPath)
'''