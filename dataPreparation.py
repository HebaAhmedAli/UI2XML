import shutil
import os

def printVocab(vocab,path):
    fTo=open(path, 'w+')
    for val in vocab:
        fTo.write(val+'\n')
    fTo.close()
    

def readXml(path,vocab):
    guiLine=""
    strings=[]
    with open(path, "r") as ins:
        for line in ins:
            strings+=line.split()
        for i in range(len(strings)):
            if strings[i][len(strings[i])-1]==',':
                vocab.update([strings[i][:-1]])
                vocab.update([','])
                guiLine+=strings[i][:-1]+" "+','+" "
            else:
                vocab.update([strings[i]])
                guiLine+=strings[i]+" "
    return guiLine

def constructData2(imagesFrom,imagesTo,xmlTo,vocab):
    root,directories,files=next(os.walk(imagesFrom))
    fTo=open(xmlTo, 'w+')
    i=0
    mxLen=0
    for file in files:
        if file.endswith(".png"):
            shutil.copy(imagesFrom+file, imagesTo+str(i)+'.png')
            guiLine=readXml(imagesFrom+(file[:-4])+'.gui',vocab)
            fTo.write(guiLine+'\n')
            i=i+1
            mxLen=max(mxLen,len(guiLine.split()))
    print("max len : "+str(mxLen))
    fTo.close()
def constructData(fileKeyValue,imagesFrom,imagesTo,xmlFrom,xmlTo):
    fFrom=open(xmlFrom)
    sequences=fFrom.readlines()
    print(len(sequences))
    fTo=open(xmlTo, 'w+')
    i=0
    with open(fileKeyValue, "r") as ins:
        for line in ins:
            imageName,lineIndex=line.split()
            shutil.copy(imagesFrom+imageName, imagesTo+str(i)+'.png')
            fTo.write(sequences[int(lineIndex)])
            i=i+1
            
    fFrom.close()
    fTo.close()
    
def getUnwantedVoab(vocabPath):
    unwanted=[]
    with open(vocabPath, "r") as ins:
        for line in ins:
            unwanted.append(line[:-1])
    return unwanted

def printUnwantedIndices(xmlPath,unwantedVocab):
    indices=set()
    fFrom=open(xmlPath)
    sequences=fFrom.readlines()
    for i in range(len(sequences)):
        for j in range(len(unwantedVocab)):
            if unwantedVocab[j] in sequences[i]:
                indices.update([i])
    print("len of indices = "+str(len(indices)))
    listIndices=list(indices)
    listIndices.sort()
    return listIndices
def removeUnwantedIndices(listIndices,imagePath,imagePathTo,maxFileSize,xmlFrom,xmlTo):
    allIndices=[i for i in range(maxFileSize)]
    finalIndices=[]
    booleanIndices=[True for i in range(maxFileSize)]
    for i in range(len(listIndices)):
        #os.remove(imagePath+str(listIndices[i])+".png")
        booleanIndices[listIndices[i]]=False
    fFrom=open(xmlFrom)
    sequences=fFrom.readlines()
    fTo=open(xmlTo, 'w+')  
    for i in range(len(allIndices)):
        if booleanIndices[i] == True:
            finalIndices.append(allIndices[i])
    for i in range(len(finalIndices)):
        fTo.write(sequences[finalIndices[i]])
        shutil.copy(imagePath+str(finalIndices[i])+'.png', imagePathTo+str(i)+'.png')
    fTo.close()
    print("len after removing : "+str(len(finalIndices)))

def printNewVocab(vocabPath,unwantedVocabPath,finalPath):
    fVocabs=open(vocabPath)
    vocabs=fVocabs.readlines()
    fUnwantedVocabs=open(unwantedVocabPath)
    unwantedVocabs=fUnwantedVocabs.readlines()     
    finalVocabs=list(set(vocabs) - set(unwantedVocabs))
    print(len(set(vocabs)),len(set(unwantedVocabs)))
    print(len(vocabs),len(unwantedVocabs),len(finalVocabs))
    fTo=open(finalPath, 'w+')  
    for i in range(len(finalVocabs)):
        fTo.write(finalVocabs[i])
    fTo.close()

