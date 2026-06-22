import math
import itertools
import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def evaluar_funcion(funcion_texto, x):
    nombres_permitidos = {
        "x": x,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
        "log": math.log,
        "ln": math.log,
        "exp": math.exp,
        "pi": math.pi,
        "e": math.e,
        "abs": abs
    }

    return eval(funcion_texto, {"__builtins__": None}, nombres_permitidos)


def error_porcentual(valor_nuevo, valor_anterior):
    if valor_nuevo == 0:
        return abs(valor_nuevo - valor_anterior)

    return abs((valor_nuevo - valor_anterior) / valor_nuevo) * 100


def error_vectorial_maximo(nuevos, anteriores):
    errores = []

    for i in range(len(nuevos)):
        if nuevos[i] == 0:
            error = abs(nuevos[i] - anteriores[i])
        else:
            error = abs((nuevos[i] - anteriores[i]) / nuevos[i]) * 100

        errores.append(error)

    return max(errores)


# =====================================================
# DOMINANCIA DIAGONAL
# =====================================================

def matriz_es_diagonalmente_dominante(A):
    n = len(A)

    for i in range(n):
        diagonal = abs(A[i][i])
        suma_otros = 0

        for j in range(n):
            if j != i:
                suma_otros += abs(A[i][j])

        if diagonal < suma_otros:
            return False

    return True


def intentar_reordenar_dominancia(A, b):
    n = len(A)

    indices = list(range(n))

    for permutacion in itertools.permutations(indices):
        nueva_A = []
        nueva_b = []

        for indice in permutacion:
            nueva_A.append(A[indice])
            nueva_b.append(b[indice])

        if matriz_es_diagonalmente_dominante(nueva_A):
            return nueva_A, nueva_b, permutacion

    return A, b, None


# =====================================================
# EJEMPLOS PRECARGADOS
# =====================================================

ejemplos_newton = [
    {
        "nombre": "Ej. 1 — 1/e^x - x",
        "f": "1/exp(x) - x",
        "df": "-exp(-x) - 1",
        "x0": "0",
        "error": "1",
        "iteraciones": "20"
    },
    {
        "nombre": "Ej. 2 — 1/e^x - ln(x)",
        "f": "1/exp(x) - log(x)",
        "df": "-exp(-x) - 1/x",
        "x0": "1",
        "error": "1",
        "iteraciones": "20"
    },
    {
        "nombre": "Ej. 3 — e^(-2x) - 5x",
        "f": "exp(-2*x) - 5*x",
        "df": "-2*exp(-2*x) - 5",
        "x0": "0",
        "error": "1",
        "iteraciones": "20"
    },
    {
        "nombre": "Ej. 4 — x^3 - cos(x)",
        "f": "x**3 - cos(x)",
        "df": "3*x**2 + sin(x)",
        "x0": "0.5",
        "error": "1",
        "iteraciones": "20"
    }
]


ejemplos_secante = [
    {
        "nombre": "Ej. 1 — 1/e^x - x",
        "f": "1/exp(x) - x",
        "x0": "0",
        "x1": "1",
        "error": "1",
        "iteraciones": "20"
    },
    {
        "nombre": "Ej. 2 — 1/e^x - ln(x)",
        "f": "1/exp(x) - log(x)",
        "x0": "1",
        "x1": "2",
        "error": "1",
        "iteraciones": "20"
    },
    {
        "nombre": "Ej. 3 — e^(-2x) - 5x",
        "f": "exp(-2*x) - 5*x",
        "x0": "0",
        "x1": "1",
        "error": "1",
        "iteraciones": "20"
    },
    {
        "nombre": "Ej. 4 — x^3 - cos(x)",
        "f": "x**3 - cos(x)",
        "x0": "0.5",
        "x1": "1",
        "error": "1",
        "iteraciones": "20"
    }
]


ejemplos_punto_fijo = [
    {
        "nombre": "Ej. 1 — g(x) = 1/e^x",
        "g": "1/exp(x)",
        "x0": "0",
        "error": "1",
        "iteraciones": "20"
    },
    {
        "nombre": "Ej. 2 — g(x) = e^(1/e^x)",
        "g": "exp(1/exp(x))",
        "x0": "1",
        "error": "1",
        "iteraciones": "20"
    },
    {
        "nombre": "Ej. 3 — g(x) = e^(-2x)/5",
        "g": "exp(-2*x)/5",
        "x0": "0",
        "error": "1",
        "iteraciones": "20"
    },
    {
        "nombre": "Ej. 4 — g(x) = cos(x)^(1/3)",
        "g": "cos(x)**(1/3)",
        "x0": "0.5",
        "error": "1",
        "iteraciones": "20"
    }
]


