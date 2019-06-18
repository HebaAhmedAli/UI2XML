import Preprocessing
import numpy as np
from keras.utils import to_categorical
import os

def loadVocab(vocabPath):
    keyStrings=set()
    with open(vocabPath, "r") as ins:
        for line in ins:
            keyStrings.update([line[:-1]])
    invVocab = dict(enumerate(sorted(keyStrings)))
    vocab = {v:k for k,v in invVocab.items()}
    print("vocabulary length = "+str(len(vocab)))
    print("inv vocabulary length = "+str(len(invVocab)))
    return vocab, invVocab

def loadData(imagesPath,vocab,start,end):
    root,directories,files=next(os.walk(imagesPath))
    Y=[]
    X=[]
    i=0
    for file in files:
        if i>=start and i<end:
            index=file.find('-')
            y=file[index+1:-4]
            Y.append(to_categorical(vocab[y], num_classes=len(vocab)))
            x=Preprocessing.imageReadAndPreprocessingClassification(imagesPath+file)
            X.append(x)
        elif i>= end:
            break
        i+=1
    print("X shape = "+str(np.array(X).shape))
    print("Y shape = "+str(np.array(Y).shape))
    return np.array(X), np.array(Y)
