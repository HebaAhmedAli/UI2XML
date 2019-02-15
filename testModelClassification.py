import ModelClassification.Model as Model
import LoadDataClassification
import numpy as np


vocab,invVocab = LoadDataClassification.loadVocab('data/vocab_classification.txt')
X,Y=LoadDataClassification.loadData('data/SampleData/',vocab,0,3)
Model.createAndTrainCNNModel(X,Y)
X,Y=LoadDataClassification.loadData('data/SampleData/',vocab,0,3)
Model.evaluateModel(X,Y)
Model.makeAprediction(invVocab,'data/SampleData/1-android.widget.CheckBox.png')