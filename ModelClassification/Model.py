import sys
sys.path.append('../')
import ModelClassification.CNN as CNN
from keras.layers import Input
from keras.models import Model,load_model
from keras.optimizers import SGD
from keras.callbacks import LearningRateScheduler
import Constants
import Preprocessing
import numpy as np


def createAndTrainCNNModel(X,Y):
    cnnInput=Input(shape=(Constants.IMAGE_SIZE_CLASSIFICATION,Constants.IMAGE_SIZE_CLASSIFICATION,3))
    model=CNN.createCNNModel(cnnInput)
    # from 0 to 50 epochs 
    opt=SGD(lr=0.001,momentum=0.9, decay=0.0, nesterov=True)
    model.compile(optimizer=opt, loss='categorical_crossentropy' , metrics=['categorical_accuracy'])
    model.fit(x=X, y=Y, batch_size=Constants.BATCH_SIZE, epochs=50,validation_split=0.2)
    # from 50 to 75
    opt=SGD(lr=0.00001,momentum=0.9, decay=0.0, nesterov=True)
    model.compile(optimizer=opt, loss='categorical_crossentropy' , metrics=['categorical_accuracy'])
    model.fit(x=X, y=Y, batch_size=Constants.BATCH_SIZE, epochs=25,validation_split=0.2)
    
    # from 75 to 100 epochs 
    opt=SGD(lr=0.000001,momentum=0.9, decay=0.0, nesterov=True)
    model.compile(optimizer=opt, loss='categorical_crossentropy' , metrics=['categorical_accuracy'])
    model.fit(x=X, y=Y, batch_size=Constants.BATCH_SIZE, epochs=25,validation_split=0.2)
    
    model.save('UI2XMLclassification.h5')
    return model

def evaluateModel(xTest,yTest):
    model = load_model('UI2XMLclassification.h5')
    evaluate =model.evaluate(x = xTest, y = yTest)
    print(model.metrics_names)
    print ("Evaluation = " + str(evaluate))
    
def makeAprediction(invVocab,image=None,model=None,imgPath=None):
    if model==None:
        model = load_model('data/ourModel/UI2XMLclassification245000_98_91.h5')
    inputImage = Preprocessing.imageReadAndPreprocessingClassification(imgPath,image)
    inputImage = np.expand_dims(inputImage, 0)
    output = model.predict(inputImage)
    outputIndex = np.argmax(output,axis=-1)
    #print("Prediction = "+invVocab[outputIndex[0]])
    return invVocab[outputIndex[0]]
    