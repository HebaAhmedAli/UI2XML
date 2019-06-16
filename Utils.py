import sys
sys.path.append('../')
import Constants as Constants
 

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
    


def isSliceList(s,l):
    for i in range(len(s)):
        if s[i] not in l:
            return False
    return True



