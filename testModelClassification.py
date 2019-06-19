import ModelClassification.Model as Model
import LoadDataClassification
import numpy as np


vocab,invVocab = LoadDataClassification.loadVocab('data/vocab_classification.txt')
'''
X,Y,auxFeatures=LoadDataClassification.loadData('data/SampleData/',vocab,0,3)
Model.createAndTrainCNNModel(X,auxFeatures,Y)
X,Y,auxFeatures=LoadDataClassification.loadData('data/SampleData/',vocab,0,3)
Model.evaluateModel(X,auxFeatures,Y)
'''
print(Model.makeAprediction(invVocab,np.array([0.6,1,1,0],dtype='float32'),imgPath='data/SampleData/1-android.widget.CheckBox.png'))