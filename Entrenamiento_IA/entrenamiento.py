from keras import models
import tensorflow as tf
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

model = models.Sequential()

model.add(Dense(1, input_dim=1))

model.compile(optimizer=Adam(learning_rate=0.8), loss='mean_squared_error')

model.summary()



