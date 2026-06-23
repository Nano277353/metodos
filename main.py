import math
import itertools

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


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
        suma_otros = sum(abs(A[i][j]) for j in range(n) if j != i)
        if diagonal < suma_otros:
            return False
    return True


def intentar_reordenar_dominancia(A, b):
    n = len(A)
    indices = list(range(n))
    for permutacion in itertools.permutations(indices):
        nueva_A = [A[i] for i in permutacion]
        nueva_b = [b[i] for i in permutacion]
        if matriz_es_diagonalmente_dominante(nueva_A):
            return nueva_A, nueva_b, permutacion
    return A, b, None


# =====================================================
# EJEMPLOS PRECARGADOS
# =====================================================

ejemplos_newton = [
    {"nombre": "Ej. 1 — 1/e^x - x",     "f": "1/exp(x) - x",      "df": "-exp(-x) - 1",       "x0": "0",   "error": "1", "iteraciones": "20"},
    {"nombre": "Ej. 2 — 1/e^x - ln(x)", "f": "1/exp(x) - log(x)", "df": "-exp(-x) - 1/x",     "x0": "1",   "error": "1", "iteraciones": "20"},
    {"nombre": "Ej. 3 — e^(-2x) - 5x",  "f": "exp(-2*x) - 5*x",   "df": "-2*exp(-2*x) - 5",   "x0": "0",   "error": "1", "iteraciones": "20"},
    {"nombre": "Ej. 4 — x^3 - cos(x)",  "f": "x**3 - cos(x)",     "df": "3*x**2 + sin(x)",    "x0": "0.5", "error": "1", "iteraciones": "20"},
]

ejemplos_secante = [
    {"nombre": "Ej. 1 — 1/e^x - x",     "f": "1/exp(x) - x",      "x0": "0", "x1": "1", "error": "1", "iteraciones": "20"},
    {"nombre": "Ej. 2 — 1/e^x - ln(x)", "f": "1/exp(x) - log(x)", "x0": "1", "x1": "2", "error": "1", "iteraciones": "20"},
    {"nombre": "Ej. 3 — e^(-2x) - 5x",  "f": "exp(-2*x) - 5*x",   "x0": "0", "x1": "1", "error": "1", "iteraciones": "20"},
    {"nombre": "Ej. 4 — x^3 - cos(x)",  "f": "x**3 - cos(x)",     "x0": "0.5","x1": "1","error": "1", "iteraciones": "20"},
]

ejemplos_punto_fijo = [
    {"nombre": "Ej. 1 — g(x) = 1/e^x",       "g": "1/exp(x)",        "x0": "0",   "error": "1", "iteraciones": "20"},
    {"nombre": "Ej. 2 — g(x) = e^(1/e^x)",   "g": "exp(1/exp(x))",   "x0": "1",   "error": "1", "iteraciones": "20"},
    {"nombre": "Ej. 3 — g(x) = e^(-2x)/5",   "g": "exp(-2*x)/5",     "x0": "0",   "error": "1", "iteraciones": "20"},
    {"nombre": "Ej. 4 — g(x) = cos(x)^(1/3)","g": "cos(x)**(1/3)",   "x0": "0.5", "error": "1", "iteraciones": "20"},
]

ejemplos_sistemas = [
    {
        "nombre": "Ej. 1 — Sistema 3x3",
        "dimension": 3,
        "matriz": [[6, 1, 1, 9], [1, 6, 2, 15], [1, 1, -6, -3]],
        "inicial": "0,0,0", "error": "1", "iteraciones": "20"
    },
    {
        "nombre": "Ej. 2 — Sistema 3x3",
        "dimension": 3,
        "matriz": [[2, -6, -1, -38], [-3, -1, 7, -34], [-8, -1, 7, -20]],
        "inicial": "0,0,0", "error": "1", "iteraciones": "20"
    },
    {
        "nombre": "Ej. 3 — Sistema 3x3",
        "dimension": 3,
        "matriz": [[0.71, 0.1, -8.2, -56.4], [25, -0.9, -0.3, 20.2], [3.7, -7.3, -0.1, -18.9]],
        "inicial": "0,0,0", "error": "1", "iteraciones": "20"
    },
]


