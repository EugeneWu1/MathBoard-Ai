import os
import numpy as np
from PIL import Image
import h5py
from tqdm import tqdm

# Configuración
data_dir = 'math_symbols/train'
image_size = (64, 64)
output_file = 'dataset.h5'

# Obtener clases (ordenadas alfabéticamente)
classes = sorted(os.listdir(data_dir))
class_to_index = {cls: idx for idx, cls in enumerate(classes)}

images = []
labels = []

print("Leyendo imágenes y creando dataset...")
for cls in classes:
    class_dir = os.path.join(data_dir, cls)
    if not os.path.isdir(class_dir):
        continue

    for file in tqdm(os.listdir(class_dir), desc=f"Clase: {cls}"):
        if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg'):
            img_path = os.path.join(class_dir, file)
            img = Image.open(img_path).convert('L')  # Escala de grises
            img = img.resize(image_size)
            img_array = np.array(img) / 255.0  # Normalización
            images.append(img_array)
            labels.append(class_to_index[cls])

# Convertir a arrays
X = np.array(images).reshape(-1, image_size[0], image_size[1], 1)
y = np.array(labels)

# Guardar en HDF5
with h5py.File(output_file, 'w') as f:
    f.create_dataset('images', data=X)
    f.create_dataset('labels', data=y)
    f.create_dataset('class_names', data=np.string_(classes))

print(f"\n✅ Dataset guardado como {output_file}")
