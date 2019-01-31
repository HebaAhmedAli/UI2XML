from keras.models import Model
from keras.layers import Input, LSTM, Dense
import numpy as np
import Constants

# Create the encoder_decoder rnn layers to use them in training the model.
def createEncoderDecoderRNN(encoderInputs,decoderInputs):
    # Create the encoder_decoder rnn layers to use them in training the model.
    encoder = LSTM(Constants.ENCODER_HIDDEN_UNITS, return_state=True)    
    encoderOutputs, stateH, stateC = encoder(encoderInputs)
    # Discard `encoderOutputs` and only keep the states.
    encoderStates = [stateH, stateC]
    decoderLstm = LSTM(Constants.DECODER_HIDDEN_UNITS, return_sequences=True, return_state=True)
    decoderOutputs, _, _ = decoderLstm(decoderInputs,
                                     initial_state=encoderStates)
    decoderDense = Dense(Constants.VOCAB_SIZE, activation='softmax')
    decoderOutputs = decoderDense(decoderOutputs)
    return decoderOutputs,encoderStates,decoderLstm,decoderDense
    
# Create the encoder & decoder models from the trained layers to use in prediction.
def getTrainedEncoderDecoderModel(encoderInputs,encoderStates,decoderInputs,decoderLstm,decoderDense):
    encoderModel = Model(encoderInputs, encoderStates)

    decoderStateInputH = Input(shape=(Constants.DECODER_HIDDEN_UNITS,))
    decoderStateInputC = Input(shape=(Constants.DECODER_HIDDEN_UNITS,))
    decoderStatesInputs = [decoderStateInputH, decoderStateInputC]
    decoderOutputs, stateH, stateC = decoderLstm(decoderInputs, initial_state=decoderStatesInputs)
    decoderStates = [stateH, stateC]
    decoderOutputs = decoderDense(decoderOutputs)
    decoderModel = Model(
    [decoderInputs] + decoderStatesInputs,
    [decoderOutputs] + decoderStates)
    return encoderModel,decoderModel
