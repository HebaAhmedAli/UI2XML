import sys
sys.path.append('../')
from keras.models import Model
from keras.layers import Input, LSTM, Dense
import Constants

# Create the encoder_decoder rnn layers to use them in training the model.
def createEncoderDecoderRNN(encoderInputs,decoderInputs):
    # Create the encoder_decoder rnn layers to use them in training the model.
    encoderLstm = LSTM(Constants.ENCODER_HIDDEN_UNITS, return_state=True)    
    encoderOutputs, stateH, stateC = encoderLstm(encoderInputs)
    # Discard `encoderOutputs` and only keep the states.
    encoderStates = [stateH, stateC]
    decoderLstm = LSTM(Constants.DECODER_HIDDEN_UNITS, return_sequences=True, return_state=True)
    decoderOutputs, _, _ = decoderLstm(decoderInputs,
                                     initial_state=encoderStates)
    decoderDense = Dense(Constants.VOCAB_SIZE, activation='softmax')
    decoderOutputs = decoderDense(decoderOutputs)
    return decoderOutputs,encoderStates,decoderLstm,decoderDense,encoderLstm
    
# Create the encoder & decoder models from the trained layers to use in prediction.
def getTrainedEncoderDecoderModel(encoderLstm,encoderStates,decoderInputs,decoderLstm,decoderDense):
    encoderInputs = Input(shape=(None , Constants.CNN_FINAL_DEPTH))
    encoderOutputs, encoderStateH, encoderStateC = encoderLstm(encoderInputs)
    encoderStates= [encoderStateH, encoderStateC]
    encoderModel = Model(encoderInputs, encoderStates, name='encoderModel')

    decoderStateInputH = Input(shape=(Constants.DECODER_HIDDEN_UNITS,))
    decoderStateInputC = Input(shape=(Constants.DECODER_HIDDEN_UNITS,))
    decoderStatesInputs = [decoderStateInputH, decoderStateInputC]
    decoderOutputs, stateH, stateC = decoderLstm(decoderInputs, initial_state=decoderStatesInputs)
    decoderStates = [stateH, stateC]
    decoderOutputs = decoderDense(decoderOutputs)
    decoderModel = Model(
    [decoderInputs] + decoderStatesInputs,
    [decoderOutputs] + decoderStates, name='decoderModel')
    return encoderModel,decoderModel
