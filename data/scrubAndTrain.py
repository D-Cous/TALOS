import numpy as np
import pandas as pd
import numpy
from numpy import random
import matplotlib.pyplot as plt
import sklearn

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers import GRU



def scrubAndTrain(asset, file):
    
    #enter your pre-processing logic for the training data

    #------------------------------------------------------------------------------------------

    #create your model and train it

    #save model
    model.save(saveFilePath)


    #------------------------------------------------------------------------------------------

    #calculate results and send to a csv

    results.to_csv('data/trainingData/' + resultFile)
    
    #--------------------------------------------------------------------------------