# =====================================================
# GRÁFICAS
# =====================================================

def graficar_funcion(funcion, titulo="Gráfica de f(x)", puntos=None):
    if puntos is None:
        puntos = []

    fig, ax = plt.subplots(figsize=(8, 4))
    valores_x = np.linspace(-5, 5, 500)
    valores_y = []

    for valor in valores_x:
        try:
            y = evaluar_funcion(funcion, valor)
            valores_y.append(np.nan if isinstance(y, complex) else y)
        except:
            valores_y.append(np.nan)

    ax.plot(valores_x, valores_y, linewidth=2, label=funcion)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)

    for punto in puntos:
        try:
            y = evaluar_funcion(funcion, punto)
            if not isinstance(y, complex):
                ax.scatter(punto, y, s=55, zorder=5)
                ax.text(punto, y, f"{punto:.4f}", fontsize=9)
        except:
            pass

    ax.set_title(titulo, fontsize=14, fontweight="bold")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    return fig


def graficar_errores(errores):
    fig, ax = plt.subplots(figsize=(8, 4))
    iteraciones = list(range(1, len(errores) + 1))
    ax.plot(iteraciones, errores, marker="o", linewidth=2)
    ax.set_title("Convergencia del error", fontsize=14, fontweight="bold")
    ax.set_xlabel("Iteración")
    ax.set_ylabel("Error porcentual máximo")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


# =====================================================
# MÉTODOS NUMÉRICOS (devuelven texto + figura)
# =====================================================

def resolver_newton(funcion, derivada, x0, error_max, iteraciones):
    x = x0
    puntos = []
    lineas = ["**MÉTODO DE NEWTON-RAPHSON**\n"]
    lineas.append("Fórmula: x_nuevo = x - f(x) / f'(x)\n")

    for i in range(1, iteraciones + 1):
        fx  = evaluar_funcion(funcion, x)
        dfx = evaluar_funcion(derivada, x)

        if dfx == 0:
            lineas.append("Error: la derivada es cero.")
            return "\n".join(lineas), None

        x_nuevo = x - fx / dfx
        error   = error_porcentual(x_nuevo, x)
        puntos.append(x_nuevo)

        lineas.append(f"Iteración {i}")
        lineas.append(f"  x        = {x:.8f}")
        lineas.append(f"  f(x)     = {fx:.8f}")
        lineas.append(f"  f'(x)    = {dfx:.8f}")
        lineas.append(f"  x_nuevo  = {x_nuevo:.8f}")
        lineas.append(f"  Error %  = {error:.8f}\n")

        if error < error_max:
            lineas.append(f"✅ Resultado final: {x_nuevo:.8f}")
            lineas.append(f"   Error final: {error:.8f}%")
            return "\n".join(lineas), graficar_funcion(funcion, "Gráfica de f(x)", puntos)

        x = x_nuevo

    lineas.append("⚠️ Se alcanzó el máximo de iteraciones.")
    return "\n".join(lineas), graficar_funcion(funcion, "Gráfica de f(x)", puntos)


def resolver_secante(funcion, x0, x1, error_max, iteraciones):
    puntos = []
    lineas = ["**MÉTODO DE LA SECANTE**\n"]
    lineas.append("Fórmula: x_nuevo = x1 - f(x1)(x1 - x0) / (f(x1) - f(x0))\n")

    for i in range(1, iteraciones + 1):
        f0 = evaluar_funcion(funcion, x0)
        f1 = evaluar_funcion(funcion, x1)
        denominador = f1 - f0

        if denominador == 0:
            lineas.append("Error: división entre cero.")
            return "\n".join(lineas), None

        x_nuevo = x1 - (f1 * (x1 - x0)) / denominador
        error   = error_porcentual(x_nuevo, x1)
        puntos.append(x_nuevo)

        lineas.append(f"Iteración {i}")
        lineas.append(f"  x0       = {x0:.8f}")
        lineas.append(f"  x1       = {x1:.8f}")
        lineas.append(f"  f(x0)    = {f0:.8f}")
        lineas.append(f"  f(x1)    = {f1:.8f}")
        lineas.append(f"  x_nuevo  = {x_nuevo:.8f}")
        lineas.append(f"  Error %  = {error:.8f}\n")

        if error < error_max:
            lineas.append(f"✅ Resultado final: {x_nuevo:.8f}")
            lineas.append(f"   Error final: {error:.8f}%")
            return "\n".join(lineas), graficar_funcion(funcion, "Gráfica de f(x)", puntos)

        x0, x1 = x1, x_nuevo

    lineas.append("⚠️ Se alcanzó el máximo de iteraciones.")
    return "\n".join(lineas), graficar_funcion(funcion, "Gráfica de f(x)", puntos)


