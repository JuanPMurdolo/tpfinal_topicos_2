from keras import models
import tensorflow as tf
from keras.layers import Dense
from keras.optimizers import Adam
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# Cargamos el dataset
data = pd.read_csv("redesNeuronales/datos_de_pacientes_5000.csv")

# Separamos los datos de entrada X y los datos de salida Y
X = data.drop('riesgo_cardiaco', axis=1)
Y = data['riesgo_cardiaco']

# Normalizamos de los datos
scaler = MinMaxScaler()
X = scaler.fit_transform(X)

# Dividimos los datos en entrenamiento y prueba
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size=0.2, random_state=42)

# Creo el modelo
model = models.Sequential()

# Añado de a una capa
model.add(Dense(64, input_dim=7, activation="relu"))
model.add(Dense(64, activation="relu"))
model.add(Dense(1, activation="sigmoid"))

# Compilamos el modelo
model.compile(optimizer=Adam(),
              loss='binary_crossentropy', metrics='accuracy')

# Entrenamos el modelo
history = model.fit(X_train, Y_train, epochs=100,
                    batch_size=32, validation_data=(X_test, Y_test))

# Evaluamos el modelo
test_loss = model.evaluate(X_test, Y_test)
print(test_loss)

# Graficamos la precision del modelo en entrenamiento y testeo
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Precision del Modelo')
plt.ylabel('Precision')
plt.xlabel('Epocas')
plt.legend(['Entrenamiento', 'Prueba'], loc='upper left')
plt.show()

# Graficamos la perdida del modelo en entrenamiento y testeo
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Perdida del Modelo')
plt.ylabel('Perdida')
plt.xlabel('Epocas')
plt.legend(['Entrenamiento', 'Prueba'], loc='upper left')
plt.show()

# Predicción de los primeros 5 elementos de entrenamiento
print("Datos a predecir:")
print(X_train[:5])
print("-----------------")
result = model.predict(X_train[:5])
print("Resultados obtenidos:")
print(result)
print("Valores correctos:")
print(Y_train[:5])
