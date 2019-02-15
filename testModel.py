import Model.Model as Model
import Model.ModelAttentionDirectly as ModelAttentionDirectly 
import LoadData
import numpy as np


vocab,invVocab = LoadData.loadVocab('data/xml_vocab.txt')

start=0
end=3

X, Yhot , YhotShiftedLeft = LoadData.loadData('data/trainingImages/','./data/XmlTraining.lst',vocab,start,end)
model,_,_,_=Model.createAndTrainModel(X,Yhot,YhotShiftedLeft)
#model.summary()

X,Yhot = LoadData.loadDataForBleu('data/trainingImages/','data/XmlTraining.lst',vocab,0,3)
Model.evaluateUsingPredictionShorterPadding(X,Yhot,vocab,invVocab)
'''
Xtesting, YhotTesting , YhotShiftedLeftTesting = LoadData.loadData('data/tryImages/','./data/XmlTry.lst',vocab,0,3)
ModelAttentionDirectly.evaluateModel(X, Yhot,YhotShiftedLeft,True,vocab)

Model.saveModelsForPrediction()
Xtesting,Ytesting = LoadData.loadDataForBleu('data/trainingImages/','./data/XmlTraining.lst',vocab,0,3)
Model.evaluateUsingBleu(Xtesting,Ytesting,vocab,invVocab,True)

predFile=open("prediction.txt", 'w+')
outputSequnce=Model.makeAprediction(vocab,invVocab,'data/trainingImages/1.png',predictionSeq=True)  #,cnnModel,encoderModel,decoderModel)
predFile.write(outputSequnce)
predFile.close()

X, Yhot , YhotShiftedLeft = LoadData.loadData('data/trainingImages/','./data/XmlTraining.lst',vocab,start,end)
model,_,_=ModelAttentionDirectly.createAndTrainModel(X,Yhot,YhotShiftedLeft)
model.summary()

Xtesting, YhotTesting , YhotShiftedLeftTesting = LoadData.loadData('data/tryImages/','./data/XmlTry.lst',vocab,0,3)
ModelAttentionDirectly.evaluateModel(X, Yhot,YhotShiftedLeft)

ModelAttentionDirectly.saveModelsForPrediction()

predFile=open("prediction.txt", 'w+')
outputSequnce=ModelAttentionDirectly.makeAprediction(vocab,invVocab,'data/trainingImages/1.png')  #,cnnModel,encoderModel,decoderModel)
predFile.write(outputSequnce)
predFile.close()
''' 
