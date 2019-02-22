import ComponentsExtraction.ComponentsExtraction as ComponentsExtraction
import ModelClassification.Model as Model
from keras.models import load_model
import LoadDataClassification
import cv2
import os
import copy

vocab,invVocab = LoadDataClassification.loadVocab('data/vocab_classification.txt')
model = load_model('data/ourModel/UI2XMLclassification245000_98_91.h5')

imagesPath='data/ScreenShots'

def processSave(subdir, file):
    img=cv2.imread(subdir+'/' +file)
    imgCopy = copy.copy(img)
    file = file.replace('.jpeg','.jpg')
    boxes, texts = ComponentsExtraction.extractComponents(img,imgCopy)
    margin = 10
    if not os.path.exists(subdir+'/compOutputs'+file[:-4]):
        os.makedirs(subdir+'/compOutputs'+file[:-4])
    if not os.path.exists(subdir+'/boxOutputs'):
        os.makedirs(subdir+'/boxOutputs')
    j = 0
    height= img.shape[0]
    width= img.shape[1]
    fTo=open(subdir+'/compOutputs'+file[:-4]+'/texts.txt', 'w+')
    for x,y,w,h in boxes:
        # testing: print the cropped in folder
        crop_img = imgCopy[max(0,y - margin):min(height,y + h + margin), max(x - margin,0):min(width,x + w + margin)]
        cv2.imwrite(subdir + "/compOutputs"+file[:-4]+'/'+str(j) + str(file[len(file)-4:len(file)]),crop_img)
        pedictedComp=Model.makeAprediction(invVocab,subdir + "/compOutputs"+file[:-4]+'/'+str(j) + str(file[len(file)-4:len(file)]),model)
        cv2.imwrite(subdir + "/compOutputs"+file[:-4]+'/'+str(j)+'-'+ pedictedComp + str(file[len(file)-4:len(file)]),crop_img)
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
