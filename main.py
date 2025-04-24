import tkinter as tk
from PIL import Image, ImageDraw
from recognizer import cargar_modelo, predecir_imagen


class CanvasEscritura:
    def __init__(self, master, id_canvas, nombre_variable):
        self.canvas_width = 200
        self.canvas_height = 200
        self.id_canvas = id_canvas
        self.nombre_variable = nombre_variable
        self.valor = None  # Aquí se guarda la predicción

        self.frame = tk.Frame(master)
        self.frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.canvas = tk.Canvas(self.frame, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.image = Image.new("L", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind("<B1-Motion>", self.paint)

        tk.Button(self.frame, text="Limpiar", command=self.limpiar).pack(pady=5)

    def paint(self, event):
        x, y = event.x, event.y
        r = 8
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")
        self.draw.ellipse([x - r, y - r, x + r, y + r], fill="black")

    def predecir(self):
        filename = f"dibujo_{self.id_canvas}.png"
        self.image.save(filename)
        print(f"[{self.nombre_variable}] Imagen guardada como {filename}")
        modelo = cargar_modelo()
        self.valor = predecir_imagen(filename, modelo)
        print(f"[{self.nombre_variable}] Predicción:", self.valor)

    def limpiar(self):
        self.canvas.delete("all")
        self.draw.rectangle([0, 0, self.canvas_width, self.canvas_height], fill="white")


class App:
    def __init__(self, root):
        # Frame principal que contendrá todo
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(padx=10, pady=10)

        # Primer canvas (A) - izquierdo
        self.canvas_A = CanvasEscritura(self.main_frame, 1, "A")
        
        # Frame para los botones de operaciones (centro)
        self.boton_frame = tk.Frame(self.main_frame)
        self.boton_frame.pack(side=tk.LEFT, padx=20)
        
        # Crear botones de operaciones en una disposición 2x2
        self.boton_sumar = tk.Button(self.boton_frame, text="+", command=lambda: self.set_signo("+"), 
                                   font=("Comic Sans", 20), width=4, height=2)
        self.boton_sumar.grid(row=0, column=0, padx=5, pady=5)
        
        self.boton_rest = tk.Button(self.boton_frame, text="-", command=lambda: self.set_signo("-"), 
                                  font=("Comic Sans", 20), width=4, height=2)
        self.boton_rest.grid(row=0, column=1, padx=5, pady=5)
        
        self.boton_multip = tk.Button(self.boton_frame, text="*", command=lambda: self.set_signo("*"), 
                                     font=("Comic Sans", 20), width=4, height=2)
        self.boton_multip.grid(row=1, column=0, padx=5, pady=5)
        
        self.boton_divi = tk.Button(self.boton_frame, text="/", command=lambda: self.set_signo("/"), 
                                   font=("Comic Sans", 20), width=4, height=2)
        self.boton_divi.grid(row=1, column=1, padx=5, pady=5)
        
        # Segundo canvas (B) - derecho
        self.canvas_B = CanvasEscritura(self.main_frame, 2, "B")

        # Frame para el botón = y resultado
        self.result_frame = tk.Frame(self.main_frame)
        self.result_frame.pack(side=tk.LEFT, padx=10)

        # Botón = grande
        self.boton_igual = tk.Button(self.result_frame, text="=", command=self.mostrar_resultados, 
                                   font=("Comic Sans", 40), width=3, height=2)
        self.boton_igual.pack(side=tk.LEFT, padx=10)

        # Canvas para mostrar el resultado (del mismo tamaño que los otros canvas)
        self.resultado_canvas = tk.Canvas(self.result_frame, width=200, height=200, bg="white")
        self.resultado_canvas.pack(side=tk.LEFT)
        
        # Texto del resultado (centrado en el canvas)
        self.resultado_text = self.resultado_canvas.create_text(100, 100, text="", 
                                                              font=("Comic Sans", 80, "bold"), 
                                                              fill="black")

        self.X = None  # Variable para guardar el signo

        # Etiqueta para mostrar el signo seleccionado (X)
        self.signo_label = tk.Label(root, text="Signo seleccionado: ", font=("Comic Sans", 14))
        self.signo_label.pack(pady=10)

    def set_signo(self, signo):
        self.X = signo
        self.signo_label.config(text=f"Signo seleccionado: {self.X}")
        print(f"Signo seleccionado: {self.X}")

    def predecir(self):
        self.canvas_A.predecir()
        self.canvas_B.predecir()

    def mostrar_resultados(self):
        self.predecir()  # Primero predecimos los valores
        
        A = self.canvas_A.valor
        B = self.canvas_B.valor

        print(f"\n--- Resultados actuales ---")
        print(f"A = {A}")
        print(f"B = {B}")

        if A is not None and B is not None and self.X is not None:
            operador = self.X
            operacion_str = f"{A} {operador} {B}"
            print(f"\nOperación interpretada: {operacion_str}")

            if operador in ["+", "-", "*", "/"]:
                resultado = self.resolver_operacion(A, operador, B)
                # Actualizamos el texto en el canvas de resultado
                self.resultado_canvas.itemconfig(self.resultado_text, text=f"{resultado}")
                print(f"Resultado: {resultado}")
            else:
                self.resultado_canvas.itemconfig(self.resultado_text, text="Error")
                print("No se puede resolver esta operación (operador no válido para cálculo).")
        else:
            self.resultado_canvas.itemconfig(self.resultado_text, text="Error")
            print("Falta uno o más valores para interpretar la operación.")

    def resolver_operacion(self, a, operador, b):
        try:
            if operador == "+":
                return a + b
            elif operador == "-":
                return a - b
            elif operador == "*":
                return a * b
            elif operador == "/":
                if b == 0:
                    return "∞"  # Infinito para división por cero
                return round(a / b, 2)
            else:
                return "Error"
        except Exception as e:
            return f"Error"


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Calculadora con Reconocimiento de Dígitos")
    app = App(root)
    root.mainloop()