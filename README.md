MathBoardAi

Es una aplicación interactiva que permite a los usuarios escribir números y operaciones matemáticas a mano en una pizarra digital. El sistema reconoce los caracteres escritos utilizando un modelo de inteligencia artificial entrenado y luego resuelve las operaciones matemáticas de manera automática.

## 📦 Requisitos del sistema

- [Visual Studio Code](https://code.visualstudio.com/) (o cualquier versión reciente recomendada)
- Python 3.12 o superior
- Sistema operativo: Windows, Linux o macOS

## 🚀 Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/EugeneWu1/MathBoard-Ai.git
cd mathboardAi

2. Crea un entorno virutal
En la terminal de visual studio code o terminal de sistema.
python -m venv venv

Para Windows:
venv\Scripts\activate

Para Linux/macOS
source venv/bin/activate

Instala las dependencias

pip install numpy
pip install opencv-python
pip install tensorflow
pip install pillow
pip install matplotlib
pip install tkinter


¿Cómo se usa?
1. Ejectua el archivo main.py, este cargara las interfaces de tkinter y los modelos, espera un poco.

2. Una vez aparezcan las interfaces podrás dibujar en este orden
-Primer lienzo: Solo dibujar números.
-Segundo lienzo: Solo dibujar signos matemáticos básicos (+,-,x,÷)
-Tercer lienzo: Solo dibujar números.

Para predecir la operación solo presiona el botón con el signo igual y obtendrás el resultado de la operación.