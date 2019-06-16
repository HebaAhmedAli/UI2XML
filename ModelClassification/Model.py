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

def scheduler(epoch): 
    lrate =0.001
    if epoch >= 1 and epoch<50:
        lrate=0.001
    elif epoch >=3 and epoch<75:
        lrate=pow(10,-5)
    elif epoch>=75:
        lrate=pow(10,-6)
    return lrate


def createAndTrainCNNModel(X,Y):
    cnnInput=Input(shape=(Constants.IMAGE_SIZE_CLASSIFICATION,Constants.IMAGE_SIZE_CLASSIFICATION,3))
    model=CNN.createCNNModel(cnnInput)
    lrSchedule = LearningRateScheduler(scheduler)
    opt=SGD(momentum=0.9, decay=0.0, nesterov=True)
    model.compile(optimizer=opt, loss='categorical_crossentropy' , metrics=['categorical_accuracy'])
    model.fit(x=X, y=Y, batch_size=Constants.BATCH_SIZE, epochs=Constants.EPOCHS, callbacks=[lrSchedule],validation_split=0.2)
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
    