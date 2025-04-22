import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageOps
import numpy as np
import tensorflow as tf
import os

class MathSymbolRecognizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconocedor de Símbolos Matemáticos")
        
        # Configuración
        self.canvas_size = 300
        self.brush_size = 15
        self.model_path = 'model/symbol_model.h5'
        self.class_names = {
            0: '+ (Suma)',
            1: '- (Resta)',
            2: '× (Multiplicacion)',
            3: '÷ (Division)',
            4: '= (Igual)'
        }
        
        # Inicializar componentes
        self.init_ui()
        self.model = self.load_model()
        
    def init_ui(self):
        """Inicializa la interfaz de usuario"""
        # Canvas de dibujo
        self.canvas = tk.Canvas(self.root, width=self.canvas_size, height=self.canvas_size, 
                               bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas.pack(pady=20)
        
        # Imagen subyacente para procesamiento
        self.image = Image.new("L", (self.canvas_size, self.canvas_size), "white")
        self.draw = ImageDraw.Draw(self.image)
        
        # Controles
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        tk.Button(control_frame, text="Predecir", command=self.predict, 
                 width=12, bg="#4CAF50", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Limpiar", command=self.clear, 
                 width=12, bg="#f44336", fg="white").pack(side=tk.LEFT, padx=5)
        
        # Resultado
        self.result_label = tk.Label(self.root, text="Dibuje un símbolo (+,-,×,÷,=)", 
                                   font=('Arial', 14), pady=10)
        self.result_label.pack()
        
        # Eventos del ratón
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset_position)
        self.prev_point = None
        
    def load_model(self):
        """Carga el modelo de reconocimiento"""
        if not os.path.exists(self.model_path):
            messagebox.showerror("Error", f"Modelo no encontrado en: {self.model_path}")
            self.root.destroy()
            return None
            
        try:
            return tf.keras.models.load_model(self.model_path)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el modelo:\n{str(e)}")
            self.root.destroy()
            return None
    
    def paint(self, event):
        """Maneja el dibujo en el canvas"""
        x, y = event.x, event.y
        r = 10
        
        # Dibujar punto actual
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill="black", outline="black")
        self.draw.ellipse([x-r, y-r, x+r, y+r], fill="black")
        
    
    def reset_position(self, event):
        """Resetea la posición anterior al soltar el mouse"""
        self.prev_point = None
    
    def clear(self):
        """Limpia el canvas"""
        self.canvas.delete("all")
        self.image = Image.new("L", (self.canvas_size, self.canvas_size), "white")
        self.draw = ImageDraw.Draw(self.image)
        self.result_label.config(text="Dibuje un símbolo (+,-,×,÷,=)")
    
    def preprocess_image(self):
        """Prepara la imagen para la predicción"""
        img = self.image.resize((64, 64))
        img = ImageOps.invert(img)
        img_array = np.array(img) / 255.0
        return np.expand_dims(img_array, axis=(0, -1))
    
    def predict(self):
        """Realiza la predicción del símbolo dibujado"""
        if not self.model:
            return
            
        try:
            # Preprocesamiento y predicción
            img_array = self.preprocess_image()
            predictions = self.model.predict(img_array, verbose=0)
            class_id = np.argmax(predictions)
            confidence = np.max(predictions)
            
            # Mostrar resultado
            result = self.class_names.get(class_id, "Desconocido")
            self.result_label.config(
                text=f"Predicción: {result}\nConfianza: {confidence:.1%}",
                fg="green" if confidence > 0.7 else "orange"
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en la predicción:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MathSymbolRecognizer(root)
    root.mainloop()
