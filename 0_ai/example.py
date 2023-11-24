# Imports a utilizar
import pickle
from tensorflow.keras import models  # Crear/entrenar/evaluar el modelo
import tensorflow as tf
from tensorflow.keras.layers import Dense  # Capas densas para la red
from tensorflow.keras.optimizers import Adam  # Optimizador a utilizar
import numpy as np  # Manejar los arreglos con los datos
import pandas as pd  # Tomar el dataset y convertir datos categoricos
from sklearn.model_selection import train_test_split  # Para separar train de test
import matplotlib.pyplot as plt  # Para graficar

# Creo el modelo
model = models.Sequential()

# Añado de a una capa
model.add(Dense(500, input_dim=7, activation="relu",
          kernel_initializer="random_normal"))
model.add(Dense(200, activation="relu"))
model.add(Dense(1, activation="relu"))


# Compilo el modelo
model.compile(optimizer=Adam(learning_rate=0.1), loss="mse")


model.summary()


# Cargo el dataset
data = pd.read_csv("redesNeuronales/datos_de_pacientes_5000.csv")

print(data)

# Separo los datos de entrada X y los datos de salida Y
Y = np.array(data["riesgo_cardiaco"])
X = data.drop(["riesgo_cardiaco"], axis=1)
X = np.array(X)

# Separo los datos en training y testing
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)


# Entreno la red
X_train = np.asarray(X_train).astype(np.float32)
Y_train = np.asarray(Y_train).astype(np.float32)
historial = model.fit(X_train, Y_train, epochs=25, batch_size=40)


test_loss = model.evaluate(X_test, Y_test)
print(test_loss)

# Grafico el loss a lo largo de las epochs
plt.xlabel("Número de época")
plt.ylabel("Pérdida/Loss")
plt.plot(historial.history["loss"])


# Predicción de los primeros 3 elementos de entrenamiento
print("Datos a predecir:")
print(X_train[:3])
print("-----------------")
result = model.predict(X_train[:3])
print("Resultados obtenidos:")
print(result)
print("Valores correctos:")
print(Y_train[:3])

model_pkl_file = "model.pkl"

with open(model_pkl_file, 'wb') as file:
    pickle.dump(model, file)

model.save("model.keras")
