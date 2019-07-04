import HandDrawingMode.ComponentsExtraction as ComponentsExtraction
from multiprocessing import Process,Manager
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
    boxToGui=[]
    predictedToGui=[]
    idToGui=[]
    xmlFilesToGui=[]
    inWhichFile=[]
    parentNodesForGui = XmlGeneration.generateXml(boxesTranslated,texts,predictedComponents,myImage,file[:-6],file[len(file)-6],boxToGui=boxToGui,predictedToGui=predictedToGui,idToGui=idToGui,xmlFilesToGui=xmlFilesToGui,inWhichFile=inWhichFile,dynamic=file[len(file)-5] == 'D')
    # Translate x and y and handle outside range.
    for i in range(len(boxToGui)):
        boxToGui[i] = [boxToGui[i][0]+myImageBox[0],boxToGui[i][1]+myImageBox[1],boxToGui[i][2],boxToGui[i][3]]     
    
    Constants.mapToGui.update( {file : [boxToGui,idToGui,predictedToGui,xmlFilesToGui,inWhichFile,parentNodesForGui,myImageBox]})


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


def createProcess(imagesPath, file):
    process = Process(target=processImage, args=(imagesPath, file))
    return process    



def processAllImages(imagesPath):
    startTime = time.time()
    Constants.HAND_DRAWN = True
    Constants.DIRECTORY = imagesPath[:-5] + Constants.androidPath
    manager=Manager()
    # Initialize the vectors of each image with empty vector(this vector is shared between processes)
    Constants.mapToGui=manager.dict()
    processes = []
    _,_, files= next(os.walk(imagesPath))
    for file in files:
        imgPath = os.path.join(imagesPath, file)
        if (".png" in imgPath or ".jpeg" in imgPath or ".jpg" in imgPath) and ('._' not in imgPath):
            process = createProcess(imagesPath, file)
            processes.append(process)
    for p in processes:
        p.start()
    for p in processes:
        p.join()
        p.terminate()
    print("Total time = ",time.time()-startTime)

def updateImage(subdir,file,valMapFromGui):
    imgXML = image.load_img(subdir+'/' +file)
    imgXML = np.array(imgXML,dtype='float32')  
    file = file.replace('.jpeg','.jpg')  
    boxToGui=[]
    predictedToGui=[]
    idToGui=[]
    xmlFilesToGui=[]
    inWhichFile=[]
     # Translate x and y and handle outside range.
    for i in range(len(valMapFromGui[0])):
        valMapFromGui[0][i] = [ valMapFromGui[0][i][0]-valMapFromGui[4][0], valMapFromGui[0][i][1]-valMapFromGui[4][1],valMapFromGui[0][i][2], valMapFromGui[0][i][3]]
    
    parentNodesForGui = XmlGeneration.updateXml(valMapFromGui[3],valMapFromGui[0],valMapFromGui[2],valMapFromGui[1],imgXML,file[:-6],file[len(file)-6],boxToGui=boxToGui,predictedToGui=predictedToGui,idToGui=idToGui,xmlFilesToGui=xmlFilesToGui,inWhichFile=inWhichFile,dynamic=file[len(file)-5] == 'D')
     # Translate x and y and handle outside range.
    for i in range(len(boxToGui)):
        boxToGui[i] = [boxToGui[i][0]+valMapFromGui[4][0],boxToGui[i][1]+valMapFromGui[4][1],boxToGui[i][2],boxToGui[i][3]]     
    
    Constants.mapToGui.update( {file : [boxToGui,idToGui,predictedToGui,xmlFilesToGui,inWhichFile,parentNodesForGui]})


def createUpdateProcess(subdir,file,valMapFromGui):
    process = Process(target=updateImage, args=(subdir,file,valMapFromGui))
    return process    



def updateAllImages(imagesPath,mapUpdatedFromGui):
    Constants.HAND_DRAWN = True
    manager=Manager()
    # Initialize the vectors of each image with empty vector(this vector is shared between processes)
    Constants.mapToGui=manager.dict()
    processes = []
    for (key, val) in mapUpdatedFromGui.items(): 
        imgPath = os.path.join(imagesPath, key)
        if (".png" in imgPath or ".jpeg" in imgPath or ".jpg" in imgPath) and ('._' not in imgPath):
            process = createUpdateProcess(imagesPath,key,val)
            processes.append(process)
    for p in processes:
        p.start()
    for p in processes:
        p.join()
        p.terminate()

'''
imagesPath='data/HandDrawn/ourTest'
Constants.HAND_DRAWN = True
processAllImages(imagesPath)
'''