import tkinter as tk
from tkinter import ttk
import sympy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para crear una interfaz de entrada de matriz
def crear_interfaz_matriz(frame, label_text):
    label = tk.Label(frame, text=label_text)
    label.pack()
    entrada_text = tk.Text(frame, height=5, width=30)
    entrada_text.pack()
    return entrada_text

# Función para encontrar la inversa de una matriz
def calcular_inversa():
    matriz = entrada_text.get("1.0", "end-1c")
    matriz = matriz.split('\n')
    matriz = [[float(x) for x in row.split()] for row in matriz if row]
    try:
        matriz = sympy.Matrix(matriz)
        resultado.set('\n'.join([' '.join([str(int(val)) for val in row]) for row in matriz.inv().tolist()]))
    except Exception as e:
        resultado.set("Error: " + str(e))

# Función para multiplicar matrices
def multiplicar_matrices():
    matriz_a = entrada_text_a.get("1.0", "end-1c")
    matriz_b = entrada_text_b.get("1.0", "end-1c")
    matriz_a = matriz_a.split('\n')
    matriz_a = [[float(x) for x in row.split()] for row in matriz_a if row]
    matriz_b = matriz_b.split('\n')
    matriz_b = [[float(x) for x in row.split()] for row in matriz_b if row]
    try:
        resultado_matriz = sympy.Matrix(matriz_a) * sympy.Matrix(matriz_b)
        resultado.set('\n'.join([' '.join([str(int(val)) for val in row]) for row in resultado_matriz.tolist()]))
    except Exception as e:
        resultado.set("Error: " + str(e))

# Función para resolver sistemas de ecuaciones
def resolver_sistema():
    ecuaciones = entrada_text_ecuaciones.get("1.0", "end-1c")
    print("Ec: ", ecuaciones)  # Imprimir las ecuaciones en la consola
    ecuaciones = ecuaciones.split('\n')
    try:
        coeficientes = []
        resultados = []
        for eq in ecuaciones:
            if eq:
                eq = eq.replace(" ", "")  # Eliminar espacios en blanco
                parts = eq.split('=')
                coeficientes.append([float(i) for i in parts[0].split(',')])
                resultados.append(float(parts[1]))
        coeficientes = np.array(coeficientes)
        resultados = np.array(resultados)
        solucion = np.linalg.solve(coeficientes, resultados)
        resultado.set("Solución:\n" + '\n'.join([f'X{i+1} = {sol:.2f}' for i, sol in enumerate(solucion)]))
    except Exception as e:
        resultado.set("Error: " + str(e))
        
# Función para graficar las ecuaciones
def graficar():
    ecuaciones = entrada_text_ecuaciones.get("1.0", "end-1c")
    print("Ec: ", ecuaciones)  # Imprimir las ecuaciones en la consola
    ecuaciones = ecuaciones.split('\n')
    try:
        coeficientes = []
        resultados = []
        for eq in ecuaciones:
            if eq:
                eq = eq.replace(" ", "")  # Eliminar espacios en blanco
                parts = eq.split('=')
                coeficientes.append([float(i) for i in parts[0].split(',')])
                resultados.append(float(parts[1]))
        coeficientes = np.array(coeficientes)
        resultados = np.array(resultados)

        # Crear una nueva ventana para la gráfica
        grafica_ventana = tk.Toplevel(root)
        grafica_ventana.title("Gráfica del sistema de ecuaciones")

        # Crear la gráfica
        fig, ax = plt.subplots()
        x_vals = np.linspace(-10, 10, 400)
        for i in range(len(coeficientes)):
            y_vals = (resultados[i] - coeficientes[i][0]*x_vals) / coeficientes[i][1]
            ax.plot(x_vals, y_vals, label=f'Ecuación {i+1}')
        
        ax.legend()
        
        # Mostrar la gráfica en la ventana
        canvas = FigureCanvasTkAgg(fig, master=grafica_ventana)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        resultado.set("Error: " + str(e))

# Crear la ventana
root = tk.Tk()
root.title("Calculadora Matricial")

# Pestañas para diferentes operaciones
notebook = ttk.Notebook(root)
notebook.pack()

# Pestaña para encontrar la inversa de una matriz
inversa_tab = ttk.Frame(notebook)
notebook.add(inversa_tab, text="Inversa")

# Pestaña para multiplicación de matrices
multiplicacion_tab = ttk.Frame(notebook)
notebook.add(multiplicacion_tab, text="Multiplicación")

# Pestaña para resolver sistemas de ecuaciones
sistema_tab = ttk.Frame(notebook)
notebook.add(sistema_tab, text="Sistema")

# Variables para los resultados
resultado = tk.StringVar()

# Interfaz para encontrar la inversa de una matriz
entrada_text = crear_interfaz_matriz(inversa_tab, "Ingrese la matriz (una fila por línea, valores separados por espacios):")
boton_inversa = tk.Button(inversa_tab, text="Calcular Inversa", command=calcular_inversa)
boton_inversa.pack()
resultado_inversa = tk.Label(inversa_tab, textvariable=resultado)
resultado_inversa.pack()

# Interfaz para multiplicación de matrices
entrada_text_a = crear_interfaz_matriz(multiplicacion_tab, "Matriz A (una fila por línea, valores separados por espacios):")
entrada_text_b = crear_interfaz_matriz(multiplicacion_tab, "Matriz B (una fila por línea, valores separados por espacios):")
boton_multiplicacion = tk.Button(multiplicacion_tab, text="Multiplicar Matrices", command=multiplicar_matrices)
boton_multiplicacion.pack()
resultado_multiplicacion = tk.Label(multiplicacion_tab, textvariable=resultado)
resultado_multiplicacion.pack()

# Interfaz para resolver sistemas de ecuaciones
label_ecuaciones = tk.Label(sistema_tab, text="Ecuaciones (una por línea, en el formato 'expresión = valor'):")
label_ecuaciones.pack()
entrada_text_ecuaciones = tk.Text(sistema_tab, height=5, width=30)
entrada_text_ecuaciones.pack()
boton_resolver_sistema = tk.Button(sistema_tab, text="Resolver Sistema", command=resolver_sistema)
boton_resolver_sistema.pack()
boton_graficar_sistema = tk.Button(sistema_tab, text="Ir a Gráfica", command=graficar)
boton_graficar_sistema.pack()
resultado_sistema_label = tk.Label(sistema_tab, textvariable=resultado)
resultado_sistema_label.pack()

root.mainloop()
