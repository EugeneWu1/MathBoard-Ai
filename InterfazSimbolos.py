import tkinter as tk
from PIL import Image, ImageDraw
import os
import glob

# Mapeo de símbolos a nombres de carpeta
symbol_map = {
    '+': 'plus',
    '-': 'minus',
    '×': 'times',
    '÷': 'divide',
    '=': 'equals'
}

class MathSymbolDrawer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Dibujar Símbolos Matemáticos")

        # Selector de símbolo
        self.symbol_var = tk.StringVar(self.root)
        self.symbol_var.set('+')  # Valor por defecto
        tk.OptionMenu(self.root, self.symbol_var, *symbol_map.keys()).pack()

        # Canvas de dibujo
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg='white')
        self.canvas.pack()

        self.image = Image.new('L', (300, 300), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind("<B1-Motion>", self.paint)

        tk.Button(self.root, text="Guardar", command=self.save).pack()
        tk.Button(self.root, text="Limpiar", command=self.clear).pack()

        self.root.mainloop()

    def paint(self, event):
        x, y = event.x, event.y
        r = 5
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill='black')
        self.draw.ellipse([x - r, y - r, x + r, y + r], fill='black')

    def save(self):
        symbol = self.symbol_var.get()
        folder_name = f"math_symbols/train/{symbol_map[symbol]}"
        os.makedirs(folder_name, exist_ok=True)

        # Obtener número de archivo para no sobreescribir
        existing_files = glob.glob(os.path.join(folder_name, "*.png"))
        index = len(existing_files) + 1
        filename = f"{symbol_map[symbol]}_{index:03d}.png"
        save_path = os.path.join(folder_name, filename)

        # Redimensionar la imagen a 64x64 para el modelo
        resized_image = self.image.resize((64, 64))
        resized_image.save(save_path)
        print(f"Guardado en: {save_path}")

        self.clear()

    def clear(self):
        self.canvas.delete("all")
        self.image = Image.new('L', (300, 300), 'white')
        self.draw = ImageDraw.Draw(self.image)

# Ejecutar la interfaz
MathSymbolDrawer()
