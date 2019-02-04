import sys
sys.path.append('../')
import Constants as Constants
 
# Converts the sequnce  into a list of integers representing the positions of the
# input sequence's strings in the "vocab"
    
def sequenceToIndices(sequence, vocab):
    keyStrings = sequence.split()  
    keyStrings = ['\t'] + keyStrings + ['\n']
    if len(keyStrings) > Constants.MAX_SEQUENCE_LENGTH:
        keyStrings = keyStrings[:Constants.MAX_SEQUENCE_LENGTH]       
    indices = list(map(lambda x: vocab.get(x), keyStrings))
    if len(keyStrings) < Constants.MAX_SEQUENCE_LENGTH:
        indices += [vocab['<pad>']] * (Constants.MAX_SEQUENCE_LENGTH - len(keyStrings))   
    for i in range(len(indices)):
        if indices[i] == None:
            indices.pop(i)
            indices.append(vocab['<pad>'])
    return indices

# Converts the list of indices into list of coresspnding keyStrings.
def indicesToSequence(indices, invVocab):
    keyStrings = [invVocab[i] for i in indices]
    sequence = ' '.join(keyStrings)
    return sequence






