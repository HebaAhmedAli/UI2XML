from keras.preprocessing import image
import Model.Constants as Constants
import numpy as np


def imageReadAndPreprocessing(imgPath):
        img = image.load_img(imgPath, target_size = (Constants.IMAGE_SIZE,Constants.IMAGE_SIZE))
        img = np.array(img,dtype='float32')  
        img /= 255.
        #img = np.expand_dims(img, 0)  # Add batch dimension.
        return img