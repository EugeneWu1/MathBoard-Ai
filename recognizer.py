import tensorflow as tf #Biblioteca para crear y entrenar modelos de aprendizaje profundo
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Cargar dataset de dígitos
#mnist.load_data() carga el dataset MNIST
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Normalizar imágenes
#Divide los valores de píxeles (0-255) entre 255 para llevarlos a rango [0, 1]
x_train = x_train / 255.0
x_test = x_test / 255.0

# Expandir dimensiones para CNN
x_train = x_train[..., None]
x_test = x_test[..., None]

# Modelo CNN simple
model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)), #28,28,1 son las dimensiones de las imagenes
    layers.MaxPooling2D(2, 2), #Reduccion de dimensiones  2x2
    layers.Conv2D(64, (3, 3), activation="relu"),
    layers.MaxPooling2D(2, 2),
    layers.Flatten(), #Aplana la salida para la capa densa
    layers.Dense(64, activation="relu"), #Capa oculta con 64 neuronas
    layers.Dense(10, activation="softmax")  # 10 neuronas para 10 dígitos (0-9)
])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

# Guardar modelo
model.save("model/modelo_digits.h5")

#Simplemente carga y devuelve el modelo previamente guardado
def cargar_modelo():
    return load_model("model/modelo_digits.h5")

def predecir_imagen(path_imagen, modelo):
    img = Image.open(path_imagen).convert("L").resize((28, 28)) #L es escala de grises
    img = np.array(img) 
    img = 255 - img  # invertir si es fondo blanco y número negro
    img = img / 255.0 #Escalar [0,1]
    img = img.reshape(1, 28, 28, 1)
    prediccion = modelo.predict(img)
    return np.argmax(prediccion)

if __name__ == "__main__":
    # Cargar dataset de dígitos
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    # Normalizar imágenes
    x_train = x_train / 255.0
    x_test = x_test / 255.0

    # Expandir dimensiones para CNN
    x_train = x_train[..., None]
    x_test = x_test[..., None]

    # Modelo CNN simple
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation="relu", input_shape=(28, 28, 1)),
        layers.MaxPooling2D(2, 2),
        layers.Conv2D(64, (3, 3), activation="relu"),
        layers.MaxPooling2D(2, 2),
        layers.Flatten(),
        layers.Dense(64, activation="relu"),
        layers.Dense(10, activation="softmax")  # Para 10 dígitos (0-9)
    ])

    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))

    # Guardar modelo
    model.save("model/modelo_digits.h5")
