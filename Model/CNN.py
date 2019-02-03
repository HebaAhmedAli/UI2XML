import sys
sys.path.append('../')
from keras.layers import Conv2D, MaxPooling2D, BatchNormalization, Activation,Lambda, Permute
from keras.models import Sequential, Model
from keras.optimizers import RMSprop
import keras.backend as K
import numpy as np

def lamdbda_split(value):
    import tensorflow as tf
    x = K.expand_dims(value, 4)
    #(batch_size,rows,cols,depth,?)
    x1 = tf.split(x, num_or_size_splits=x.shape[1], axis=1)  #(batch_size,1,cols,depth)
    x = K.concatenate(x1, 4)        #(batch_size,1,cols,depth,rows)
    x2 = tf.split(x, num_or_size_splits=x.shape[2], axis=2)  #(batch_size,1,1,depth)
    x = K.concatenate(x2, 4)        #(batch_size,1,1,depth,rows*col)
    x = K.squeeze(x,axis=1)
    x = K.squeeze(x,axis=1)
    return x

def createCNN(xInput):
    x = Conv2D(64, (3, 3), padding='valid', activation='relu',data_format="channels_last")(xInput)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Conv2D(128, (3, 3), padding='valid', activation='relu',data_format="channels_last")(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    x = Conv2D(256, (3, 3), padding='valid',data_format="channels_last")(x)
    x = BatchNormalization(axis = 3)(x)
    x = Activation('relu')(x)
    x = Conv2D(256, (3, 3), padding='valid', activation='relu',data_format="channels_last")(x)
    x = MaxPooling2D(pool_size=(2, 1))(x)
    x = Conv2D(512, (3, 3), padding='valid',data_format="channels_last")(x)
    x = BatchNormalization(axis = 3)(x)
    x = Activation('relu')(x)
    x = MaxPooling2D(pool_size=(1, 2))(x)
    x = Conv2D(512, (3, 3), padding='valid',data_format="channels_last")(x)
    x = BatchNormalization(axis = 3)(x)
    x = Activation('relu')(x)
    x = Lambda(lamdbda_split)(x)
    x = Permute((2,1))(x)
    return x


def getTrainedCnnModel(xInput,xOutput):
        cnnModel = Model(inputs = xInput, outputs = xOutput, name='cnnModel')
        return cnnModel
     
    