ejemplos_sistemas = [
    {
        "nombre": "Ej. 1 — Sistema 3x3",
        "dimension": 3,
        "matriz": [
            [6, 1, 1, 9],
            [1, 6, 2, 15],
            [1, 1, -6, -3]
        ],
        "inicial": "0,0,0",
        "error": "1",
        "iteraciones": "20"
    },
    {
        "nombre": "Ej. 2 — Sistema 3x3",
        "dimension": 3,
        "matriz": [
            [2, -6, -1, -38],
            [-3, -1, 7, -34],
            [-8, -1, 7, -20]
        ],
        "inicial": "0,0,0",
        "error": "1",
        "iteraciones": "20"
    },
    {
        "nombre": "Ej. 3 — Sistema 3x3",
        "dimension": 3,
        "matriz": [
            [0.71, 0.1, -8.2, -56.4],
            [25, -0.9, -0.3, 20.2],
            [3.7, -7.3, -0.1, -18.9]
        ],
        "inicial": "0,0,0",
        "error": "1",
        "iteraciones": "20"
    }
]


# =====================================================
# APLICACIÓN
# =====================================================

class AppMetodosNumericos:
    def __init__(self, root):
        self.root = root
        self.root.title("Métodos Numéricos")
        self.root.geometry("1350x850")
        self.root.minsize(1200, 760)

        self.color_fondo = "#F3F4F6"
        self.color_card = "#FFFFFF"
        self.color_primario = "#2F2F2F"
        self.color_texto = "#111827"
        self.color_secundario = "#6B7280"

        self.fuente_titulo = ("Segoe UI", 28, "bold")
        self.fuente_subtitulo = ("Segoe UI", 13)
        self.fuente_normal = ("Segoe UI", 13)
        self.fuente_bold = ("Segoe UI", 14, "bold")
        self.fuente_codigo = ("Consolas", 13)
        self.fuente_matriz = ("Segoe UI", 14)

        self.root.configure(bg=self.color_fondo)

        self.metodo_var = tk.StringVar()
        self.ejemplo_var = tk.StringVar()
        self.dimension_var = tk.IntVar(value=3)

        self.entradas_matriz = []

        self.configurar_estilos()
        self.crear_ui()

    # =====================================================
    # ESTILOS
    # =====================================================

    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background=self.color_fondo)
        style.configure("Card.TFrame", background=self.color_card)

        style.configure(
            "TLabel",
            background=self.color_fondo,
            foreground=self.color_texto,
            font=self.fuente_normal
        )

        style.configure(
            "Card.TLabel",
            background=self.color_card,
            foreground=self.color_texto,
            font=self.fuente_normal
        )

        style.configure(
            "Title.TLabel",
            background=self.color_fondo,
            foreground=self.color_texto,
            font=self.fuente_titulo
        )

        style.configure(
            "Subtitle.TLabel",
            background=self.color_fondo,
            foreground=self.color_secundario,
            font=self.fuente_subtitulo
        )

        style.configure(
            "Header.TLabel",
            background=self.color_card,
            foreground=self.color_texto,
            font=self.fuente_bold
        )

        style.configure(
            "TButton",
            font=self.fuente_bold,
            padding=10
        )

        style.configure(
            "Primary.TButton",
            background=self.color_primario,
            foreground="white",
            borderwidth=0
        )

        style.map(
            "Primary.TButton",
            background=[("active", "#111111")]
        )

        style.configure(
            "TEntry",
            padding=9,
            fieldbackground="#F9FAFB",
            font=self.fuente_normal
        )

        style.configure(
            "TCombobox",
            padding=9,
            fieldbackground="#F9FAFB",
            font=self.fuente_normal
        )

    # =====================================================
    # INTERFAZ
    # =====================================================

    def crear_ui(self):
        contenedor = ttk.Frame(self.root, padding=18)
        contenedor.pack(fill="both", expand=True)

        encabezado = ttk.Frame(contenedor)
        encabezado.pack(fill="x", pady=(0, 15))

        ttk.Label(
            encabezado,
            text="Solucionador de Métodos Numéricos",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            encabezado,
            text="Selecciona un método, carga un ejemplo o ingresa tu propio problema.",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(3, 0))

        barra_superior = ttk.Frame(contenedor, style="Card.TFrame", padding=14)
        barra_superior.pack(fill="x", pady=(0, 15))

        ttk.Label(barra_superior, text="Método", style="Card.TLabel").grid(row=0, column=0, sticky="w")

        self.combo_metodo = ttk.Combobox(
            barra_superior,
            textvariable=self.metodo_var,
            state="readonly",
            width=25,
            values=[
                "Newton-Raphson",
                "Secante",
                "Punto fijo",
                "Gauss-Seidel",
                "Jacobi"
            ]
        )
        self.combo_metodo.grid(row=1, column=0, padx=(0, 18), sticky="ew")
        self.combo_metodo.bind("<<ComboboxSelected>>", self.actualizar_ejemplos)

        ttk.Label(barra_superior, text="Ejemplo", style="Card.TLabel").grid(row=0, column=1, sticky="w")

        self.combo_ejemplo = ttk.Combobox(
            barra_superior,
            textvariable=self.ejemplo_var,
            state="readonly",
            width=40
        )
        self.combo_ejemplo.grid(row=1, column=1, padx=(0, 18), sticky="ew")
        self.combo_ejemplo.bind("<<ComboboxSelected>>", self.cargar_ejemplo)

        ttk.Button(
            barra_superior,
            text="Resolver",
            style="Primary.TButton",
            command=self.resolver
        ).grid(row=1, column=2, padx=(0, 8))

        ttk.Button(
            barra_superior,
            text="Limpiar",
            command=self.limpiar
        ).grid(row=1, column=3)

        barra_superior.columnconfigure(1, weight=1)

        cuerpo = ttk.Frame(contenedor)
        cuerpo.pack(fill="both", expand=True)

        self.panel_izquierdo = ttk.Frame(cuerpo, style="Card.TFrame", padding=16)
        self.panel_izquierdo.pack(side="left", fill="y", padx=(0, 15))

        self.panel_derecho = ttk.Frame(cuerpo, style="Card.TFrame", padding=12)
        self.panel_derecho.pack(side="right", fill="both", expand=True)

        ttk.Label(
            self.panel_izquierdo,
            text="Datos del problema",
            style="Header.TLabel"
        ).pack(anchor="w", pady=(0, 12))

        self.frame_inputs = ttk.Frame(self.panel_izquierdo, style="Card.TFrame")
        self.frame_inputs.pack(fill="x")

        self.entrada_funcion = self.crear_input(self.frame_inputs, "Función f(x) o g(x)")
        self.entrada_derivada = self.crear_input(self.frame_inputs, "Derivada f'(x)")
        self.entrada_x0 = self.crear_input(self.frame_inputs, "Valor inicial x0")
        self.entrada_x1 = self.crear_input(self.frame_inputs, "Valor inicial x1")
        self.entrada_error = self.crear_input(self.frame_inputs, "Error permitido (%)")
        self.entrada_iteraciones = self.crear_input(self.frame_inputs, "Máximo de iteraciones")

        self.frame_matriz = ttk.Frame(self.panel_izquierdo, style="Card.TFrame")
        self.frame_matriz.pack(fill="x")

        self.crear_seccion_matriz()

        ttk.Label(
            self.panel_derecho,
            text="Gráfica",
            style="Header.TLabel"
        ).pack(anchor="w", pady=(0, 8))

        self.figura, self.ax = plt.subplots(figsize=(7, 4.2))
        self.figura.patch.set_facecolor("white")

        self.canvas = FigureCanvasTkAgg(self.figura, master=self.panel_derecho)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.panel_derecho)
        self.toolbar.update()

        ttk.Label(
            self.panel_derecho,
            text="Procedimiento paso a paso",
            style="Header.TLabel"
        ).pack(anchor="w", pady=(12, 8))

        self.salida = tk.Text(
            self.panel_derecho,
            height=13,
            font=self.fuente_codigo,
            bg="#111827",
            fg="#E5E7EB",
            insertbackground="white",
            relief="flat",
            borderwidth=12
        )
        self.salida.pack(fill="both", expand=True)

        self.ocultar_todos_los_campos()
        self.graficar_inicio()

    def crear_input(self, parent, label):
        frame = ttk.Frame(parent, style="Card.TFrame")
        frame.pack(fill="x", pady=(4, 7))

        ttk.Label(
            frame,
            text=label,
            style="Card.TLabel"
        ).pack(anchor="w", pady=(0, 3))

        entrada = ttk.Entry(frame, width=38)
        entrada.pack(fill="x")

        entrada.frame_padre = frame
        return entrada

    def crear_seccion_matriz(self):
        self.frame_dimension = ttk.Frame(self.frame_matriz, style="Card.TFrame")
        self.frame_dimension.pack(fill="x", pady=(5, 10))

        ttk.Label(
            self.frame_dimension,
            text="Dimensión del sistema (nxn):",
            style="Card.TLabel"
        ).pack(anchor="w", pady=(0, 5))

        fila = ttk.Frame(self.frame_dimension, style="Card.TFrame")
        fila.pack(fill="x")

        self.combo_dimension = ttk.Combobox(
            fila,
            textvariable=self.dimension_var,
            state="readonly",
            width=8,
            values=[2, 3, 4, 5]
        )
        self.combo_dimension.pack(side="left", padx=(0, 8))

        ttk.Button(
            fila,
            text="Crear matriz",
            style="Primary.TButton",
            command=self.crear_matriz_vacia
        ).pack(side="left")

        ttk.Label(
            self.frame_matriz,
            text="Matriz aumentada [A|b]",
            style="Card.TLabel"
        ).pack(anchor="w", pady=(5, 5))

        self.frame_grid_matriz = ttk.Frame(self.frame_matriz, style="Card.TFrame")
        self.frame_grid_matriz.pack(fill="x")

        self.entrada_inicial_sistema = self.crear_input(
            self.frame_matriz,
            "Valores iniciales x0, separados por coma"
        )

        ayuda = ttk.Label(
            self.frame_matriz,
            text="Ejemplo para 3x3:\n6   1   1   9\n1   6   2   15\n1   1  -6  -3",
            style="Card.TLabel",
            foreground=self.color_secundario
        )
        ayuda.pack(anchor="w", pady=(8, 0))

        self.crear_matriz_vacia()

    def crear_matriz_vacia(self):
        for widget in self.frame_grid_matriz.winfo_children():
            widget.destroy()

        self.entradas_matriz = []

        n = int(self.dimension_var.get())

        for i in range(n):
            fila = []

            for j in range(n + 1):
                entrada = tk.Entry(
                    self.frame_grid_matriz,
                    width=8,
                    font=self.fuente_matriz,
                    justify="center",
                    bg="#F9FAFB",
                    fg=self.color_texto,
                    relief="solid",
                    bd=1
                )

                entrada.grid(row=i, column=j, padx=6, pady=7, ipady=7)

                if j == n:
                    entrada.configure(bg="#EEF2FF")

                fila.append(entrada)

            self.entradas_matriz.append(fila)

    # =====================================================
    # VISIBILIDAD DE CAMPOS
    # =====================================================

    def ocultar_todos_los_campos(self):
        campos = [
            self.entrada_funcion,
            self.entrada_derivada,
            self.entrada_x0,
            self.entrada_x1,
            self.entrada_error,
            self.entrada_iteraciones
        ]

        for campo in campos:
            campo.frame_padre.pack_forget()

        self.frame_matriz.pack_forget()

    def mostrar_campo(self, campo):
        campo.frame_padre.pack(fill="x", pady=(4, 7))

    def actualizar_campos_visibles(self):
        metodo = self.metodo_var.get()

        self.ocultar_todos_los_campos()

        if metodo == "Newton-Raphson":
            self.mostrar_campo(self.entrada_funcion)
            self.mostrar_campo(self.entrada_derivada)
            self.mostrar_campo(self.entrada_x0)
            self.mostrar_campo(self.entrada_error)
            self.mostrar_campo(self.entrada_iteraciones)

        elif metodo == "Secante":
            self.mostrar_campo(self.entrada_funcion)
            self.mostrar_campo(self.entrada_x0)
            self.mostrar_campo(self.entrada_x1)
            self.mostrar_campo(self.entrada_error)
            self.mostrar_campo(self.entrada_iteraciones)

        elif metodo == "Punto fijo":
            self.mostrar_campo(self.entrada_funcion)
            self.mostrar_campo(self.entrada_x0)
            self.mostrar_campo(self.entrada_error)
            self.mostrar_campo(self.entrada_iteraciones)

        elif metodo == "Jacobi" or metodo == "Gauss-Seidel":
            self.frame_matriz.pack(fill="x")
            self.mostrar_campo(self.entrada_error)
            self.mostrar_campo(self.entrada_iteraciones)

    # =====================================================
    # EJEMPLOS
    # =====================================================

    def actualizar_ejemplos(self, event=None):
        metodo = self.metodo_var.get()

        opciones = []

        if metodo == "Newton-Raphson":
            opciones = [e["nombre"] for e in ejemplos_newton]

        elif metodo == "Secante":
            opciones = [e["nombre"] for e in ejemplos_secante]

        elif metodo == "Punto fijo":
            opciones = [e["nombre"] for e in ejemplos_punto_fijo]

        elif metodo == "Jacobi" or metodo == "Gauss-Seidel":
            opciones = [e["nombre"] for e in ejemplos_sistemas]

        opciones.append("Problema propio")

        self.combo_ejemplo["values"] = opciones
        self.ejemplo_var.set("")
        self.limpiar_campos()
        self.actualizar_campos_visibles()

    def cargar_ejemplo(self, event=None):
        metodo = self.metodo_var.get()
        ejemplo_nombre = self.ejemplo_var.get()

        self.limpiar_campos()
        self.actualizar_campos_visibles()

        if ejemplo_nombre == "Problema propio":
            self.insertar(self.entrada_error, "1")
            self.insertar(self.entrada_iteraciones, "20")
            return

        if metodo == "Newton-Raphson":
            ejemplo = self.buscar_ejemplo(ejemplos_newton, ejemplo_nombre)
            self.insertar(self.entrada_funcion, ejemplo["f"])
            self.insertar(self.entrada_derivada, ejemplo["df"])
            self.insertar(self.entrada_x0, ejemplo["x0"])
            self.insertar(self.entrada_error, ejemplo["error"])
            self.insertar(self.entrada_iteraciones, ejemplo["iteraciones"])
            self.graficar_funcion(ejemplo["f"])

        elif metodo == "Secante":
            ejemplo = self.buscar_ejemplo(ejemplos_secante, ejemplo_nombre)
            self.insertar(self.entrada_funcion, ejemplo["f"])
            self.insertar(self.entrada_x0, ejemplo["x0"])
            self.insertar(self.entrada_x1, ejemplo["x1"])
            self.insertar(self.entrada_error, ejemplo["error"])
            self.insertar(self.entrada_iteraciones, ejemplo["iteraciones"])
            self.graficar_funcion(ejemplo["f"])

        elif metodo == "Punto fijo":
            ejemplo = self.buscar_ejemplo(ejemplos_punto_fijo, ejemplo_nombre)
            self.insertar(self.entrada_funcion, ejemplo["g"])
            self.insertar(self.entrada_x0, ejemplo["x0"])
            self.insertar(self.entrada_error, ejemplo["error"])
            self.insertar(self.entrada_iteraciones, ejemplo["iteraciones"])
            self.graficar_funcion(ejemplo["g"], "Gráfica de g(x)")

        elif metodo == "Jacobi" or metodo == "Gauss-Seidel":
            ejemplo = self.buscar_ejemplo(ejemplos_sistemas, ejemplo_nombre)
            self.dimension_var.set(ejemplo["dimension"])
            self.crear_matriz_vacia()
            self.cargar_matriz(ejemplo["matriz"])
            self.insertar(self.entrada_inicial_sistema, ejemplo["inicial"])
            self.insertar(self.entrada_error, ejemplo["error"])
            self.insertar(self.entrada_iteraciones, ejemplo["iteraciones"])
            self.graficar_matriz()

    def buscar_ejemplo(self, lista, nombre):
        for ejemplo in lista:
            if ejemplo["nombre"] == nombre:
                return ejemplo

        return None

    def insertar(self, entrada, valor):
        entrada.delete(0, tk.END)
        entrada.insert(0, str(valor))

    def cargar_matriz(self, matriz):
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                self.entradas_matriz[i][j].delete(0, tk.END)
                self.entradas_matriz[i][j].insert(0, str(matriz[i][j]))

    # =====================================================
    # PASO DE DOMINANCIA DIAGONAL
    # =====================================================

    def revisar_y_reordenar_sistema(self, A, b):
        self.escribir("PASO PREVIO: REVISIÓN DE DOMINANCIA DIAGONAL\n")
        self.escribir("Para Jacobi y Gauss-Seidel es recomendable que la matriz sea diagonalmente dominante.\n")
        self.escribir("Esto ayuda a que el método converja y evita que el error crezca demasiado.\n\n")

        n = len(A)

        self.escribir("Revisión fila por fila:\n")

        for i in range(n):
            diagonal = abs(A[i][i])
            suma_otros = 0

            for j in range(n):
                if j != i:
                    suma_otros += abs(A[i][j])

            self.escribir(
                f"Fila {i + 1}: |a{i + 1}{i + 1}| = {diagonal:.8f}, "
                f"suma de los otros coeficientes = {suma_otros:.8f}\n"
            )

            if diagonal >= suma_otros:
                self.escribir("Cumple: la diagonal es mayor o igual que la suma de los demás.\n\n")
            else:
                self.escribir("No cumple: la diagonal es menor que la suma de los demás.\n\n")

        if matriz_es_diagonalmente_dominante(A):
            self.escribir("Resultado: la matriz ya es diagonalmente dominante.\n")
            self.escribir("Se puede continuar con el método seleccionado.\n\n")
            return A, b

        self.escribir("Resultado: la matriz no es diagonalmente dominante en este orden.\n")
        self.escribir("Se intentará reordenar automáticamente las ecuaciones.\n\n")

        nueva_A, nueva_b, permutacion = intentar_reordenar_dominancia(A, b)

        if permutacion is not None:
            self.escribir("Sí fue posible reordenar las ecuaciones.\n")
            self.escribir("Nuevo orden de filas:\n")

            for nueva_posicion in range(len(permutacion)):
                fila_original = permutacion[nueva_posicion] + 1
                self.escribir(f"Fila nueva {nueva_posicion + 1} = fila original {fila_original}\n")

            self.escribir("\nMatriz reordenada:\n")

            for i in range(n):
                fila_texto = ""

                for j in range(n):
                    fila_texto += f"{nueva_A[i][j]:10.4f}"

                fila_texto += f" | {nueva_b[i]:10.4f}"
                self.escribir(fila_texto + "\n")

            self.escribir("\nSe continuará usando la matriz reordenada.\n\n")

            self.actualizar_matriz_en_pantalla(nueva_A, nueva_b)
            self.graficar_matriz()

            return nueva_A, nueva_b

        self.escribir("No fue posible encontrar un orden diagonalmente dominante.\n")
        self.escribir("Advertencia: el método puede divergir, es decir, el error puede aumentar.\n")
        self.escribir("Se continuará con el orden original, pero el resultado puede no converger.\n\n")

        return A, b

    # =====================================================
    # RESOLVER
    # =====================================================

    def resolver(self):
        metodo = self.metodo_var.get()

        if metodo == "":
            messagebox.showerror("Error", "Selecciona un método.")
            return

        self.salida.delete("1.0", tk.END)

        try:
            if metodo == "Newton-Raphson":
                self.resolver_newton()

            elif metodo == "Secante":
                self.resolver_secante()

            elif metodo == "Punto fijo":
                self.resolver_punto_fijo()

            elif metodo == "Jacobi":
                self.resolver_jacobi()

            elif metodo == "Gauss-Seidel":
                self.resolver_gauss_seidel()

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def resolver_newton(self):
        funcion = self.entrada_funcion.get()
        derivada = self.entrada_derivada.get()
        x = float(self.entrada_x0.get())
        error_max = float(self.entrada_error.get())
        iteraciones = int(self.entrada_iteraciones.get())

        puntos = []

        self.escribir("MÉTODO DE NEWTON-RAPHSON\n")
        self.escribir("Fórmula: x_nuevo = x - f(x) / f'(x)\n\n")

        for i in range(1, iteraciones + 1):
            fx = evaluar_funcion(funcion, x)
            dfx = evaluar_funcion(derivada, x)

            if dfx == 0:
                self.escribir("Error: la derivada es cero.\n")
                return

            x_nuevo = x - fx / dfx
            error = error_porcentual(x_nuevo, x)
            puntos.append(x_nuevo)

            self.escribir(f"Iteración {i}\n")
            self.escribir(f"x = {x:.8f}\n")
            self.escribir(f"f(x) = {fx:.8f}\n")
            self.escribir(f"f'(x) = {dfx:.8f}\n")
            self.escribir(f"x_nuevo = {x_nuevo:.8f}\n")
            self.escribir(f"Error % = {error:.8f}\n\n")

            if error < error_max:
                self.escribir(f"Resultado final: {x_nuevo:.8f}\n")
                self.escribir(f"Error final: {error:.8f}%\n")
                self.graficar_funcion(funcion, "Gráfica de f(x)", puntos)
                return

            x = x_nuevo

        self.escribir("Se alcanzó el máximo de iteraciones.\n")
        self.graficar_funcion(funcion, "Gráfica de f(x)", puntos)

    def resolver_secante(self):
        funcion = self.entrada_funcion.get()
        x0 = float(self.entrada_x0.get())
        x1 = float(self.entrada_x1.get())
        error_max = float(self.entrada_error.get())
        iteraciones = int(self.entrada_iteraciones.get())

        puntos = []

        self.escribir("MÉTODO DE LA SECANTE\n")
        self.escribir("Fórmula: x_nuevo = x1 - f(x1)(x1 - x0) / (f(x1) - f(x0))\n\n")

        for i in range(1, iteraciones + 1):
            f0 = evaluar_funcion(funcion, x0)
            f1 = evaluar_funcion(funcion, x1)

            denominador = f1 - f0

            if denominador == 0:
                self.escribir("Error: división entre cero.\n")
                return

            x_nuevo = x1 - (f1 * (x1 - x0)) / denominador
            error = error_porcentual(x_nuevo, x1)
            puntos.append(x_nuevo)

            self.escribir(f"Iteración {i}\n")
            self.escribir(f"x0 = {x0:.8f}\n")
            self.escribir(f"x1 = {x1:.8f}\n")
            self.escribir(f"f(x0) = {f0:.8f}\n")
            self.escribir(f"f(x1) = {f1:.8f}\n")
            self.escribir(f"x_nuevo = {x_nuevo:.8f}\n")
            self.escribir(f"Error % = {error:.8f}\n\n")

            if error < error_max:
                self.escribir(f"Resultado final: {x_nuevo:.8f}\n")
                self.escribir(f"Error final: {error:.8f}%\n")
                self.graficar_funcion(funcion, "Gráfica de f(x)", puntos)
                return

            x0 = x1
            x1 = x_nuevo

        self.escribir("Se alcanzó el máximo de iteraciones.\n")
        self.graficar_funcion(funcion, "Gráfica de f(x)", puntos)

    def resolver_punto_fijo(self):
        funcion = self.entrada_funcion.get()
        x = float(self.entrada_x0.get())
        error_max = float(self.entrada_error.get())
        iteraciones = int(self.entrada_iteraciones.get())

        puntos = []

        self.escribir("MÉTODO DE PUNTO FIJO\n")
        self.escribir("Fórmula: x_nuevo = g(x)\n\n")

        for i in range(1, iteraciones + 1):
            x_nuevo = evaluar_funcion(funcion, x)
            error = error_porcentual(x_nuevo, x)
            puntos.append(x_nuevo)

            self.escribir(f"Iteración {i}\n")
            self.escribir(f"x = {x:.8f}\n")
            self.escribir(f"g(x) = {x_nuevo:.8f}\n")
            self.escribir(f"Error % = {error:.8f}\n\n")

            if error < error_max:
                self.escribir(f"Resultado final: {x_nuevo:.8f}\n")
                self.escribir(f"Error final: {error:.8f}%\n")
                self.graficar_funcion(funcion, "Gráfica de g(x)", puntos)
                return

            x = x_nuevo

        self.escribir("Se alcanzó el máximo de iteraciones.\n")
        self.graficar_funcion(funcion, "Gráfica de g(x)", puntos)

    def resolver_jacobi(self):
        A, b, x_anterior = self.obtener_sistema()
        A, b = self.revisar_y_reordenar_sistema(A, b)

        error_max = float(self.entrada_error.get())
        iteraciones = int(self.entrada_iteraciones.get())

        n = len(A)
        errores = []

        self.escribir("MÉTODO DE JACOBI\n")
        self.escribir("Cada variable usa únicamente los valores de la iteración anterior.\n\n")

        for iteracion in range(1, iteraciones + 1):
            x_nuevo = []

            self.escribir(f"Iteración {iteracion}\n")

            for i in range(n):
                total = b[i]

                formula = f"x{i + 1} = ({b[i]}"

                for j in range(n):
                    if j != i:
                        total = total - A[i][j] * x_anterior[j]
                        formula += f" - ({A[i][j]})({x_anterior[j]:.6f})"

                valor = total / A[i][i]
                x_nuevo.append(valor)

                formula += f") / {A[i][i]}"
                self.escribir(formula + "\n")
                self.escribir(f"x{i + 1} = {valor:.8f}\n")

            error = error_vectorial_maximo(x_nuevo, x_anterior)
            errores.append(error)

            self.escribir(f"Error máximo % = {error:.8f}\n\n")

            if error < error_max:
                self.escribir("Resultado final:\n")

                for i in range(n):
                    self.escribir(f"x{i + 1} = {x_nuevo[i]:.8f}\n")

                self.graficar_errores(errores)
                return

            x_anterior = x_nuevo

        self.escribir("Se alcanzó el máximo de iteraciones.\n")
        self.graficar_errores(errores)

    def resolver_gauss_seidel(self):
        A, b, x = self.obtener_sistema()
        A, b = self.revisar_y_reordenar_sistema(A, b)

        error_max = float(self.entrada_error.get())
        iteraciones = int(self.entrada_iteraciones.get())

        n = len(A)
        errores = []

        self.escribir("MÉTODO DE GAUSS-SEIDEL\n")
        self.escribir("Cada variable usa los valores más recientes disponibles.\n\n")

        for iteracion in range(1, iteraciones + 1):
            x_anterior = x.copy()

            self.escribir(f"Iteración {iteracion}\n")

            for i in range(n):
                total = b[i]

                formula = f"x{i + 1} = ({b[i]}"

                for j in range(n):
                    if j != i:
                        total = total - A[i][j] * x[j]
                        formula += f" - ({A[i][j]})({x[j]:.6f})"

                x[i] = total / A[i][i]

                formula += f") / {A[i][i]}"
                self.escribir(formula + "\n")
                self.escribir(f"x{i + 1} = {x[i]:.8f}\n")

            error = error_vectorial_maximo(x, x_anterior)
            errores.append(error)

            self.escribir(f"Error máximo % = {error:.8f}\n\n")

            if error < error_max:
                self.escribir("Resultado final:\n")

                for i in range(n):
                    self.escribir(f"x{i + 1} = {x[i]:.8f}\n")

                self.graficar_errores(errores)
                return

        self.escribir("Se alcanzó el máximo de iteraciones.\n")
        self.graficar_errores(errores)

    # =====================================================
    # OBTENER SISTEMA DESDE MATRIZ
    # =====================================================

    def obtener_sistema(self):
        n = int(self.dimension_var.get())

        A = []
        b = []

        for i in range(n):
            fila = []

            for j in range(n):
                fila.append(float(self.entradas_matriz[i][j].get()))

            resultado = float(self.entradas_matriz[i][n].get())

            A.append(fila)
            b.append(resultado)

        x_inicial_texto = self.entrada_inicial_sistema.get()
        x_inicial = []

        for valor in x_inicial_texto.split(","):
            x_inicial.append(float(valor.strip()))

        if len(x_inicial) != n:
            raise ValueError("La cantidad de valores iniciales debe coincidir con la dimensión del sistema.")

        return A, b, x_inicial

    def actualizar_matriz_en_pantalla(self, A, b):
        n = len(A)

        self.dimension_var.set(n)
        self.crear_matriz_vacia()

        for i in range(n):
            for j in range(n):
                self.entradas_matriz[i][j].delete(0, tk.END)
                self.entradas_matriz[i][j].insert(0, str(A[i][j]))

            self.entradas_matriz[i][n].delete(0, tk.END)
            self.entradas_matriz[i][n].insert(0, str(b[i]))

    # =====================================================
    # GRÁFICAS
    # =====================================================

    def graficar_funcion(self, funcion, titulo="Gráfica de f(x)", puntos=None):
        if puntos is None:
            puntos = []

        self.ax.clear()

        valores_x = np.linspace(-5, 5, 500)
        valores_y = []

        for valor in valores_x:
            try:
                y = evaluar_funcion(funcion, valor)

                if isinstance(y, complex):
                    valores_y.append(np.nan)
                else:
                    valores_y.append(y)

            except:
                valores_y.append(np.nan)

        self.ax.plot(valores_x, valores_y, linewidth=2, label=funcion)
        self.ax.axhline(0, linewidth=1)
        self.ax.axvline(0, linewidth=1)

        for punto in puntos:
            try:
                y = evaluar_funcion(funcion, punto)

                if not isinstance(y, complex):
                    self.ax.scatter(punto, y, s=55)
                    self.ax.text(punto, y, f"{punto:.4f}", fontsize=10)

            except:
                pass

        self.ax.set_title(titulo, fontsize=16, fontweight="bold")
        self.ax.set_xlabel("x", fontsize=13)
        self.ax.set_ylabel("y", fontsize=13)
        self.ax.tick_params(axis="both", labelsize=11)
        self.ax.grid(True, alpha=0.3)
        self.ax.legend(fontsize=11)

        self.figura.tight_layout()
        self.canvas.draw()

    def graficar_errores(self, errores):
        self.ax.clear()

        iteraciones = list(range(1, len(errores) + 1))

        self.ax.plot(iteraciones, errores, marker="o", linewidth=2)
        self.ax.set_title("Convergencia del error", fontsize=16, fontweight="bold")
        self.ax.set_xlabel("Iteración", fontsize=13)
        self.ax.set_ylabel("Error porcentual máximo", fontsize=13)
        self.ax.tick_params(axis="both", labelsize=11)
        self.ax.grid(True, alpha=0.3)

        self.figura.tight_layout()
        self.canvas.draw()

    def graficar_matriz(self):
        self.ax.clear()
        self.ax.axis("off")
        self.ax.set_title("Matriz aumentada [A|b]", fontsize=16, fontweight="bold")

        n = int(self.dimension_var.get())
        texto = ""

        for i in range(n):
            fila = []

            for j in range(n + 1):
                valor = self.entradas_matriz[i][j].get()
                fila.append(valor)

            texto += "   ".join(fila) + "\n"

        self.ax.text(
            0.05,
            0.85,
            texto,
            transform=self.ax.transAxes,
            fontsize=13,
            verticalalignment="top",
            family="monospace"
        )

        self.canvas.draw()

    def graficar_inicio(self):
        self.ax.clear()
        self.ax.axis("off")
        self.ax.set_title("Selecciona un método y un ejemplo", fontsize=16, fontweight="bold")
        self.canvas.draw()

    # =====================================================
    # LIMPIEZA
    # =====================================================

    def escribir(self, texto):
        self.salida.insert(tk.END, texto)
        self.salida.see(tk.END)

    def limpiar_campos(self):
        entradas = [
            self.entrada_funcion,
            self.entrada_derivada,
            self.entrada_x0,
            self.entrada_x1,
            self.entrada_error,
            self.entrada_iteraciones,
            self.entrada_inicial_sistema
        ]

        for entrada in entradas:
            entrada.delete(0, tk.END)

        for fila in self.entradas_matriz:
            for entrada in fila:
                entrada.delete(0, tk.END)

        self.salida.delete("1.0", tk.END)

    def limpiar(self):
        self.limpiar_campos()
        self.ejemplo_var.set("")
        self.graficar_inicio()


# =====================================================
# EJECUTAR APLICACIÓN
# =====================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = AppMetodosNumericos(root)
    root.mainloop()