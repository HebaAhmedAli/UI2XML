import sys
sys.path.append('../')
import ModelClassification.CNN as CNN
from keras.layers import Input
from keras.models import Model,load_model
from keras.optimizers import SGD
