import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
import glob
import random
import numpy as np
from io import BytesIO

# Mapeo de símbolos mejorado, asi se estructuraran las carpetas
symbol_map = {
    '+': 'plus',
    '-': 'minus',
    '×': 'times',
    '÷': 'divide',
    '=': 'equals'
}

class AdvancedSymbolDrawer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Generador de Dataset de Símbolos Matemáticos")
        self.tk_image = None  # Para mantener referencia a la imagen
        
        # Configuración de variables
        self.symbol_var = tk.StringVar(value='+')
        self.brush_size = tk.IntVar(value=15)
        self.add_noise = tk.BooleanVar(value=False)
        self.random_rotate = tk.BooleanVar(value=True)
        
        # Interfaz
        self.create_widgets()
        self.setup_canvas()
        
        self.root.mainloop()
    
    def create_widgets(self):
        """Crea los controles de la interfaz"""
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)
        
        # Selector de símbolo
        ttk.Label(control_frame, text="Símbolo:").grid(row=0, column=0, sticky=tk.W)
        ttk.OptionMenu(control_frame, self.symbol_var, '+', *symbol_map.keys()).grid(row=0, column=1, sticky=tk.EW)
        
        # Control de grosor
        ttk.Label(control_frame, text="Grosor del pincel:").grid(row=1, column=0, sticky=tk.W)
        ttk.Scale(control_frame, from_=5, to=30, variable=self.brush_size).grid(row=1, column=1, sticky=tk.EW)
        
        # Opciones avanzadas
        ttk.Checkbutton(control_frame, text="Agregar ruido", variable=self.add_noise).grid(row=2, column=0, columnspan=2, sticky=tk.W)
        ttk.Checkbutton(control_frame, text="Rotación aleatoria", variable=self.random_rotate).grid(row=3, column=0, columnspan=2, sticky=tk.W)
        
        # Botones
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Guardar (Manual)", command=self.save_manual).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Generar Auto", command=self.generate_auto).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)
    
    def setup_canvas(self):
        """Configura el área de dibujo"""
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg='white', highlightthickness=1, highlightbackground="black")
        self.canvas.pack(pady=10)
        
        self.image = Image.new('L', (300, 300), 'white')
        self.draw = ImageDraw.Draw(self.image)
        
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset_prev_point)
        self.prev_point = None
    
    def paint(self, event):
        """Dibuja en el canvas"""
        x, y = event.x, event.y
        r = self.brush_size.get() // 2
        
        # Dibujar punto actual
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='black', outline='black')
        self.draw.ellipse([x-r, y-r, x+r, y+r], fill='black')
    
    def reset_prev_point(self, event):
        """Resetea el punto anterior al soltar el mouse"""
        self.prev_point = None
    
    def clear_canvas(self):
        """Limpia el canvas"""
        self.canvas.delete("all")
        self.image = Image.new('L', (300, 300), 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.tk_image = None  # Liberar referencia anterior
    
    def save_manual(self):
        """Guarda el símbolo dibujado manualmente"""
        symbol = self.symbol_var.get()
        self._save_image(symbol, "manual")
    
    def generate_auto(self):
        """Genera automáticamente variaciones del símbolo seleccionado"""
        symbol = self.symbol_var.get()
        num_variations = 10  # Número de variaciones a generar
        
        for i in range(num_variations):
            self.clear_canvas()
            self._draw_auto_symbol(symbol)
            self._save_image(symbol, f"auto_{i}")
        
        messagebox.showinfo("Generación completada", f"Se generaron {num_variations} variaciones de {symbol}")
    
    def _draw_auto_symbol(self, symbol):
        """Dibuja el símbolo automáticamente con variaciones"""
        font_size = random.randint(30, 50)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        
        # Posición aleatoria
        x = random.randint(50, 200)
        y = random.randint(50, 200)
        
        # Rotación aleatoria si está habilitada
        rotation = random.randint(-15, 15) if self.random_rotate.get() else 0
        
        # Dibujar texto en una imagen temporal
        temp_img = Image.new('L', (300, 300), 'white')
        temp_draw = ImageDraw.Draw(temp_img)
        temp_draw.text((x, y), symbol, fill='black', font=font)
        
        # Rotar si es necesario
        if rotation != 0:
            temp_img = temp_img.rotate(rotation, expand=0, fillcolor='white')
        
        # Combinar con la imagen principal
        self.image.paste(temp_img, (0, 0), temp_img)
        
        # Convertir la imagen para mostrarla en el canvas (SOLUCIÓN AL ERROR)
        img_bytes = BytesIO()
        self.image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Crear PhotoImage correctamente
        self.tk_image = tk.PhotoImage(data=img_bytes.read())  # Guardar como atributo
        self.canvas.create_image(0, 0, image=self.tk_image, anchor=tk.NW)
    
    def _save_image(self, symbol, prefix):
        """Guarda la imagen con el formato adecuado"""
        try:
            import cv2
            folder_name = f"math_symbols/test/{symbol_map[symbol]}"
            os.makedirs(folder_name, exist_ok=True)
            
            # Contar archivos existentes
            existing_files = glob.glob(os.path.join(folder_name, "*.png"))
            index = len(existing_files) + 1
            filename = f"{symbol_map[symbol]}_{prefix}_{index:04d}.png"
            save_path = os.path.join(folder_name, filename)
            
            # Preprocesamiento similar al entrenamiento
            processed_img = self._preprocess_image()
            processed_img.save(save_path)
            print(f"Imagen guardada: {save_path}")
        except ImportError:
            messagebox.showerror("Error", "OpenCV no está instalado. Instálalo con: pip install opencv-python")
    
    def _preprocess_image(self):
        """Preprocesa la imagen como en el entrenamiento"""
        # Redimensionar y binarizar
        img = self.image.resize((64, 64))
        
        # Convertir a array numpy para procesamiento
        img_array = np.array(img)
        
        # Umbral adaptativo
        img_array = cv2.adaptiveThreshold(img_array, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                        cv2.THRESH_BINARY_INV, 11, 2)
        
        # Agregar ruido si está habilitado
        if self.add_noise.get():
            noise = np.random.normal(0, 25, img_array.shape).astype(np.uint8)
            img_array = cv2.add(img_array, noise)
            img_array = np.clip(img_array, 0, 255)
        
        # Convertir de nuevo a imagen PIL
        return Image.fromarray(img_array)

if __name__ == "__main__":
    try:
        import cv2
        app = AdvancedSymbolDrawer()
    except ImportError:
        messagebox.showerror("Error", "OpenCV no está instalado. Instálalo con: pip install opencv-python")