from keras.preprocessing import image
import Constants as Constants
import numpy as np
import cv2


def imageReadAndPreprocessingClassification(imgPath=None,imagee=None):
        if imgPath!=None:
            img = image.load_img(imgPath, target_size = (Constants.IMAGE_SIZE_CLASSIFICATION,Constants.IMAGE_SIZE_CLASSIFICATION))
        else:
            img = cv2.resize(imagee,(Constants.IMAGE_SIZE_CLASSIFICATION,Constants.IMAGE_SIZE_CLASSIFICATION))
            #img = Image.fromarray(image).resize((Constants.IMAGE_SIZE_CLASSIFICATION,Constants.IMAGE_SIZE_CLASSIFICATION))
        img = np.array(img,dtype='float32')  
        img /= 255.
        return img
