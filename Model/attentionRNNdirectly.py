import sys
sys.path.append('../')
from keras.layers import Bidirectional, Concatenate, Permute, Dot, Input, LSTM, Multiply
from keras.layers import RepeatVector, Dense, Activation, Lambda
from keras.optimizers import Adam
from keras.utils import to_categorical
from keras.models import load_model, Model
import keras.backend as K
import numpy as np
import Constants
import tensorflow as tf

def lamdbda_split(value):
    import sys
    sys.path.append('../')
    import Constants
    value=value[:,Constants.t,:]
    x = K.expand_dims(value, axis=1)
    return x

# Performs one step of attention: Outputs a context vector computed as a dot product of the attention weights
# "alphas" and the hidden states "a" of the Bi-LSTM.
def one_step_attention(a, s_prev,repeator,concatenator,densor1,densor2,activator,dotor):
    # Use repeator to repeat s_prev to be of shape (batch, Tx, n_s) so that you can concatenate it with all hidden states "a" 
    s_prev = repeator(s_prev)
    concat = concatenator([a,s_prev])
    # Use densor1 to propagate concat through a small fully-connected neural network to compute the "intermediate energies" variable e. 
    e = densor1(concat)
    # Use densor2 to propagate e through a small fully-connected neural network to compute the "energies" variable energies. 
    energies = densor2(e)
    # Use "activator" on "energies" to compute the attention weights "alphas" (≈ 1 line)
    alphas = activator(energies)
    # Use dotor together with "alphas" and "a" to compute the context vector to be given to the next (post-attention) LSTM-cell.
    context = dotor([alphas,a])
    return context

# Create the attention rnn layers to use them in training the model.
def createAttentionRnn(attentionInputs,s0,c0,postAttentionInputs):
    s = s0
    c = c0
    # Defined shared layers as global variables
    repeator = RepeatVector(Constants.CNN_FINAL_H*Constants.CNN_FINAL_W)
    concatenator = Concatenate(axis=-1)
    densor1 = Dense(Constants.MAX_SEQUENCE_LENGTH, activation = "tanh")
    densor2 = Dense(1, activation = "relu")
    activator = Activation('softmax', name='attention_weights') 
    dotor = Dot(axes = 1)
    lambdaLayer=Lambda(lamdbda_split)
    concatenatorPost=Concatenate(axis=-1)
    post_activation_LSTM_cell = LSTM(Constants.CNN_FINAL_DEPTH, return_state = True)
    output_layer = Dense(Constants.VOCAB_SIZE, activation='softmax')
    
    outputs = []
    for t in range(Constants.MAX_SEQUENCE_LENGTH):
        Constants.t=t
        context = one_step_attention(attentionInputs, s,repeator,concatenator,densor1,densor2,activator,dotor)
        #slicedPostAttentionInputs = Lambda(lambda x: x[:, t, :])(postAttentionInputs)
        postAttentionInputsT = lambdaLayer(postAttentionInputs)
        contextAndInput = concatenatorPost([postAttentionInputsT, context ])
        s, _, c = post_activation_LSTM_cell(contextAndInput,initial_state=[s,c])
        out = output_layer(s)
        outputs.append(out)
    return outputs,repeator,concatenator,densor1,densor2,activator,dotor,concatenatorPost,post_activation_LSTM_cell,output_layer



# Create the attention from the trained layers to use in prediction.
def getTrainedattentionRnnModel(repeator,concatenator,densor1,densor2,activator,dotor,s0,c0,concatenatorPost,post_activation_LSTM_cell,output_layer):
    attentionInputs = Input(shape=(Constants.CNN_FINAL_H*Constants.CNN_FINAL_W, Constants.CNN_FINAL_DEPTH))
    postAttentionInputs = Input(shape=(1, Constants.VOCAB_SIZE))

    context = one_step_attention(attentionInputs, s0,repeator,concatenator,densor1,densor2,activator,dotor)
    contextAndInput = concatenatorPost([postAttentionInputs , context ])
    s, _, c = post_activation_LSTM_cell(contextAndInput,initial_state=[s0,c0])
    out = output_layer(s)
    attentionRnnModel = Model([attentionInputs,postAttentionInputs,s0,c0], [out,s,c], name='attentionRnnModel')
    
    return attentionRnnModel