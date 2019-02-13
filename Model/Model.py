import sys
sys.path.append('../')
import Model.EncoderDecoderRNN as EncoderDecoderRNN
import Model.CNN as CNN
from keras.layers import Input
from keras.models import Model,load_model
from nltk.translate.bleu_score import corpus_bleu
import keras.backend as K
import numpy as np
import Utils
import Constants 
import Preprocessing
import LoadData



def createAndTrainModel(X,Y,YshiftedLeft):
    cnnInput=Input(shape=(Constants.IMAGE_SIZE,Constants.IMAGE_SIZE,3))
    decoderInputs = Input(shape=(None, Constants.VOCAB_SIZE))
    
    encoderInputs=CNN.createCNN(cnnInput)
    
    decoderOutputs,encoderStates,decoderLstm,decoderDense,encoderLstm \
    =EncoderDecoderRNN.createEncoderDecoderRNN(encoderInputs,decoderInputs)
    
    model = Model([cnnInput, decoderInputs], decoderOutputs,name='UI2XML')
    
    model.compile(optimizer='adam', loss='categorical_crossentropy' , metrics=['categorical_accuracy'])
    model.fit([X, Y], YshiftedLeft,
          batch_size=Constants.BATCH_SIZE,
          epochs=Constants.EPOCHS,
          validation_split=0.2)
    # Save model
    model.save('UI2XML.h5')
    
    # Models to used in prediction.
    cnnModelForPrediction=CNN.getTrainedCnnModel(cnnInput,encoderInputs)
    encoderModelForPrediction,decoderModelForPrediction \
    =EncoderDecoderRNN.getTrainedEncoderDecoderModel(encoderLstm,encoderStates,decoderInputs,decoderLstm,decoderDense)
    cnnModelForPrediction.save('cnnModel.h5')
    encoderModelForPrediction.save('encoderModel.h5')
    decoderModelForPrediction.save('decoderModel.h5')
    return model,cnnModelForPrediction,encoderModelForPrediction,decoderModelForPrediction
    
def evaluateModel(xTest,yTest,yTestShiftedLeft):
    model = load_model('UI2XML.h5')
    evaluate =model.evaluate(x = [xTest,yTest], y = yTestShiftedLeft)
    print ("Loss = " + str(evaluate[0]))
    print ("Test Accuracy = " + str(evaluate[1]))

def evaluateUsingPrediction(xTest,yTest,yTestShiftedLeft,vocab,invVocab):
    totalModelAccuracy=0
    cnnModel = load_model('cnnModel.h5')
    encoderModel = load_model('encoderModel.h5')
    decoderModel = load_model('decoderModel.h5')
    for i in range(len(xTest)):
        outputSequnce=makeAprediction(vocab,invVocab,None,xTest[i],False,cnnModel,encoderModel,decoderModel) 
        Y=[]
        Y.append(outputSequnce)
        yPred,yPredShifted=LoadData.preprocessY(Y,vocab)
        totalModelAccuracy+=np.mean(np.equal(np.argmax(yTestShiftedLeft[i], axis=-1),np.argmax(yPredShifted, axis=-1)))
    print("Calculated accuracy = "+str(totalModelAccuracy/len(xTest)))
    
def evaluateUsingBleu(xTest,yTest,vocab,invVocab):
    cnnModel = load_model('cnnModel.h5')
    encoderModel = load_model('encoderModel.h5')
    decoderModel = load_model('decoderModel.h5')
    predicted=list()
    for i in range(len(xTest)):
        outputSequnce=makeAprediction(vocab,invVocab,None,xTest[i],False,cnnModel,encoderModel,decoderModel) 
        predicted.append(outputSequnce.split())
    print("Bleu accuracy = "+str(corpus_bleu(yTest, predicted)))

       
# TODO : Remove the models from the arguments and uncomment them inside func.
def makeAprediction(vocab,invVocab,imgPath=None,inputImage=None,pathGiven=True,cnnModel=None,encoderModel=None,decoderModel=None ):
    if pathGiven == True:
        inputImage = Preprocessing.imageReadAndPreprocessing(imgPath)
        cnnModel = load_model('cnnModel.h5')
        encoderModel = load_model('encoderModel.h5')
        decoderModel = load_model('decoderModel.h5')

    
    inputImage = np.expand_dims(inputImage, 0)
    #print("image to predict shape: "+str(inputImage.shape))
    encoderInputs = cnnModel.predict(inputImage)
    statesValue = encoderModel.predict(encoderInputs)
    
    targetSeq = np.zeros((1, 1, Constants.VOCAB_SIZE))
    targetSeq[0, 0, vocab['\t']] = 1.
    stopCondition = False
    outputIndices = []
    while not stopCondition:
        outputToken, h, c = decoderModel.predict([targetSeq] + statesValue)

        # Sample a token
        sampledTokenIndex = np.argmax(outputToken,axis=-1)
        sampledTokenIndex = sampledTokenIndex [0][0]
        outputIndices.append(sampledTokenIndex)
        # Exit condition: either hit max length
        # or find stop character.
        if (invVocab[sampledTokenIndex] == '\n' or
           len(outputIndices) > Constants.MAX_SEQUENCE_LENGTH):
            stopCondition = True
        # Update the target sequence (of length 1).
        targetSeq = np.zeros((1, 1, Constants.VOCAB_SIZE))
        targetSeq[0, 0, sampledTokenIndex] = 1.
        # Update states
        statesValue = [h, c]
        
    outputSequnce = Utils.indicesToSequence(outputIndices , invVocab)
    return outputSequnce
    
def saveModelsForPrediction():
    # Models to used in prediction.
    model = load_model('UI2XML.h5')
    cnnInput=model.input[0]   # input_1 layer in model
    encoderInputs=model.layers[18].output #output of permute layer in cnn
    decoderInputs=model.input[1]       # input_2 layer in model    
    encoderLstm=model.layers[20]
    _, stateH, stateC = encoderLstm(encoderInputs)
    encoderStates=[stateH, stateC]
    decoderLstm=model.layers[21]
    decoderDense=model.layers[22]
    cnnModelForPrediction=CNN.getTrainedCnnModel(cnnInput,encoderInputs)
    encoderModelForPrediction,decoderModelForPrediction \
    =EncoderDecoderRNN.getTrainedEncoderDecoderModel(encoderLstm,encoderStates,decoderInputs,decoderLstm,decoderDense)
    cnnModelForPrediction.save('cnnModel.h5')
    encoderModelForPrediction.save('encoderModel.h5')
    decoderModelForPrediction.save('decoderModel.h5')
    return 
    
    

    

