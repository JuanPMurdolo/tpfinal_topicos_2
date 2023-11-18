#Imports a utilizar
from tensorflow.keras import models #Crear/entrenar/evaluar el modelo
import tensorflow as tf
from tensorflow.keras.layers import Dense #Capas densas para la red
from tensorflow.keras.optimizers import Adam #Optimizador a utilizar
import numpy as np #Manejar los arreglos con los datos
import pandas as pd #Tomar el dataset y convertir datos categoricos
from sklearn.model_selection import train_test_split #Para separar train de test
import matplotlib.pyplot as plt #Para graficar


# # Parte 1: Celsius a Fahrenheit

# In[10]:


#Creo el modelo
model = models.Sequential()

#Añado la capa
model.add(Dense(1, input_dim=1))

#Compilo el modelo
model.compile(optimizer=Adam(learning_rate=0.1), loss="mse")

model.summary()


# In[11]:


#Los datos a usar
X = np.array([-40, 0, 15, 20, 25, 30, 55, 67, 12.5, 17.3])
Y = np.array([-40, 32, 59, 68, 77, 86, 131, 152.6, 54.5, 63.14])

#Separo los datos en training y testing
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size= 0.2)


# In[12]:


#Entreno la red
historial = model.fit(X_train,Y_train,epochs=1000)


# In[13]:


test_loss = model.evaluate(X_test, Y_test)
print(test_loss)


# In[14]:


#Grafico el loss a lo largo de las epochs
plt.xlabel("Número de época")
plt.ylabel("Pérdida/Loss")
plt.plot(historial.history["loss"])


# In[15]:


#Predicción de los primeros 3 elementos de entrenamiento
print("Datos a predecir:")
print(X_train[:3])
print("-----------------")
result = model.predict(X_train[:3])
print("Resultados obtenidos:")
print(result)
print("Valores correctos:")
print(Y_train[:3])


# In[16]:


print(model.get_weights())


# # Parte 2: SueldO


# In[18]:


#Creo el modelo
model = models.Sequential()

#Añado de a una capa
model.add(Dense(50, input_dim=6, activation="relu", kernel_initializer="random_normal"))
model.add(Dense(20, activation="relu"))
model.add(Dense(10, activation="relu"))

model.add(Dense(1, activation="relu"))


# In[19]:


#Compilo el modelo
model.compile(optimizer=Adam(learning_rate=0.1), loss="mse")


# In[20]:


model.summary()


# In[21]:


#Cargo el dataset
data = pd.read_csv("redesNeuronales/datos_empleados_50000.csv")

print(data)

#Pasa de 4 inputs a 6 -> Convierte Categoria en 3 entradas.
data = pd.get_dummies(data)
data=data.astype(np.float32)
print(data)


#Separo los datos de entrada X y los datos de salida Y
Y = np.array(data["sueldo"])
X = data.drop(["sueldo"], axis=1)
X = np.array(X.drop(data.columns[0], axis=1))

#Separo los datos en training y testing


X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size= 0.2)


# In[22]:


#Entreno la red
X_train = np.asarray(X_train).astype(np.float32)
Y_train = np.asarray(Y_train).astype(np.float32)
historial = model.fit(X_train,Y_train,epochs=5,batch_size=40)


# In[ ]:


test_loss = model.evaluate(X_test, Y_test)
print(test_loss)


# In[ ]:


#Grafico el loss a lo largo de las epochs
plt.xlabel("Número de época")
plt.ylabel("Pérdida/Loss")
plt.plot(historial.history["loss"])


# In[ ]:


#Predicción de los primeros 3 elementos de entrenamiento
print("Datos a predecir:")
print(X_train[:3])
print("-----------------")
result = model.predict(X_train[:3])
print("Resultados obtenidos:")
print(result)
print("Valores correctos:")
print(Y_train[:3])

import pickle
model_pkl_file = "model.pkl"  

with open(model_pkl_file, 'wb') as file:  
    pickle.dump(model, file)


model.save("model.keras")

params=np.array([[10600,2,1,0,1,0]])
result=model.predict(params)
print(result)