import ScreenShotMode.ComponentsExtraction as ComponentsExtraction
import CodeGeneration.XmlGeneration as XmlGeneration
from keras.models import load_model
import LoadDataClassification
import Constants
import cv2
import os
import copy
import numpy as np
from keras.preprocessing import image
import time
import Utils

def processImage(subdir, file,model,invVocab):
    img = cv2.imread(subdir+'/' +file)
    imgCopy = copy.copy(img)
    imgXML = image.load_img(subdir+'/' +file)
    imgXML = np.array(imgXML,dtype='float32')  
    file = file.replace('.jpeg','.jpg')
    boxes, texts ,addedManuallyBool ,predictedComponents = ComponentsExtraction.extractComponentsAndPredict(img,imgCopy,imgXML,model,invVocab)
    margin = 10
    if Constants.DEBUG_MODE == True :
        if not os.path.exists(subdir+'/compOutputsAll'+file[:-4]):
            os.makedirs(subdir+'/compOutputsAll'+file[:-4])
        if not os.path.exists(subdir+'/compOutputs'+file[:-4]):
            os.makedirs(subdir+'/compOutputs'+file[:-4])    
        if not os.path.exists(subdir+'/boxOutputs'):
            os.makedirs(subdir+'/boxOutputs')

    height= img.shape[0]
    width= img.shape[1]
    
    if Constants.DEBUG_MODE == True :
        fTo=open(subdir+'/compOutputsAll'+file[:-4]+'/texts.txt', 'w+')
    boxesFiltered,textsFiltered,predictedComponentsFiltered=ComponentsExtraction.filterComponents(boxes, texts ,addedManuallyBool ,predictedComponents,imgCopy,model,invVocab)
    if file[len(file)-5] == 'D':
        Constants.DYNAMIC=True
    else:
        Constants.DYNAMIC=False
    parentNodesForGui = XmlGeneration.generateXml(boxesFiltered,textsFiltered,predictedComponentsFiltered,imgXML,file[:-6],file[len(file)-6])
    Constants.mapToGui.update( {file : (Constants.boxToGui,Constants.idToGui,Constants.predictedToGui,Constants.xmlFilesToGui,Constants.inWhichFile,parentNodesForGui)})
    #parentNodesForGui = XmlGeneration.updateXml(parentNodesForGui,[[19, 18, 44, 42]],['android.widget.'+"TextView"],['ImageView_0_16_1_0_1'],imgXML,file[:-6],file[len(file)-6])
    if Constants.DEBUG_MODE == True :
        j = 0
        for x,y,w,h in boxes:
            # testing: print the cropped in folder
            crop_img = imgCopy[max(0,y - margin):min(height,y + h + margin), max(x - margin,0):min(width,x + w + margin)]
            cv2.imwrite(subdir + "/compOutputsAll"+file[:-4]+'/'+str(j)+'-'+ predictedComponents[j] + str(file[len(file)-4:len(file)]),crop_img)
            fTo.write(str(j)+'- '+texts[j]+" "+str(boxes[j])+'\n')
            j+=1    
        fTo.close()
        fTo=open(subdir+'/compOutputs'+file[:-4]+'/texts.txt', 'w+')
        j=0
        edit = 0
        for x,y,w,h in boxesFiltered:
            # testing: print the cropped in folder
            '''
            if predictedComponentsFiltered[j] == "android.widget.EditText":
                edit = 10
            else:
                edit = 0
            '''
            crop_img = imgCopy[max(0,y - margin - edit):min(height,y + h + margin), max(x - margin,0):min(width,x + w + margin)]
            cv2.imwrite(subdir + "/compOutputs"+file[:-4]+'/'+str(j)+'-'+ predictedComponentsFiltered[j] + str(file[len(file)-4:len(file)]),crop_img)
            fTo.write(str(j)+'- '+textsFiltered[j]+" "+str(boxesFiltered[j])+'\n')
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
    Constants.mapToGui.update( {file : (Constants.boxToGui,Constants.idToGui,Constants.predictedToGui,Constants.xmlFilesToGui,parentNodesForGui)})
        

def processAllImages(imagesPath,model,invVocab):
    Constants.DIRECTORY = imagesPath[:-5] + Constants.androidPath
    if not os.path.exists(Constants.DIRECTORY):
            os.makedirs(Constants.DIRECTORY)
    Constants.mapToGui = {}
    _,_, files= next(os.walk(imagesPath))
    for file in files:
        imgPath = os.path.join(imagesPath, file)
        if (".png" in imgPath or ".jpeg" in imgPath or ".jpg" in imgPath) and ('._' not in imgPath):
            processImage(imagesPath, file,model,invVocab)

def updateAllImages(imagesPath,mapUpdatedFromGui):
    # TODO: Comment after testing.
    mapUpdatedFromGui = {"drND.png":([[36, 315, 128, 88]],['ImageView_0_2_0'],['android.widget.'+"TextView"],Constants.mapToGui.get("drND.png")[4])}
    Constants.mapToGui = {}
    for (key, val) in mapUpdatedFromGui.items(): 
        imgPath = os.path.join(imagesPath, key)
        if (".png" in imgPath or ".jpeg" in imgPath or ".jpg" in imgPath) and ('._' not in imgPath):
            updateImage(imagesPath, key,val)
            
# UI2XMLclassification_224_245000_99_93
# UI2XMLclassificationAlex_224_245000_99_92 adam with 224 * 224
# UI2XMLclassification245000_98_91 decay with 150 * 150
# UI2XMLclassification245000_98_90 adam with 150 * 150
# UI2XMLclassification245000_97_87 with 64 * 64

'''
vocab,invVocab = LoadDataClassification.loadVocab('data/vocab_classification.txt')
model = load_model('data/ourModel/'+Constants.MODEL_NAME) # 150 * 150
imagesPath='data/ScreenShots/ourTest'

processAllImages(imagesPath,model,invVocab)
print(Constants.mapToGui,'\n')
print(Utils.getXmlOfComponent(0,'face3AD.jpg'),'\n')
print(Utils.getXmlOfComponent(2,'face3AD.jpg'),'\n')
print(Utils.getXmlOfComponent(3,'face3AD.jpg'),'\n')
'''
#updateAllImages(imagesPath,{})
