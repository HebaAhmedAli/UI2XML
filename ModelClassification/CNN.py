import sys
sys.path.append('../')
from keras.layers import Conv2D, MaxPooling2D, Dense,Dropout,Activation
from keras.models import Model
import keras.backend as K
import numpy as np
import Constants

def createCNN(xInput):
    x = Conv2D(64, (7, 7), stride = (2,2),padding='same', activation='relu')(xInput)
    x = Conv2D(64, (7, 7), stride = (2,2), padding='same', activation='relu')(x)
    x = MaxPooling2D(pool_size=(3, 3))(x)
    x = Conv2D(96, (3, 3), padding='valid',activation='relu')(x)    
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Dropout(0.5)(x)
    x = Dense(1024)(x)
    x = Dropout(0.5)(x)
    x = Dense(1024)(x)
    x = Dense(Constants.VOCAB_SIZE_CLASSIFICATION)(x)
    x = Activation('softmax')(x)
    return x


def getTrainedCnnModel(xInput,xOutput):
        cnnModel = Model(inputs = xInput, outputs = xOutput, name='cnnModel')
        return cnnModel
     