def resolver_punto_fijo(funcion, x0, error_max, iteraciones):
    x = x0
    puntos = []
    lineas = ["**MÉTODO DE PUNTO FIJO**\n", "Fórmula: x_nuevo = g(x)\n"]

    for i in range(1, iteraciones + 1):
        x_nuevo = evaluar_funcion(funcion, x)
        error   = error_porcentual(x_nuevo, x)
        puntos.append(x_nuevo)

        lineas.append(f"Iteración {i}")
        lineas.append(f"  x        = {x:.8f}")
        lineas.append(f"  g(x)     = {x_nuevo:.8f}")
        lineas.append(f"  Error %  = {error:.8f}\n")

        if error < error_max:
            lineas.append(f"✅ Resultado final: {x_nuevo:.8f}")
            lineas.append(f"   Error final: {error:.8f}%")
            return "\n".join(lineas), graficar_funcion(funcion, "Gráfica de g(x)", puntos)

        x = x_nuevo

    lineas.append("⚠️ Se alcanzó el máximo de iteraciones.")
    return "\n".join(lineas), graficar_funcion(funcion, "Gráfica de g(x)", puntos)


def revisar_dominancia(A, b):
    lineas = []
    lineas.append("**PASO PREVIO: REVISIÓN DE DOMINANCIA DIAGONAL**\n")
    n = len(A)

    for i in range(n):
        diagonal   = abs(A[i][i])
        suma_otros = sum(abs(A[i][j]) for j in range(n) if j != i)
        cumple     = "✅ Cumple" if diagonal >= suma_otros else "❌ No cumple"
        lineas.append(
            f"Fila {i+1}: |a{i+1}{i+1}| = {diagonal:.4f}, "
            f"suma otros = {suma_otros:.4f} → {cumple}"
        )

    lineas.append("")
    if matriz_es_diagonalmente_dominante(A):
        lineas.append("✅ La matriz ya es diagonalmente dominante.\n")
        return A, b, "\n".join(lineas)

    lineas.append("La matriz no es diagonalmente dominante. Intentando reordenar...")
    nueva_A, nueva_b, permutacion = intentar_reordenar_dominancia(A, b)

    if permutacion is not None:
        lineas.append("✅ Reordenamiento exitoso:")
        for nueva_pos, orig in enumerate(permutacion):
            lineas.append(f"  Fila nueva {nueva_pos+1} = fila original {orig+1}")
        lineas.append("")
        return nueva_A, nueva_b, "\n".join(lineas)

    lineas.append("⚠️ No fue posible reordenar. El método puede divergir.\n")
    return A, b, "\n".join(lineas)


def resolver_jacobi(A, b, x_inicial, error_max, iteraciones):
    A, b, texto_dom = revisar_dominancia(A, b)
    x_anterior = list(x_inicial)
    n = len(A)
    errores = []
    lineas = [texto_dom, "**MÉTODO DE JACOBI**\n"]

    for iteracion in range(1, iteraciones + 1):
        x_nuevo = []
        lineas.append(f"Iteración {iteracion}")

        for i in range(n):
            total = b[i]
            formula = f"  x{i+1} = ({b[i]}"
            for j in range(n):
                if j != i:
                    total  -= A[i][j] * x_anterior[j]
                    formula += f" - ({A[i][j]})({x_anterior[j]:.4f})"
            valor = total / A[i][i]
            x_nuevo.append(valor)
            formula += f") / {A[i][i]}"
            lineas.append(formula)
            lineas.append(f"  x{i+1} = {valor:.8f}")

        error = error_vectorial_maximo(x_nuevo, x_anterior)
        errores.append(error)
        lineas.append(f"  Error máximo % = {error:.8f}\n")

        if error < error_max:
            lineas.append("✅ Resultado final:")
            for i in range(n):
                lineas.append(f"  x{i+1} = {x_nuevo[i]:.8f}")
            return "\n".join(lineas), graficar_errores(errores), A, b

        x_anterior = x_nuevo

    lineas.append("⚠️ Se alcanzó el máximo de iteraciones.")
    return "\n".join(lineas), graficar_errores(errores), A, b


