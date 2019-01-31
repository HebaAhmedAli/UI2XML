import Constants 
import CNN
import EncoderDecoderRNN
from keras.layers import Input
from keras.models import Model

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
    
    
    
    



# TODO : Predict.
# Hint:  prediction = np.argmax(prediction, axis = -1)
#        outputSequnce = indicesToSequence(prediction , invVocab)

