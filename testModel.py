import Model.Model as Model
import LoadData

vocab,invVocab = LoadData.loadVocab('data/xml_vocab.txt')
X, Yhot , YhotShiftedLeft = LoadData.loadData('data/tryImages/','data/XmlTry.lst',vocab)

model,cnnModel,encoderModel,decoderModel=Model.createAndTrainModel(X, Yhot,YhotShiftedLeft)
model.summary()
evaluate =model.evaluate(x = [X, Yhot], y = YhotShiftedLeft)
print ("Loss = " + str(evaluate[0]))
print ("Test Accuracy = " + str(evaluate[1]))
# TODO: To be changed.
#Model.evaluateModel(X, Yhot,YhotShiftedLeft)

predFile=open("prediction.txt", 'w+')
outputSequnce=Model.makeAprediction('data/tryImages/1.png',vocab,invVocab,cnnModel,encoderModel,decoderModel)
predFile.write(outputSequnce)
predFile.close()

