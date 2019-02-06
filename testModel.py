import Model.Model as Model
import LoadData


vocab,invVocab = LoadData.loadVocab('data/xml_vocab.txt')

start=0
end=10
X, Yhot , YhotShiftedLeft = LoadData.loadData('data/trainingImages/','./data/XmlValidation.lst',vocab,start,end)
model,cnnModel,encoderModel,decoderModel=Model.createAndTrainModel(X, Yhot[start:min(end,len(Yhot))],YhotShiftedLeft[start:min(end,len(Yhot))])
model.summary()

#Xtesting, YhotTesting , YhotShiftedLeftTesting = LoadData.loadData('data/testingImages/','./data/XmlTesting.lst',vocab,0,3)
#Model.evaluateModel(X, Yhot,YhotShiftedLeft)

Model.saveModelsForPrediction()

predFile=open("prediction.txt", 'w+')
outputSequnce=Model.makeAprediction('data/tryImages/1.png',vocab,invVocab)  #,cnnModel,encoderModel,decoderModel)
predFile.write(outputSequnce)
predFile.close()

