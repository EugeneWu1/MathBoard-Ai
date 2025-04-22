import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import GlobalAveragePooling2D

# Configuración del modelo y entrenamiento
input_shape = (64, 64, 1)   # Tamaño de entrada (64x64, escala de grises)
num_classes = 5             # Número de clases (+, -, ×, ÷ y =)
batch_size = 32             # Tamaño del batch
epochs = 27                 # Número máximo de épocas de entrenamiento

# Generadores de datos con aumentos para prevenir sobreajuste
train_datagen = ImageDataGenerator(
    rescale=1./255,                # Normaliza las imágenes a [0, 1]
    rotation_range=15,             # Rango de rotación aleatoria
    width_shift_range=0.1,         # Desplazamiento horizontal
    height_shift_range=0.1,        # Desplazamiento vertical
    shear_range=0.1,               # Cizallamiento
    zoom_range=0.1,                # Zoom aleatorio
    fill_mode='nearest'            # Método para rellenar los píxeles vacíos
)

# Generador para el conjunto de prueba (sin aumentos, solo normalización)
test_datagen = ImageDataGenerator(rescale=1./255)

# Generador de entrenamiento: carga imágenes desde el directorio
train_generator = train_datagen.flow_from_directory(
    'math_symbols/train', # Ruta al dataset de entrenamiento
    target_size=(64, 64), # Redimensiona las imágenes
    color_mode='grayscale', # Escala de grises
    batch_size=batch_size,
    class_mode='categorical' # Codificación one-hot para clasificación multiclase
)

# Generador de prueba
test_generator = test_datagen.flow_from_directory(
    'math_symbols/test', # Ruta al dataset de prueba
    target_size=(64, 64),
    color_mode='grayscale',
    batch_size=batch_size,
    class_mode='categorical'
)

# Definición del modelo CNN
model = Sequential([
    # Capa 1: convolución 
    Conv2D(32, (3,3), activation='relu', kernel_regularizer=l2(0.001), input_shape=input_shape),
    BatchNormalization(),
    MaxPooling2D((2,2)),

    # Capa 2
    Conv2D(64, (3,3), activation='relu', kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    MaxPooling2D((2,2)),

    # Capa 3
    Conv2D(128, (3,3), activation='relu', kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    MaxPooling2D((2,2)),

    # Capa 4
    Conv2D(256, (3,3), activation='relu', kernel_regularizer=l2(0.001)),
    BatchNormalization(),
    MaxPooling2D((2,2)),

    # Capa de pooling global
    GlobalAveragePooling2D(),

    # Capa densa con dropout
    Dense(128, activation='relu'),
    Dropout(0.5),

    # Capa de salida
    Dense(num_classes, activation='softmax')  # Softmax para clasificación multiclase
])

# Compilar el modelo
model.compile(optimizer=Adam(learning_rate=0.0005),   # Optimizador Adam
              loss='categorical_crossentropy',        # Función de pérdida para clasificación multiclase
              metrics=['accuracy'])                   # Métrica principal: precisión

# Callbacks para detener entrenamiento temprano y guardar mejor modelo
callbacks = [
    EarlyStopping(patience=5, restore_best_weights=True), # Evita sobreajuste
    ModelCheckpoint('model/symbol_model.h5', save_best_only=True) # Guarda el mejor modelo
]

# Entrenamiento del modelo
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=epochs,
    validation_data=test_generator,
    validation_steps=test_generator.samples // batch_size,
    callbacks=callbacks
)

# Guardar el modelo final
model.save('model/math_symbols_model.h5')
