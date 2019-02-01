import Constants 
import CNN
import EncoderDecoderRNN
from keras.layers import Input
from keras.models import Model,load_model
import Utils
import Preprocessing
import sys
import numpy as np
sys.path.append('../')


def createAndTrainModel(X,Y,YshiftedLeft):
    cnnInput=Input(shape=(Constants.IMAGE_SIZE,Constants.IMAGE_SIZE,3))
    decoderInputs = Input(shape=(None, Constants.VOCAB_SIZE))
    
    encoderInputs=CNN.createCNN(cnnInput)
    
    decoderOutputs,encoderStates,decoderLstm,decoderDense \
    =EncoderDecoderRNN.createEncoderDecoderRNN(encoderInputs,decoderInputs)
    
    model = Model([cnnInput, decoderInputs], decoderOutputs)
    
    model.compile(optimizer='sgd', loss='categorical_crossentropy')
    model.fit([X, Y], YshiftedLeft,
          batch_size=Constants.BATCH_SIZE,
          epochs=Constants.EPOCHS,
          validation_split=0.2)
    # Save model
    model.save('UI2XML.h5')
    
    # Models to used in prediction.
    cnnModelForPrediction=CNN.getTrainedCnnModel(cnnInput,encoderInputs)
    encoderModelForPrediction,decoderModelForPrediction \
    =EncoderDecoderRNN.getTrainedEncoderDecoderModel(encoderInputs,encoderStates,decoderInputs,decoderLstm,decoderDense)
    cnnModelForPrediction.save('cnnModel.h5')
    encoderModelForPrediction.save('encoderModel.h5')
    decoderModelForPrediction.save('decoderModel.h5')
    return model
    
def evaluateModel(xTest,yTest,yTestShiftedLeft):
    model = load_model('UI2XML.h5')
    evaluate =model.evaluate(x = [xTest,yTest], y = yTestShiftedLeft)
    print ("Loss = " + str(evaluate[0]))
    print ("Test Accuracy = " + str(evaluate[1]))

       
# TODO : Predict.
def makeAprediction(imgPath,vocab,invVocab):
    inputImage = Preprocessing.preprocessing(imgPath)
    cnnModel = load_model('cnnModel.h5')
    encoderModel = load_model('encoderModel.h5')
    decoderModel = load_model('decoderModel.h5')
    
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
    

    

