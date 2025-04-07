import tkinter as tk
from PIL import Image, ImageDraw
from recognizer import cargar_modelo, predecir_imagen


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Canvas de Escritura")
        self.canvas_width = 400
        self.canvas_height = 200

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # Imagen para guardar lo que se dibuja
        self.image = Image.new("L", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind("<B1-Motion>", self.paint)

        tk.Button(root, text="Guardar como imagen", command=self.guardar).pack(pady=10)
        tk.Button(root, text="Limpiar", command=self.limpiar).pack()

    def paint(self, event):
        x, y = event.x, event.y
        r = 8  # radio del trazo
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")
        self.draw.ellipse([x - r, y - r, x + r, y + r], fill="black")

    def guardar(self):
        self.image.save("dibujo.png")
        print("Imagen guardada como dibujo.png")
        modelo = cargar_modelo()
        resultado = predecir_imagen("dibujo.png", modelo)
        print("Predicción del modelo:", resultado)

    def limpiar(self):
        self.canvas.delete("all")
        self.draw.rectangle([0, 0, self.canvas_width, self.canvas_height], fill="white")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
