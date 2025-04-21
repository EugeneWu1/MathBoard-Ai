import os
import numpy as np
from PIL import Image
import h5py
from tqdm import tqdm

# Configuración de rutas, tamaño de imagen y archivo de salida
data_dir = 'math_symbols/train'  # Directorio principal de las imágenes organizadas por clase(signos)
image_size = (64, 64) # Tamaño al que se redimensionarán las imágenes
output_file = 'dataset.h5' # Nombre del archivo HDF5 de salida

# Obtener las clases (subdirectorios), ordenadas alfabéticamente
classes = sorted(os.listdir(data_dir))
class_to_index = {cls: idx for idx, cls in enumerate(classes)}  # Mapeo de clase a índice numérico

# Listas para almacenar imágenes y etiquetas
images = []
labels = []

print("Leyendo imágenes y creando dataset...")

# Recorrer cada clase
for cls in classes:
    class_dir = os.path.join(data_dir, cls)
    if not os.path.isdir(class_dir):
        continue  # Saltar si no es un directorio

    # Recorrer cada archivo de imagen dentro de la clase
    for file in tqdm(os.listdir(class_dir), desc=f"Clase: {cls}"):
        if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg'):
            img_path = os.path.join(class_dir, file)
            
            # Abrir la imagen, convertir a escala de grises y redimensionar
            img = Image.open(img_path).convert('L')  # 'L' convierte a escala de grises
            img = img.resize(image_size)
            
            # Convertir a array de NumPy y normalizar valores a [0, 1]
            img_array = np.array(img) / 255.0
            images.append(img_array)
            
            # Agregar la etiqueta correspondiente
            labels.append(class_to_index[cls])

# Convertir las listas a arrays de NumPy y darles forma adecuada
X = np.array(images).reshape(-1, image_size[0], image_size[1], 1)  # Añadir canal de un solo color (grises)
y = np.array(labels)

# Guardar datos en un archivo HDF5
with h5py.File(output_file, 'w') as f:
    f.create_dataset('images', data=X) # Dataset de imágenes
    f.create_dataset('labels', data=y) # Dataset de etiquetas
    f.create_dataset('class_names', data=np.string_(classes)) # Nombres de las clases como strings

print(f"\n✅ Dataset guardado como {output_file}")
