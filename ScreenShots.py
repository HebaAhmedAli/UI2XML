from multiprocessing import Process,Manager
import Constants
import cv2
import os
import copy
import numpy as np
import time
from keras.models import load_model
from keras.preprocessing import image
import LoadDataClassification
import ScreenShotMode.ComponentsExtraction as ComponentsExtraction
import CodeGeneration.XmlGeneration as XmlGeneration
    

def filterAndConstructXml(subdir,file,img,imgCopy,imgXML,boxes,texts,addedManuallyBool,predictedComponents):
    margin = 10
    boxesFiltered,textsFiltered,predictedComponentsFiltered=ComponentsExtraction.filterComponents(boxes, texts ,addedManuallyBool ,predictedComponents,imgCopy)
    boxToGui=[]
    predictedToGui=[]
    idToGui=[]
    xmlFilesToGui=[]
    inWhichFile=[]
    parentNodesForGui = XmlGeneration.generateXml(boxesFiltered,textsFiltered,predictedComponentsFiltered,imgXML,file[:-6],file[len(file)-6],boxToGui=boxToGui,predictedToGui=predictedToGui,idToGui=idToGui,xmlFilesToGui=xmlFilesToGui,inWhichFile=inWhichFile,dynamic=file[len(file)-5] == 'D')
    Constants.mapToGui.update( {file : [boxToGui,idToGui,predictedToGui,xmlFilesToGui,inWhichFile,parentNodesForGui]})
    #parentNodesForGui = XmlGeneration.updateXml(parentNodesForGui,[[19, 18, 44, 42]],['android.widget.'+"TextView"],['ImageView_0_16_1_0_1'],imgXML,file[:-6],file[len(file)-6])
    if Constants.DEBUG_MODE == True :
        height= imgCopy.shape[0]
        width= imgCopy.shape[1]
        fTo=open(subdir+'/compOutputsAll'+file[:-4]+'/texts.txt', 'w+')
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
            crop_img = imgCopy[max(0,y - margin - edit):min(height,y + h + margin), max(x - margin,0):min(width,x + w + margin)]
            cv2.imwrite(subdir + "/compOutputs"+file[:-4]+'/'+str(j)+'-'+ predictedComponentsFiltered[j] + str(file[len(file)-4:len(file)]),crop_img)
            fTo.write(str(j)+'- '+textsFiltered[j]+" "+str(boxesFiltered[j])+'\n')
            j+=1  
        cv2.imwrite(subdir+"/boxOutputs/"+file,img)
        
def createProcess(subdir,file,img,imgCopy,imgXML,boxes,texts,addedManuallyBool,predictedComponents):
    process = Process(target=filterAndConstructXml, args=(subdir,file,img,imgCopy,imgXML,boxes,texts,addedManuallyBool,predictedComponents))
    return process



def processImage(subdir, file,model,invVocab):
    img = cv2.imread(subdir+'/' +file)
    imgCopy = copy.copy(img)
    imgXML = image.load_img(subdir+'/' +file)
    imgXML = np.array(imgXML,dtype='float32')  
    file = file.replace('.jpeg','.jpg')
    boxes, texts ,addedManuallyBool ,predictedComponents = ComponentsExtraction.extractComponentsAndPredict(img,imgCopy,imgXML,model,invVocab)
    if Constants.DEBUG_MODE == True :
        if not os.path.exists(subdir+'/compOutputsAll'+file[:-4]):
            os.makedirs(subdir+'/compOutputsAll'+file[:-4])
        if not os.path.exists(subdir+'/compOutputs'+file[:-4]):
            os.makedirs(subdir+'/compOutputs'+file[:-4])    
        if not os.path.exists(subdir+'/boxOutputs'):
            os.makedirs(subdir+'/boxOutputs')
    # open Process
    return createProcess(subdir,file,img,imgCopy,imgXML,boxes,texts,addedManuallyBool,predictedComponents)


def processAllImages(imagesPath,model,invVocab):
    startTime = time.time()
    Constants.DIRECTORY = imagesPath[:-5] + Constants.androidPath
    if not os.path.exists(Constants.DIRECTORY):
            os.makedirs(Constants.DIRECTORY)
    manager=Manager()
    # Initialize the vectors of each image with empty vector(this vector is shared between processes)
    Constants.mapToGui=manager.dict()
    processes = []
    #Constants.mapToGui = {}
    _,_, files= next(os.walk(imagesPath))
    for file in files:
        imgPath = os.path.join(imagesPath, file)
        if (".png" in imgPath or ".jpeg" in imgPath or ".jpg" in imgPath) and ('._' not in imgPath):
            process = processImage(imagesPath, file,model,invVocab)
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
    parentNodesForGui = XmlGeneration.updateXml(valMapFromGui[3],valMapFromGui[0],valMapFromGui[2],valMapFromGui[1],imgXML,file[:-6],file[len(file)-6],boxToGui=boxToGui,predictedToGui=predictedToGui,idToGui=idToGui,xmlFilesToGui=xmlFilesToGui,inWhichFile=inWhichFile,dynamic=file[len(file)-5] == 'D')
    Constants.mapToGui.update( {file : [boxToGui,idToGui,predictedToGui,xmlFilesToGui,inWhichFile,parentNodesForGui]})

def createUpdateProcess(subdir,file,valMapFromGui):
    process = Process(target=updateImage, args=(subdir,file,valMapFromGui))
    return process       

         
def updateAllImages(imagesPath,mapUpdatedFromGui):
    # TODO: Comment after testing.
    #mapUpdatedFromGui = {"drAD.png":[[[36, 315, 128, 88]],['ImageView_0_2_0'],['android.widget.'+"TextView"],Constants.mapToGui.get("drAD.png")[5]]}
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

# UI2XMLclassification_224_245000_99_93
# UI2XMLclassificationAlex_224_245000_99_92 adam with 224 * 224
# UI2XMLclassification245000_98_91 decay with 150 * 150
# UI2XMLclassification245000_98_90 adam with 150 * 150
# UI2XMLclassification245000_97_87 with 64 * 64

'''
vocab,invVocab = LoadDataClassification.loadVocab('data/vocab_classification.txt')
model = load_model('data/ourModel/'+Constants.MODEL_NAME) # 150 * 150

imagesPath='data/ScreenShots/ourTest'
startTime = time.time()
processAllImages(imagesPath,model,invVocab)
print("Total time = ",time.time()-startTime)
'''

'''
print(Constants.mapToGui,'\n')
print(Utils.getXmlOfComponent(0,'face3AD.jpg'),'\n')
print(Utils.getXmlOfComponent(2,'face3AD.jpg'),'\n')
print(Utils.getXmlOfComponent(3,'face3AD.jpg'),'\n')
'''
#updateAllImages(imagesPath,{})