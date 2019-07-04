from psd_tools import PSDImage
from keras.models import load_model
from keras.preprocessing import image
import LoadDataClassification
import CodeGeneration.XmlGeneration as XmlGeneration
import PsdMode.ComponentsExtraction as ComponentsExtraction
import numpy as np
import Constants
import cv2
import os

def processPsd(subdir, file,model,invVocab):
    psd = PSDImage.load(subdir+'/' +file)
    mergedImage = psd.as_PIL()
    mergedImage.save(subdir+'/' +file[:-4]+'.png')
    img = cv2.imread(subdir+'/' +file[:-4]+'.png')
    imgXML = image.load_img(subdir+'/' +file[:-4]+'.png')
    imgXML = np.array(imgXML,dtype='float32')  
    boxes, texts ,predictedComponents = ComponentsExtraction.extractComponentsAndPredict(psd,img,imgXML,model,invVocab)
    if Constants.DEBUG_MODE == True :
        if not os.path.exists(subdir+'/compOutputs'+file[:-4]):
            os.makedirs(subdir+'/compOutputs'+file[:-4])    


    height= img.shape[0]
    width= img.shape[1]
    
    if Constants.DEBUG_MODE == True :
        fTo=open(subdir+'/compOutputs'+file[:-4]+'/texts.txt', 'w+')

    if file[len(file)-5] == 'D':
        Constants.DYNAMIC=True
    else:
        Constants.DYNAMIC=False
    parentNodesForGui = XmlGeneration.generateXml(boxes,texts,predictedComponents,imgXML,file[:-6],file[len(file)-6])
    Constants.mapToGui.update( {file[:-4]+'.png' : [Constants.boxToGui,Constants.idToGui,Constants.predictedToGui,Constants.xmlFilesToGui,Constants.inWhichFile,parentNodesForGui]})
    #print(Constants.mapToGui)
    if Constants.DEBUG_MODE == True :
        j = 0
        for x,y,w,h in boxes:
            # testing: print the cropped in folder
            crop_img = img[max(0,y):min(height,y + h ), max(x ,0):min(width,x + w )]
            cv2.imwrite(subdir + "/compOutputs"+file[:-4]+'/'+str(j)+'-'+ predictedComponents[j] + '.png',crop_img)
            fTo.write(str(j)+'- '+texts[j]+" "+str(boxes[j])+'\n')
            j+=1    
        fTo.close()
        j=0


def processAllPsds(imagesPath,model,invVocab):
   Constants.DIRECTORY = imagesPath[:-5] + Constants.androidPath
   Constants.mapToGui = {}
   _,_, files= next(os.walk(imagesPath))
   for file in files:
        imgPath = os.path.join(imagesPath, file)
        if (".psd" in imgPath) and ('._' not in imgPath):
            processPsd(imagesPath, file,model,invVocab)
    
def updateImage(subdir,file,valMapFromGui):
    imgXML = image.load_img(subdir+'/' +file)
    imgXML = np.array(imgXML,dtype='float32')  
    if file[len(file)-5] == 'D':
        Constants.DYNAMIC=True
    else:
        Constants.DYNAMIC=False
    parentNodesForGui = XmlGeneration.updateXml(valMapFromGui[3],valMapFromGui[0],valMapFromGui[2],valMapFromGui[1],imgXML,file[:-6],file[len(file)-6])
    Constants.mapToGui.update( {file : [Constants.boxToGui,Constants.idToGui,Constants.predictedToGui,Constants.xmlFilesToGui,Constants.inWhichFile,parentNodesForGui]})
    
def updateAllImages(imagesPath,mapUpdatedFromGui):
    # TODO: Comment after testing.
    #mapUpdatedFromGui = {"drND.png":([[36, 315, 128, 88]],['ImageView_0_2_0'],['android.widget.'+"TextView"],Constants.mapToGui.get("drND.png")[4])}
    Constants.mapToGui = {}
    for (key, val) in mapUpdatedFromGui.items(): 
        imgPath = os.path.join(imagesPath, key)
        if (".png" in imgPath) and ('._' not in imgPath):
            updateImage(imagesPath, key,val)

'''
vocab,invVocab = LoadDataClassification.loadVocab('data/vocab_classification.txt')
model = load_model('data/ourModel/UI2XMLclassificationAllFeaturesAC_98_92.h5') # 150 * 150
imagesPath='data/Psds/ourTest'

processAllPsds(imagesPath,model,invVocab)
'''