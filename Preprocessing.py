from keras.preprocessing import image
import Constants as Constants
import numpy as np
import cv2

def imageReadAndPreprocessing(imgPath):
        img = image.load_img(imgPath, target_size = (Constants.IMAGE_SIZE,Constants.IMAGE_SIZE))
        img = np.array(img,dtype='float32')  
        img /= 255.
        return img

def imageReadAndPreprocessingClassification(image=None,imgPath=None):
        if imgPath!=None:
            img = image.load_img(imgPath, target_size = (Constants.IMAGE_SIZE_CLASSIFICATION,Constants.IMAGE_SIZE_CLASSIFICATION))
        else:
            img = cv2.resize(image,(Constants.IMAGE_SIZE_CLASSIFICATION,Constants.IMAGE_SIZE_CLASSIFICATION))
        img = np.array(img,dtype='float32')  
        img /= 255.
        return img