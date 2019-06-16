import cv2
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import morphology, label
import random

# CANNY algorithm
CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO = 0.66
# we want to low threshold value of candy always below 0.1 #255, some
# image the contrast between button and background not must different
CANNY_RATIO_CONTROL_THRESHOLD = 0.1 / CANNY_KERRY_WONG_LOW_THRESHOLD_RATIO
    
dilationSize = 1
lowThreshold = 30
highThreshold = 80
cannyRatio = 2


def preProcess(image):
    # convert the image to grayscale, blur it slightly, and threshold it
    im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Inner morphological gradient.
    morph = morphology.grey_dilation(im, (5, 5)) - im
    return morph

# Extract boxes from given image.
def extractBoxes(img,texts, txtBoxes):
    # Initialize isText and textBoxes
    allBoxes = txtBoxes
    isText = texts
    morph=preProcess(img)
    # Binarize.
    mean, std = morph.mean(), morph.std()
    t = mean + std
    morph[morph < t] = 0
    morph[morph >= t] = 1
    # Connected components.
    lbl, numcc = label(morph)
    # Size threshold.
    min_size = 200 # pixels
    for i in range(1, numcc + 1):
        py, px = np.nonzero(lbl == i)
        if len(py) < min_size:
            morph[lbl == i] = 0
            continue
        xmin, xmax, ymin, ymax = px.min(), px.max(), py.min(), py.max()
        randColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        cv2.rectangle(img, (xmin,ymin), (xmax,ymax), randColor,2)
        allBoxes.append([xmin, ymin, xmax-xmin, ymax-ymin])
        isText.append("")

    filteredBoxes=filterBoxes(allBoxes)
    return filteredBoxes

def filterBoxes(allBoxes):
    filteredBoxes=allBoxes #TODO: Filter Them.
    
    return filteredBoxes