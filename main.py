import tkinter as tk #Biblioteca para crear interfaces en python
from PIL import Image, ImageDraw #Para manipulacion de imagenes
from recognizer import cargar_modelo, predecir_imagen #Modulo personalizado que contiene funciones para cargar un modelo y hacer predicciones


class App:
    def __init__(self, root):
        self.root = root #root es la ventana principal
        self.root.title("Canvas de Escritura") #Titulo de la ventana
        self.canvas_width = 400  #Ancho
        self.canvas_height = 200 #Alto

        #Creacion de la pizarra con las dimensiones anteriores
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack() #Lo coloca en la ventana principal

        # Imagen para guardar lo que se dibuja
        self.image = Image.new("L", (self.canvas_width, self.canvas_height), "white") 
        self.draw = ImageDraw.Draw(self.image)  #Para poder dibujar sobre la imagen

        self.canvas.bind("<B1-Motion>", self.paint)#Vincular el mov del raton con el click izquierdo

        tk.Button(root, text="Predecir", command=self.guardar).pack(pady=10)#Boton para guardar y predecir
        tk.Button(root, text="Limpiar", command=self.limpiar).pack() #Boton para limpiar

    #Se ejecuta cuando estamo presionando el click izquierdo
    def paint(self, event):
        x, y = event.x, event.y
        r = 8  # radio del trazo
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="black") #Diubja un circulo negro en el canvas visible
        self.draw.ellipse([x - r, y - r, x + r, y + r], fill="black") #Dibuja el mismo circulo en la imagen subyacente

    def guardar(self):
        self.image.save("dibujo.png") #Guarda la imagen com dibuj
        print("Imagen guardada como dibujo.png")
        modelo = cargar_modelo() #Cargar el modelo de reconocimiento (modulo_mnist.h5)
        resultado = predecir_imagen("dibujo.png", modelo) #Pasa la imagen al modelo para obtener una prediccion
        print("Predicción del modelo:", resultado) #Muestra el resultado en consola

    #Borra todo el contenido en la pizarra
    def limpiar(self):
        self.canvas.delete("all")
        self.draw.rectangle([0, 0, self.canvas_width, self.canvas_height], fill="white")

#Ejecucion principal
if __name__ == "__main__":
    root = tk.Tk() #Crea la ventana principal
    app = App(root) #Instancia de App
    root.mainloop() #Inicio del bucle principal de la interfaz
