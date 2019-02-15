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

def createAndTrainModelPredictedSequence(X,YshiftedLeft,vocab):
    cnnInput=Input(shape=(Constants.IMAGE_SIZE,Constants.IMAGE_SIZE,3))
    decoderInputs = Input(shape=(None, Constants.VOCAB_SIZE)) # Note it will be (1,1,vocab_size)
    
    encoderInputs=CNN.createCNN(cnnInput)
    
    decoderOutputs,encoderStates,decoderLstm,decoderDense,encoderLstm \
    =EncoderDecoderRNN.createEncoderDecoderRNNfromPrediction(encoderInputs,decoderInputs)
    
    model = Model([cnnInput, decoderInputs], decoderOutputs,name='UI2XML')
    
    model.compile(optimizer='adam', loss='categorical_crossentropy' , metrics=['categorical_accuracy'])
    YshiftedLeft = list(YshiftedLeft.swapaxes(0,1))
    startSeq = np.zeros((X.shape[0], 1, Constants.VOCAB_SIZE))
    startSeq[:, 0, vocab['\t']] = 1.
    print("startSeq = "+str(startSeq.shape))
    model.fit([X,startSeq], YshiftedLeft,
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
    
def evaluateModel(xTest,yTest,yTestShiftedLeft,fromPrediction=False,vocab=None):
    model = load_model('UI2XML.h5')
    evaluate=[]
    if fromPrediction == True:
        yTestShiftedLeft = list(yTestShiftedLeft.swapaxes(0,1))
        startSeq = np.zeros((xTest.shape[0], 1, Constants.VOCAB_SIZE))
        startSeq[:, 0, vocab['\t']] = 1.
        evaluate =model.evaluate(x = [xTest,startSeq], y = yTestShiftedLeft)
    else:
        evaluate =model.evaluate(x = [xTest,yTest], y = yTestShiftedLeft)
    print(model.metrics_names)
    print ("Evaluation = " + str(evaluate))

def evaluateUsingPredictionShorterPadding(xTest,yTest,vocab,invVocab,predictionSeq=False):
    totalModelAccuracy=0
    cnnModel = load_model('cnnModel.h5')
    encoderModel = load_model('encoderModel.h5')
    decoderModel = load_model('decoderModel.h5')
    from0_50=0
    from50_60=0
    from60_75=0
    from75_85=0
    from85_100=0
    accuracies=[]
    YTestShiftedLeft=[yTest[i][1:len(yTest[i])]+['<pad>'] for i in range(len(yTest))]
    for i in range(len(xTest)):
        outputSequnce=makeAprediction(vocab,invVocab,None,xTest[i],False,predictionSeq,cnnModel,encoderModel,decoderModel) 
        outputSequnce=outputSequnce.split()
        if len(YTestShiftedLeft[i]) > len(outputSequnce):
            outputSequnce=outputSequnce+(['<pad>']*(len(YTestShiftedLeft[i])-len(outputSequnce)))
        else:
            YTestShiftedLeft[i]=YTestShiftedLeft[i]+(['<pad>']*(len(outputSequnce)-len(YTestShiftedLeft[i])))
        accuracy=np.mean(np.asarray(YTestShiftedLeft[i])==np.asarray(outputSequnce))
        totalModelAccuracy+=accuracy
        accuracies.append(accuracy)
        accuracy=accuracy*100
        if accuracy>0 and accuracy<=50:
            from0_50+=1
        elif accuracy>50 and accuracy<=60:
            from50_60+=1
        elif accuracy>60 and accuracy<=75:
            from60_75+=1
        elif accuracy>75 and accuracy<=85:
            from75_85+=1
        elif accuracy>85 and accuracy<=100:
            from85_100+=1
    print("Calculated accuracy = "+str(totalModelAccuracy/len(xTest)))
    print("From0_50 = "+str(from0_50))
    print("From50_60 = "+str(from50_60))
    print("From60_75 = "+str(from60_75))
    print("From75_85 = "+str(from75_85))
    print("From85_100 = "+str(from85_100))
    print(accuracies)
    
def evaluateUsingPrediction(xTest,yTest,yTestShiftedLeft,vocab,invVocab,predictionSeq=False):
    totalModelAccuracy=0
    cnnModel = load_model('cnnModel.h5')
    encoderModel = load_model('encoderModel.h5')
    decoderModel = load_model('decoderModel.h5')
    from0_50=0
    from50_60=0
    from60_75=0
    from75_85=0
    from85_100=0
    accuracies=[]
    for i in range(len(xTest)):
        outputSequnce=makeAprediction(vocab,invVocab,None,xTest[i],False,predictionSeq,cnnModel,encoderModel,decoderModel) 
        Y=[]
        Y.append(outputSequnce)
        yPred,yPredShifted=LoadData.preprocessY(Y,vocab)
        accuracy=np.mean(np.equal(np.argmax(yTestShiftedLeft[i], axis=-1),np.argmax(yPredShifted, axis=-1)))
        totalModelAccuracy+=accuracy
        accuracies.append(accuracy)
        accuracy=accuracy*100
        if accuracy>0 and accuracy<=50:
            from0_50+=1
        elif accuracy>50 and accuracy<=60:
            from50_60+=1
        elif accuracy>60 and accuracy<=75:
            from60_75+=1
        elif accuracy>75 and accuracy<=85:
            from75_85+=1
        elif accuracy>85 and accuracy<=100:
            from85_100+=1
    print("Calculated accuracy = "+str(totalModelAccuracy/len(xTest)))
    print("From0_50 = "+str(from0_50))
    print("From50_60 = "+str(from50_60))
    print("From60_75 = "+str(from60_75))
    print("From75_85 = "+str(from75_85))
    print("From85_100 = "+str(from85_100))
    print(accuracies)
    
def evaluateUsingBleu(xTest,yTest,vocab,invVocab,predictionSeq=False):
    cnnModel = load_model('cnnModel.h5')
    encoderModel = load_model('encoderModel.h5')
    decoderModel = load_model('decoderModel.h5')
    predicted=list()
    for i in range(len(xTest)):
        outputSequnce=makeAprediction(vocab,invVocab,None,xTest[i],False,predictionSeq,cnnModel,encoderModel,decoderModel) 
        predicted.append(outputSequnce.split())
    print("Bleu accuracy = "+str(corpus_bleu(yTest, predicted)))

       
# TODO : Remove the models from the arguments and uncomment them inside func.
def makeAprediction(vocab,invVocab,imgPath=None,inputImage=None,pathGiven=True,predictionSeq=False,cnnModel=None,encoderModel=None,decoderModel=None ):
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
        if predictionSeq==False:
            sampledTokenIndex = sampledTokenIndex [0][0]
        else:
             sampledTokenIndex = sampledTokenIndex [0]
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
    
    

    

