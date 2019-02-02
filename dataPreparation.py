import shutil


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
            fTo.write(sequences[int(lineIndex)]+'\n')
            i=i+1
            
    fFrom.close()
    fTo.close()
            
#constructData('data/train.lst','data/processedImage/','data/trainingImages/','data/XMLsequence.lst','data/XmlTraining.lst')
constructData('data/validate.lst','data/processedImage/','data/validationImages/','data/XMLsequence.lst','data/XmlVlidation.lst')
#constructData('data/test_shuffle.lst','data/processedImage/','data/testingImages/','data/XMLsequence.lst','data/XmlTesting.lst')