def resolver_gauss_seidel(A, b, x_inicial, error_max, iteraciones):
    A, b, texto_dom = revisar_dominancia(A, b)
    x = list(x_inicial)
    n = len(A)
    errores = []
    lineas = [texto_dom, "**MÉTODO DE GAUSS-SEIDEL**\n"]

    for iteracion in range(1, iteraciones + 1):
        x_anterior = x.copy()
        lineas.append(f"Iteración {iteracion}")

        for i in range(n):
            total = b[i]
            formula = f"  x{i+1} = ({b[i]}"
            for j in range(n):
                if j != i:
                    total  -= A[i][j] * x[j]
                    formula += f" - ({A[i][j]})({x[j]:.4f})"
            x[i] = total / A[i][i]
            formula += f") / {A[i][i]}"
            lineas.append(formula)
            lineas.append(f"  x{i+1} = {x[i]:.8f}")

        error = error_vectorial_maximo(x, x_anterior)
        errores.append(error)
        lineas.append(f"  Error máximo % = {error:.8f}\n")

        if error < error_max:
            lineas.append("✅ Resultado final:")
            for i in range(n):
                lineas.append(f"  x{i+1} = {x[i]:.8f}")
            return "\n".join(lineas), graficar_errores(errores), A, b

        # x already updated in-place for Gauss-Seidel

    lineas.append("⚠️ Se alcanzó el máximo de iteraciones.")
    return "\n".join(lineas), graficar_errores(errores), A, b


# =====================================================
# STREAMLIT UI
# =====================================================

st.set_page_config(page_title="Métodos Numéricos", layout="wide")
st.title("Solucionador de Métodos Numéricos")
st.caption("Selecciona un método, carga un ejemplo o ingresa tu propio problema.")

# --- Selección de método y ejemplo ---
col_metodo, col_ejemplo = st.columns([1, 2])

with col_metodo:
    metodo = st.selectbox(
        "Método",
        ["Newton-Raphson", "Secante", "Punto fijo", "Jacobi", "Gauss-Seidel"]
    )

# Ejemplos disponibles según método
if metodo == "Newton-Raphson":
    lista_ejemplos = ejemplos_newton
elif metodo == "Secante":
    lista_ejemplos = ejemplos_secante
elif metodo == "Punto fijo":
    lista_ejemplos = ejemplos_punto_fijo
else:
    lista_ejemplos = ejemplos_sistemas

nombres_ejemplos = [e["nombre"] for e in lista_ejemplos] + ["Problema propio"]

with col_ejemplo:
    ejemplo_nombre = st.selectbox("Ejemplo", nombres_ejemplos)

ejemplo = next((e for e in lista_ejemplos if e["nombre"] == ejemplo_nombre), None)

st.divider()

# =====================================================
# INPUTS SEGÚN MÉTODO
# =====================================================

