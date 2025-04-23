import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Simplemente carga y devuelve el modelo previamente guardado
def cargar_modelo():
    return load_model("model/cnn_digits.h5")  # O el modelo que ya tengas guardado

def predecir_imagen(path_imagen, modelo):
    img = Image.open(path_imagen).convert("L").resize((28, 28)) # Escala de grises
    img = np.array(img) 
    img = 255 - img  # Invertir blanco/negro
    img = img / 255.0
    img = img.reshape(1, 28, 28, 1)
    prediccion = modelo.predict(img)
    return np.argmax(prediccion)

# Este bloque solo se ejecuta si corres recognizer.py directamente
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
        layers.Dense(10, activation="softmax")
    ])

    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.fit(x_train, y_train, epochs=1, validation_data=(x_test, y_test))

    # Guardar modelo entrenado
    model.save("model/cnn_digits.h5")
