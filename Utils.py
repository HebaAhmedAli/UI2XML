import Constants
import numpy as np
from keras.utils import to_categorical

   
# Converts the sequnce  into a list of integers representing the positions of the
# input sequence's strings in the "vocab"
    
def sequenceToIndices(sequence, vocab):
    keyStrings = sequence.split()
    if len(keyStrings) > Constants.MAX_SEQUENCE_LENGTH:
        keyStrings = keyStrings[:Constants.MAX_SEQUENCE_LENGTH]       
    indices = list(map(lambda x: vocab.get(x), keyStrings))
    return indices

# Converts the list of indices into list of coresspnding keyStrings.
def indicesToSequence(indices, invVocab):
    keyStrings = [invVocab[i] for i in indices]
    sequence = ' '.join(keyStrings)
    return sequence




