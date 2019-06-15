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

# box = x,y,w,h
def iou(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2]+boxA[0], boxB[2]+boxB[0])
    yB = min(boxA[3]+boxA[1], boxB[3]+boxB[1])

    # compute the area of intersection rectangle
    if yB>=yA and xB >= xA:
        return (xB - xA) * (yB - yA)
    else:
        return 0
    
def checkYrange(boxA,boxB):
    if (boxA[1]>=boxB[1] and boxA[1]<(boxB[1]+boxB[3])) or \
    ((boxA[1]+boxA[3])>boxB[1] and (boxA[1]+boxA[3])<(boxB[1]+boxB[3])) or \
    (boxB[1]>=boxA[1] and boxB[1]<(boxA[1]+boxA[3])) or \
    ((boxB[1]+boxB[3])>boxA[1] and (boxB[1]+boxB[3])<(boxA[1]+boxA[3])):
        return True
    return False

def checkXrange(boxA,boxB):
    if (boxA[0]>=boxB[0] and boxA[0]<(boxB[0]+boxB[2])) or \
    ((boxA[0]+boxA[2])>boxB[0] and (boxA[0]+boxA[2])<(boxB[0]+boxB[2])) or \
    (boxB[0]>=boxA[0] and boxB[0]<(boxA[0]+boxA[2])) or \
    ((boxB[0]+boxB[2])>boxA[0] and (boxB[0]+boxB[2])<(boxA[0]+boxA[2])):
        return True
    return False

        

def isSliceList(s,l):
    for i in range(len(s)):
        if s[i] not in l:
            return False
    return True



