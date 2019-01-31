import Utils
import Constants
import numpy as np
from keras.utils import to_categorical

def preprocessData(dataset, vocab):
    X, Y = zip(*dataset)
    
    Y = [Utils.sequenceToIndices(t , vocab) for t in Y]
    
    Yoh = np.array(list(map(lambda x: to_categorical(x, num_classes=len(vocab)), Y)))

    return X, np.array(Y) , Yoh


# Testing to be used.
keyStrings=set()
keyStrings.update(["heba"])
keyStrings.update(["feryal"])
keyStrings.update(["fatema"])
invVocab = dict(enumerate(sorted(keyStrings)))
vocab = {v:k for k,v in invVocab.items()}
print(keyStrings)
print(invVocab)
print(vocab)
print(Utils.indicesToSequence(Utils.sequenceToIndices("heba fatema",vocab),invVocab))
#####################.
