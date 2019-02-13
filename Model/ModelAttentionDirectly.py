import sys
sys.path.append('../')
import Model.attentionRNNdirectly as attentionRNNdirectly
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
    cnnInput=Input(shape=(Constants.IMAGE_SIZE,Constants.IMAGE_SIZE,3))
    postAttentionInputs = Input(shape=(None, Constants.VOCAB_SIZE))
    s0 = Input(shape=(Constants.CNN_FINAL_DEPTH,), name='s0')
    c0 = Input(shape=(Constants.CNN_FINAL_DEPTH,), name='c0')
    
    attentionInputs=CNN.createCNN(cnnInput)
    
    outputs,repeator,concatenator,densor1,densor2,activator,dotor \
    ,concatenatorPost,post_activation_LSTM_cell,output_layer \
    =attentionRNNdirectly.createAttentionRnn(attentionInputs,s0,c0,postAttentionInputs)
    
    model = Model([cnnInput, postAttentionInputs , s0 ,c0], outputs,name='UI2XMLattention')
    
    opt = Adam(lr=Constants.LEARNING_RATE, beta_1=0.9, beta_2=0.999, decay=Constants.LR_DECAY)
    model.compile(optimizer=opt, loss='categorical_crossentropy' , metrics=['accuracy'])
    sInitial = np.zeros((X.shape[0], Constants.CNN_FINAL_DEPTH))
    cInitial = np.zeros((X.shape[0], Constants.CNN_FINAL_DEPTH))
    YshiftedLeft = list(YshiftedLeft.swapaxes(0,1))
    
    model.fit([X, Y,sInitial,cInitial], YshiftedLeft,
          batch_size=Constants.BATCH_SIZE,
          epochs=Constants.EPOCHS,
          validation_split=0.2)
    # Save model
    model.save('UI2XMLattentionDirectly.h5')
    
    # Models to used in prediction.
    cnnModelForPrediction=CNN.getTrainedCnnModel(cnnInput,attentionInputs)
    attentionRnnModel \
    =attentionRNNdirectly.getTrainedattentionRnnModel(repeator,concatenator,densor1,densor2,activator,dotor,s0,c0,concatenatorPost,post_activation_LSTM_cell,output_layer)
    cnnModelForPrediction.save('cnnModel.h5')
    attentionRnnModel.save('attentionRnnModelDirectly.h5')
    return model,cnnModelForPrediction,attentionRnnModel
    
def evaluateModel(xTest,yTest,yTestShiftedLeft):
    model = load_model('UI2XMLattentionDirectly.h5')
    s0 = np.zeros((xTest.shape[0], Constants.CNN_FINAL_DEPTH))
    c0 = np.zeros((xTest.shape[0], Constants.CNN_FINAL_DEPTH))
    yTestShiftedLeft = list(yTestShiftedLeft.swapaxes(0,1))
    evaluate =model.evaluate(x = [xTest,yTest,s0,c0], y = yTestShiftedLeft)
    print(model.metrics_names)
    print ("Evaluation = " + str(evaluate))

       
# TODO : Complete this function.
def makeAprediction(vocab,invVocab,imgPath): #,cnnModel,encoderModel,decoderModel):
    inputImage = Preprocessing.imageReadAndPreprocessing(imgPath)
    cnnModel = load_model('cnnModel.h5')
    attentionRnnModel = load_model('attentionRnnModelDirectly.h5')
    inputImage = np.expand_dims(inputImage, 0)
    print("image to predict shape: "+str(inputImage.shape))
    attentionInputs = cnnModel.predict(inputImage)
    
    s0 = np.zeros((1, Constants.CNN_FINAL_DEPTH))
    c0 = np.zeros((1, Constants.CNN_FINAL_DEPTH))
    s=s0
    c=c0
    targetSeq = np.zeros((1, 1, Constants.VOCAB_SIZE))
    targetSeq[0, 0, vocab['\t']] = 1.
    stopCondition = False
    outputIndices = []
    while not stopCondition:
        outputToken, s, c = attentionRnnModel.predict([attentionInputs,targetSeq,s,c])

        # Sample a token
        sampledTokenIndex = np.argmax(outputToken,axis=-1)
        sampledTokenIndex = sampledTokenIndex[0]
        outputIndices.append(sampledTokenIndex)
        # Exit condition: either hit max length
        # or find stop character.
        if (invVocab[sampledTokenIndex] == '\n' or
           len(outputIndices) > Constants.MAX_SEQUENCE_LENGTH):
            stopCondition = True
        # Update the target sequence (of length 1).
        targetSeq = np.zeros((1, 1, Constants.VOCAB_SIZE))
        targetSeq[0, 0, sampledTokenIndex] = 1.

        
    outputSequnce = Utils.indicesToSequence(outputIndices , invVocab)
    return outputSequnce


def saveModelsForPrediction():
    # Models to used in prediction.
    model = load_model('UI2XMLattentionDirectly.h5')
    cnnInput=model.input[0]   # input_1 layer in model
    s0 = model.input[2] 
    c0 = model.input[3] 
    attentionInputs=model.layers[19].output #output of permute layer in cnn
    repeator=model.layers[20]
    concatenator=model.layers[21]
    densor1=model.layers[22]
    densor2=model.layers[23]
    activator=model.layers[25]
    dotor=model.layers[27]
    concatenatorPost=model.layers[28]
    post_activation_LSTM_cell=model.layers[30]
    output_layer=model.layers[31]
    cnnModelForPrediction=CNN.getTrainedCnnModel(cnnInput,attentionInputs)
    attentionRnnModel \
    =attentionRNNdirectly.getTrainedattentionRnnModel(repeator,concatenator,densor1,densor2,activator,dotor,s0,c0,concatenatorPost,post_activation_LSTM_cell,output_layer)
    cnnModelForPrediction.save('cnnModel.h5')
    attentionRnnModel.save('attentionRnnModel.h5')
    return 
    

    