def replaceVocabs(repPath,xmlPath):
    fFrom=open(xmlPath)
    sequences=fFrom.readlines()
    fFrom.close()
    fFromRep=open(repPath)
    vocabs=fFromRep.readlines()
    fFromRep.close()
    for i in range(len(sequences)):
        for j in range(len(vocabs)):
            firstStr=vocabs[j].split()[0]
            secondString=vocabs[j].split()[1]
            sequences[i]=sequences[i].replace(firstStr,secondString)
    fTo=open(xmlPath, 'w+')  
    for i in range(len(sequences)):
        fTo.write(sequences[i])
    fTo.close()

def copyData(imagesFrom,imagesTo1,imagesTo2):
  root,directories,files=next(os.walk(imagesFrom))
  for i in range(len(files)):
    if i<(len(files)/2):
        shutil.copy(imagesFrom+files[i], imagesTo1+files[i])
    else:
        shutil.copy(imagesFrom+files[i], imagesTo2+files[i])

copyData('data/testAndValidationToRename/TestAll/','data/testAndValidationToRename/Test1/','data/testAndValidationToRename/Test2/')
'''
unwantedVocab=getUnwantedVoab("data/unwanted_vocab.txt")
printNewVocab('data/xml_vocabR.txt',"data/unwanted_vocab.txt",'data/xml_vocab.txt')
listIndices1=printUnwantedIndices("data/XmlTrainingR.lst",unwantedVocab)
listIndices2=printUnwantedIndices('data/XmlTestingR.lst',unwantedVocab)
listIndices3=printUnwantedIndices('data/XmlValidationR.lst',unwantedVocab)
removeUnwantedIndices(listIndices1,'data/trainingImagesR/','data/trainingImages/',165887,'data/XmlTrainingR.lst','data/XmlTraining.lst')
removeUnwantedIndices(listIndices2,'data/testingImagesR/','data/testingImages/',12643,'data/XmlTestingR.lst','data/XmlTesting.lst')
removeUnwantedIndices(listIndices3,'data/validationImagesR/','data/validationImages/',5539,'data/XmlValidationR.lst','data/XmlValidation.lst')
'''
#printNewVocab('data/xml_vocabR.txt',"data/unwanted_vocab.txt",'data/xml_vocabInter.txt')
#printNewVocab('data/xml_vocabInter.txt',"data/replacementRemove.txt",'data/xml_vocab.txt')
'''
replaceVocabs('data/replacement.txt','data/XmlTraining.lst')
replaceVocabs('data/replacement.txt','data/XmlValidation.lst')
replaceVocabs('data/replacement.txt','data/XmlTesting.lst')
'''
#constructData('data/try.lst','data/processedImage/','data/tryImages/','data/XMLsequence.lst','data/XmlTry.lst')
#constructData('data/train.lst','data/processedImage/','data/trainingImages/','data/XMLsequence.lst','data/XmlTraining.lst')
#constructData('data/validate.lst','data/processedImage/','data/validationImages/','data/XMLsequence.lst','data/XmlValidation.lst')
#constructData('data/test_shuffle.lst','data/processedImage/','data/testingImages/','data/XMLsequence.lst','data/XmlTesting.lst')
'''
vocab=set()
print(len(vocab))
constructData2('data/training_set/','data/trainingImages2/','data/XmlTraining2.lst',vocab)
constructData2('data/eval_set/','data/testingImages2/','data/XmlTesting2.lst',vocab)
printVocab(vocab,'data/xml_vocab2.txt')
print(len(vocab))
fFrom=open('data/XmlTesting.lst')
sequences=fFrom.readlines()
mxLen=0
for i in range(len(sequences)):
    mxLen=max(mxLen,len(sequences[i].split()))
    
print("max len : "+str(mxLen))
'''