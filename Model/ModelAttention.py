import sys
sys.path.append('../')
import Model.attentionRNN as attentionRNN
import Model.CNN as CNN
from keras.layers import Input
from keras.models import Model,load_model
from keras.optimizers import Adam
import keras.backend as K
import numpy as np
import Utils
import Constants 
import Preprocessing

# TODO : Modify this to match attention model.

def createAndTrainModel(X,Y,YshiftedLeft):
    n_a = 32
    n_s = 64
    cnnInput=Input(shape=(Constants.IMAGE_SIZE,Constants.IMAGE_SIZE,3))
    postAttentionInputs = Input(shape=(None, Constants.VOCAB_SIZE))
    s0 = Input(shape=(n_s,), name='s0')
    c0 = Input(shape=(n_s,), name='c0')
    
    attentionInputs=CNN.createCNN(cnnInput)
    
    outputs,biLstm,repeator,concatenator,densor1,densor2,activator,dotor \
    ,concatenatorPost,post_activation_LSTM_cell,output_layer \
    =attentionRNN.createAttentionRnn(attentionInputs,s0,c0,postAttentionInputs,n_a,n_s)
    
    model = Model([cnnInput, postAttentionInputs , s0 ,c0], outputs,name='UI2XMLattention')
    
    opt = Adam(lr=Constants.LEARNING_RATE, beta_1=0.9, beta_2=0.999, decay=Constants.LR_DECAY)
    model.compile(optimizer=opt, loss='categorical_crossentropy' , metrics=['accuracy'])
    s0 = np.zeros((Constants.BATCH_SIZE, n_s))
    c0 = np.zeros((Constants.BATCH_SIZE, n_s))
    #outputs = list(Yoh.swapaxes(0,1))
    model.fit([X, Y,s0,c0], YshiftedLeft,
          batch_size=Constants.BATCH_SIZE,
          epochs=Constants.EPOCHS,
          validation_split=0.2)
    # Save model
    model.save('UI2XMLattention.h5')
    
    # Models to used in prediction.
    cnnModelForPrediction=CNN.getTrainedCnnModel(cnnInput,attentionInputs)
    biDirectionalModel,attentionRnnModel \
    =attentionRNN.getTrainedEncoderDecoderModel(biLstm,repeator,concatenator,densor1,densor2,activator,dotor,postAttentionInputs,s0,c0,concatenatorPost,post_activation_LSTM_cell,output_layer,n_a)
    cnnModelForPrediction.save('cnnModel.h5')
    biDirectionalModel.save('biDirectionalModel.h5')
    attentionRnnModel.save('attentionRnnModel.h5')
    return model,cnnModelForPrediction,biDirectionalModel,attentionRnnModel
    
def evaluateModel(xTest,yTest,yTestShiftedLeft):
    model = load_model('UI2XMLattention.h5')
    n_s = 64
    s0 = np.zeros((Constants.BATCH_SIZE, n_s))
    c0 = np.zeros((Constants.BATCH_SIZE, n_s))
    evaluate =model.evaluate(x = [xTest,yTest,s0,c0], y = yTestShiftedLeft)
    print ("Loss = " + str(evaluate[0]))
    print ("Test Accuracy = " + str(evaluate[1]))

       
# TODO : Complete this function.
def makeAprediction(imgPath,vocab,invVocab ): #,cnnModel,encoderModel,decoderModel):
    inputImage = Preprocessing.imageReadAndPreprocessing(imgPath)
    cnnModel = load_model('cnnModel.h5')
    biDirectionalModel = load_model('biDirectionalModel.h5')
    attentionRnnModel = load_model('attentionRnnModel.h5')
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
    

    