if metodo in ("Newton-Raphson", "Secante", "Punto fijo"):
    col_izq, col_der = st.columns([1, 2])

    with col_izq:
        st.subheader("Datos del problema")

        label_f = "Función g(x)" if metodo == "Punto fijo" else "Función f(x)"
        funcion_default = (ejemplo.get("f") or ejemplo.get("g", "")) if ejemplo else ""
        funcion = st.text_input(label_f, value=funcion_default)

        if metodo == "Newton-Raphson":
            derivada_default = ejemplo["df"] if ejemplo else ""
            derivada = st.text_input("Derivada f'(x)", value=derivada_default)

        x0_default = ejemplo["x0"] if ejemplo else "0"
        x0 = st.text_input("Valor inicial x0", value=x0_default)

        if metodo == "Secante":
            x1_default = ejemplo["x1"] if ejemplo else "1"
            x1 = st.text_input("Valor inicial x1", value=x1_default)

        error_default = ejemplo["error"] if ejemplo else "1"
        error_max = st.text_input("Error permitido (%)", value=error_default)

        iter_default = ejemplo["iteraciones"] if ejemplo else "20"
        iteraciones = st.text_input("Máximo de iteraciones", value=iter_default)

        resolver = st.button("▶ Resolver", type="primary", use_container_width=True)

    with col_der:
        if ejemplo and metodo != "Punto fijo":
            st.pyplot(graficar_funcion(funcion or ejemplo.get("f",""), "Vista previa de f(x)"))
        elif ejemplo and metodo == "Punto fijo":
            st.pyplot(graficar_funcion(funcion or ejemplo.get("g",""), "Vista previa de g(x)"))

        if resolver:
            try:
                em = float(error_max)
                it = int(iteraciones)
                x0v = float(x0)

                if metodo == "Newton-Raphson":
                    texto, fig = resolver_newton(funcion, derivada, x0v, em, it)
                elif metodo == "Secante":
                    x1v = float(x1)
                    texto, fig = resolver_secante(funcion, x0v, x1v, em, it)
                else:
                    texto, fig = resolver_punto_fijo(funcion, x0v, em, it)

                if fig:
                    st.pyplot(fig)
                st.text_area("Procedimiento paso a paso", value=texto, height=350)

            except Exception as e:
                st.error(f"Error: {e}")

# =====================================================
# SISTEMAS (Jacobi / Gauss-Seidel)
# =====================================================

else:
    col_izq, col_der = st.columns([1, 2])

    with col_izq:
        st.subheader("Sistema de ecuaciones")

        dim_default = ejemplo["dimension"] if ejemplo else 3
        dimension = st.selectbox("Dimensión del sistema (n×n)", [2, 3, 4, 5], index=[2,3,4,5].index(dim_default))

        st.markdown("**Matriz aumentada [A|b]**")
        st.caption("Ingresa los coeficientes fila por fila. La última columna es el vector b.")

        # Construir valores default de la matriz
        mat_default = ejemplo["matriz"] if ejemplo else [[0.0] * (dimension + 1)] * dimension

        # Asegurarse que mat_default tiene el tamaño correcto
        filas = []
        for i in range(dimension):
            cols_ui = st.columns(dimension + 1)
            fila = []
            for j in range(dimension + 1):
                etiqueta = f"b{i+1}" if j == dimension else f"a{i+1}{j+1}"
                try:
                    default_val = float(mat_default[i][j]) if i < len(mat_default) and j < len(mat_default[i]) else 0.0
                except:
                    default_val = 0.0
                val = cols_ui[j].number_input(etiqueta, value=default_val, key=f"m_{i}_{j}", label_visibility="visible", step=0.01)
                fila.append(val)
            filas.append(fila)

        inicial_default = ejemplo["inicial"] if ejemplo else ",".join(["0"] * dimension)
        inicial_str = st.text_input("Valores iniciales x₀ (separados por coma)", value=inicial_default)

        error_default = ejemplo["error"] if ejemplo else "1"
        error_max = st.text_input("Error permitido (%)", value=error_default)

        iter_default = ejemplo["iteraciones"] if ejemplo else "20"
        iteraciones = st.text_input("Máximo de iteraciones", value=iter_default)

        resolver = st.button("▶ Resolver", type="primary", use_container_width=True)

    with col_der:
        if resolver:
            try:
                A = [fila[:dimension] for fila in filas]
                b = [fila[dimension] for fila in filas]
                x_inicial = [float(v.strip()) for v in inicial_str.split(",")]
                em = float(error_max)
                it = int(iteraciones)

                if len(x_inicial) != dimension:
                    st.error(f"Se necesitan exactamente {dimension} valores iniciales.")
                else:
                    if metodo == "Jacobi":
                        texto, fig, A_final, b_final = resolver_jacobi(A, b, x_inicial, em, it)
                    else:
                        texto, fig, A_final, b_final = resolver_gauss_seidel(A, b, x_inicial, em, it)

                    st.pyplot(fig)
                    st.text_area("Procedimiento paso a paso", value=texto, height=400)

            except Exception as e:
                st.error(f"Error: {e}")