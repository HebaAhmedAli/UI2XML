import sys
sys.path.append('../')
import Model.EncoderDecoderRNN as EncoderDecoderRNN
import Model.CNN as CNN
from keras.layers import Input
from keras.models import Model,load_model
import keras.backend as K
import numpy as np
import Utils
import Constants 
import Preprocessing

# TODO : Modify this to match attention model.

def createAndTrainModel(X,Y,YshiftedLeft):
    cnnInput=Input(shape=(Constants.IMAGE_SIZE,Constants.IMAGE_SIZE,3))
    decoderInputs = Input(shape=(None, Constants.VOCAB_SIZE))
    
    encoderInputs=CNN.createCNN(cnnInput)
    
    decoderOutputs,encoderStates,decoderLstm,decoderDense,encoderLstm \
    =EncoderDecoderRNN.createEncoderDecoderRNN(encoderInputs,decoderInputs)
    
    model = Model([cnnInput, decoderInputs], decoderOutputs,name='UI2XML')
    
    model.compile(optimizer='sgd', loss='categorical_crossentropy' , metrics=['accuracy'])
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

       
# TODO : Remove the models from the arguments and uncomment them inside func.
def makeAprediction(imgPath,vocab,invVocab ): #,cnnModel,encoderModel,decoderModel):
    inputImage = Preprocessing.imageReadAndPreprocessing(imgPath)
    cnnModel = load_model('cnnModel.h5')
    encoderModel = load_model('encoderModel.h5')
    decoderModel = load_model('decoderModel.h5')
    inputImage = np.expand_dims(inputImage, 0)
    print("image to predict shape: "+str(inputImage.shape))
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
    

    
