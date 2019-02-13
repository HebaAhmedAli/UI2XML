import Utils
import Preprocessing
import numpy as np
from keras.utils import to_categorical

# TODO: Add function to load dataSet.

def loadVocab(vocabPath):
    keyStrings=set()
    with open(vocabPath, "r") as ins:
        for line in ins:
            keyStrings.update([line[:-1]])
    keyStrings.update(['<pad>'])
    keyStrings.update(['\t'])
    keyStrings.update(['\n'])
    invVocab = dict(enumerate(sorted(keyStrings)))
    vocab = {v:k for k,v in invVocab.items()}
    print("vocabulary length = "+str(len(vocab)))
    print("inv vocabulary length = "+str(len(invVocab)))
    return vocab, invVocab

def loadData(imagesPath,xmlPath,vocab,start,end):
    Y=[]
    i=0
    with open(xmlPath, "r") as ins:
        for line in ins:
            if i>=start and i<end:
                Y.append(line)
            elif i>=end:
                break
            i=i+1
    Yhot , YhotShiftedLeft = preprocessY(Y,vocab)
    X=[]
    for i in range(start,end):
        x=Preprocessing.imageReadAndPreprocessing(imagesPath+str(i)+'.png')
        X.append(x)
    print("X shape = "+str(np.array(X).shape))
    print("Yhot shape = "+str(Yhot.shape))
    return np.array(X), Yhot , YhotShiftedLeft
    
def loadDataForBleu(imagesPath,xmlPath,vocab,start,end):
    Y=[]
    i=0
    with open(xmlPath, "r") as ins:
        for line in ins:
            if i>=start and i<end:
                Y.append(line.split())
            elif i>=end:
                break
            i=i+1
    X=[]
    for i in range(start,end):
        x=Preprocessing.imageReadAndPreprocessing(imagesPath+str(i)+'.png')
        X.append(x)
    print("X shape = "+str(np.array(X).shape))
    return np.array(X), Y
    
def preprocessY(Y,vocab):
    Y = [Utils.sequenceToIndices(t , vocab) for t in Y]
    YhotShiftedLeft=[Y[i][1:len(Y[i])]+[vocab['<pad>']] for i in range(len(Y))]
    Yhot = np.array(list(map(lambda x: to_categorical(x, num_classes=len(vocab)), Y)))
    YhotShiftedLeft =np.array(list(map(lambda x: to_categorical(x, num_classes=len(vocab)), YhotShiftedLeft)))
    return  Yhot , YhotShiftedLeft



