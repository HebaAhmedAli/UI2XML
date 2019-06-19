import ComponentsExtraction.ComponentsExtraction as ComponentsExtraction
import XmlGeneration.XmlGeneration as XmlGeneration
from keras.models import load_model
import LoadDataClassification
import cv2
import os
import copy
import numpy as np
from keras.preprocessing import image
import time

vocab,invVocab = LoadDataClassification.loadVocab('data/vocab_classification.txt')
model = load_model('data/ourModel/UI2XMLclassification245000_98_91.h5') # 150 * 150
# UI2XMLclassification_224_245000_99_93
# UI2XMLclassificationAlex_224_245000_99_92 adam with 224 * 224
# UI2XMLclassification245000_98_91 decay with 150 * 150
# UI2XMLclassification245000_98_90 adam with 150 * 150
# UI2XMLclassification245000_97_87 with 64 * 64

imagesPath='data/ScreenShots'

def processSave(subdir, file):
    img = cv2.imread(subdir+'/' +file)
    imgCopy = copy.copy(img)
    imgXML = image.load_img(subdir+'/' +file)
    imgXML = np.array(imgXML,dtype='float32')  
    #img = np.copy(imgXML)
    #imgCopy = np.copy(imgXML)
    file = file.replace('.jpeg','.jpg')
    boxes, texts ,addedManuallyBool ,predictedComponents= ComponentsExtraction.extractComponentsAndPredict(img,imgCopy,model,invVocab)
    margin = 10
    if not os.path.exists(subdir+'/compOutputsAll'+file[:-4]):
        os.makedirs(subdir+'/compOutputsAll'+file[:-4])
    if not os.path.exists(subdir+'/compOutputs'+file[:-4]):
        os.makedirs(subdir+'/compOutputs'+file[:-4])    
    if not os.path.exists(subdir+'/boxOutputs'):
        os.makedirs(subdir+'/boxOutputs')
    j = 0
    height= img.shape[0]
    width= img.shape[1]
    fTo=open(subdir+'/compOutputsAll'+file[:-4]+'/texts.txt', 'w+')
    boxesFiltered,textsFiltered,predictedComponentsFiltered=ComponentsExtraction.filterComponents(boxes, texts ,addedManuallyBool ,predictedComponents,imgCopy,model,invVocab)
    XmlGeneration.generateXml(boxesFiltered,textsFiltered,predictedComponentsFiltered,imgXML,file[:-5],file[len(file)-5])
    for x,y,w,h in boxes:
        # testing: print the cropped in folder
        crop_img = imgCopy[max(0,y - margin):min(height,y + h + margin), max(x - margin,0):min(width,x + w + margin)]
        cv2.imwrite(subdir + "/compOutputsAll"+file[:-4]+'/'+str(j)+'-'+ predictedComponents[j] + str(file[len(file)-4:len(file)]),crop_img)
        fTo.write(str(j)+'- '+texts[j]+'\n')
        j+=1    
    fTo.close()
    fTo=open(subdir+'/compOutputs'+file[:-4]+'/texts.txt', 'w+')
    j=0
    for x,y,w,h in boxesFiltered:
        # testing: print the cropped in folder
        crop_img = imgCopy[max(0,y - margin):min(height,y + h + margin), max(x - margin,0):min(width,x + w + margin)]
        cv2.imwrite(subdir + "/compOutputs"+file[:-4]+'/'+str(j)+'-'+ predictedComponentsFiltered[j] + str(file[len(file)-4:len(file)]),crop_img)
        fTo.write(str(j)+'- '+textsFiltered[j]+'\n')
        j+=1  
    cv2.imwrite(subdir+"/boxOutputs/"+file,img)

startTime = time.time()
subdir, dirs, _= next(os.walk(imagesPath))
for direc in dirs:
    _,_, files= next(os.walk(subdir+'/'+direc))
    for file in files:
        imgPath = os.path.join(subdir, file)
        if (".png" in imgPath or ".jpeg" in imgPath or ".jpg" in imgPath) and ('._' not in imgPath):
            startTimeI = time.time()
            processSave(subdir+'/'+direc, file)
            print(time.time()-startTimeI)
print(time.time()-startTime)