from keras.preprocessing import image
import Constants as Constants
import numpy as np


def imageReadAndPreprocessing(imgPath):
        img = image.load_img(imgPath, target_size = (Constants.IMAGE_SIZE,Constants.IMAGE_SIZE))
        img = np.array(img,dtype='float32')  
        img /= 255.
        return img