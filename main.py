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
        self.canvas_A = CanvasEscritura(root, 1, "A")
        self.canvas_X = CanvasEscritura(root, 2, "X")
        self.canvas_B = CanvasEscritura(root, 3, "B")

        # Frame de botones y resultado
        self.boton_frame = tk.Frame(root)
        self.boton_frame.pack(pady=10)

        tk.Button(self.boton_frame, text="Predecir", command=self.predecir_todo).pack(side=tk.LEFT, padx=10)
        tk.Button(self.boton_frame, text="Mostrar Resultado", command=self.mostrar_resultados).pack(side=tk.LEFT)

        # Label para mostrar el resultado final
        self.resultado_label = tk.Label(root, text="=", font=("Comic Sans", 100, "bold"), fg="black")
        self.resultado_label.pack(pady=20)

    def interpretar_operador(self, x):
        if x in [0, 1, 2]:
            return "+"
        elif x in [3, 4, 5]:
            return "-"
        elif x in [6, 7]:
            return "*"
        elif x in [8, 9]:
            return "/"
        else:
            return "?"

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
                    return "Error: División por cero"
                return round(a / b, 2)
            else:
                return "No se puede evaluar esta operación."
        except Exception as e:
            return f"Error al evaluar: {e}"

    def predecir_todo(self):
        self.canvas_A.predecir()
        self.canvas_X.predecir()
        self.canvas_B.predecir()

    def mostrar_resultados(self):
        A = self.canvas_A.valor
        X = self.canvas_X.valor
        B = self.canvas_B.valor

        print(f"\n--- Resultados actuales ---")
        print(f"A = {A}")
        print(f"X = {X}")
        print(f"B = {B}")

        if A is not None and X is not None and B is not None:
            operador = self.interpretar_operador(X)
            operacion_str = f"{A} {operador} {B}"
            print(f"\nOperación interpretada: {operacion_str}")

            if operador in ["+", "-", "*", "/"]:
                resultado = self.resolver_operacion(A, operador, B)
                self.resultado_label.config(text=f"{resultado}")
                print(f"{resultado}")
            else:
                self.resultado_label.config(text="Resultado: Operador no válido para calcular")
                print("No se puede resolver esta operación (operador no válido para cálculo).")
        else:
            self.resultado_label.config(text="Resultado: Datos incompletos")
            print("Falta uno o más valores para interpretar la operación.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Canvas x3 con Evaluación General y Resultado")
    app = App(root)
    root.mainloop()
