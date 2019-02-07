import Model.Model as Model
import Model.ModelAttention as ModelAttention 
import LoadData
import numpy as np


vocab,invVocab = LoadData.loadVocab('data/xml_vocab.txt')
'''
start=0
end=3
X, Yhot , YhotShiftedLeft = LoadData.loadData('data/tryImages/','./data/XmlTry.lst',vocab,start,end)
model,_,_,_=ModelAttention.createAndTrainModel(X, Yhot,YhotShiftedLeft)
model.summary()

Xtesting, YhotTesting , YhotShiftedLeftTesting = LoadData.loadData('data/tryImages/','./data/XmlTry.lst',vocab,0,3)
#ModelAttention.evaluateModel(X, Yhot,YhotShiftedLeft)
'''
ModelAttention.saveModelsForPrediction()


predFile=open("prediction.txt", 'w+')
outputSequnce=ModelAttention.makeAprediction('data/tryImages/1.png',vocab,invVocab)  #,cnnModel,encoderModel,decoderModel)
predFile.write(outputSequnce)
predFile.close()
