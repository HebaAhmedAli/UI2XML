import Utils
import Model.Constants as Constants
import numpy as np
from keras.utils import to_categorical

# TODO: Complete this function.
def preprocessData(dataset, vocab):
    X, Y = zip(*dataset)
    
    Y = [Utils.sequenceToIndices(t , vocab) for t in Y]
    
    Yoh = np.array(list(map(lambda x: to_categorical(x, num_classes=len(vocab)), Y)))
    #YohShiftedLeft = Yoh[1:len(Y)]+ hotvector of <pad>
    return X, Yoh , YohShiftedLeft


# Testing to be used.
keyStrings=set()
keyStrings.update(["heba"])
keyStrings.update(["feryal"])
keyStrings.update(["fatema"])
keyStrings.update(['<pad>'])
keyStrings.update(['\t'])
keyStrings.update(['\n'])

invVocab = dict(enumerate(sorted(keyStrings)))
vocab = {v:k for k,v in invVocab.items()}
print(keyStrings)
print(invVocab)
print(vocab)
print(Utils.sequenceToIndices("heba fatema <pad>",vocab))
#####################.
