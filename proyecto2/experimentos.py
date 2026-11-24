import csv
import os
import random
import sys
import time
import tracemalloc

import fuerza_bruta
import generador
import mrv
import recocido
from sudoku import contar_faltantes, leer_sudoku

# Tecnicas que se comparan, todas reciben el limite de tiempo
TECNICAS = {
    "fuerza_bruta": fuerza_bruta.resolver,
    "mrv": mrv.resolver,
    "recocido": recocido.resolver,
}

# Otros valores que se prueban, cambiando un parametro a la vez
# El diccionario vacio corre la tecnica con sus valores por defecto
# Recocido: t0=None y 120, alfa 0.75 y 0.99, y las iteraciones salen de Lewis (2007) y De Souza y Romero (2013)
# Lewis usa (celdas vacias)^2 iteraciones: unas 2600 en el 9x9 y unas 17000 en los 16x16
# Las ultimas de cada lista combinan los mejores valores de la prueba de uno a la vez
VARIANTES = {
    "fuerza_bruta": [{}],
    "mrv": [{}, {"reinicios": 1000}, {"reinicios": 10000}, {"celda_azar": True}, {"valor_azar": False},
            {"celda_azar": True, "reinicios": 1000}, {"celda_azar": True, "reinicios": 10000}],
    "recocido": [{}, {"t0": None}, {"t0": 0.5}, {"t0": 2.0}, {"t0": 5.0}, {"t0": 120.0},
                 {"alfa": 0.75}, {"alfa": 0.9}, {"alfa": 0.99},
                 {"iteraciones": 10}, {"iteraciones": 260}, {"iteraciones": 2600}, {"iteraciones": 17000},
                 {"reinicio": 10}, {"reinicio": 50}, {"reinicio": 100},
                 {"alfa": 0.99, "reinicio": 100},
                 {"t0": 0.5, "alfa": 0.9}, {"t0": 0.5, "reinicio": 100}, {"alfa": 0.9, "reinicio": 100},
                 {"t0": 0.5, "alfa": 0.9, "reinicio": 100},
                 {"t0": 0.5, "alfa": 0.9, "reinicio": 100, "iteraciones": 2000}],
}

# Sudokus que se generan con la palabra generados: cada tamano con cada proporcion p de pistas,
# y varias semillas para no depender de un solo sudoku
TAMANOS = [4, 9, 16]
PROPORCIONES = [0.2, 0.3, 0.4, 0.5, 0.6]
SEMILLAS = [1, 2, 3]

# Palabras que se pueden agregar al final del comando
OPCIONES = ["parametros", "memoria", "generados"]

# Columnas del CSV, una fila por corrida
COLUMNAS = ["tecnica", "parametros", "sudoku", "tamano", "p", "semilla", "vacias", "limite", "corrida",
            "faltantes", "resuelto", "tiempo", "memoria_kb"]

# Retorna cuantas celdas vacias tiene el tablero
def contar_vacias(tablero):
    return sum(fila.count(0) for fila in tablero)

# Lee los sudokus de input y retorna el nombre, el tablero, la proporcion de pistas y la semilla de cada uno
def sudokus_de_input():
    sudokus = []
    for archivo in sorted(os.listdir("input")):
        tablero = leer_sudoku(os.path.join("input", archivo))
        celdas = len(tablero) * len(tablero)
        p = round((celdas - contar_vacias(tablero)) / celdas, 2)
        sudokus.append((archivo, tablero, p, ""))
    return sudokus

# Genera un sudoku por cada tamano, proporcion y semilla, con los mismos datos que sudokus_de_input
def sudokus_generados():
    sudokus = []
    for tamano in TAMANOS:
        for p in PROPORCIONES:
            for semilla in SEMILLAS:
                tablero = generador.generar(tamano, p, semilla)
                sudokus.append((f"generado_{tamano}x{tamano}_p{p}_s{semilla}", tablero, p, semilla))
    # generar fija la semilla, asi que se vuelve al azar para que las corridas no se repitan
    random.seed()
    return sudokus

# Retorna los parametros como texto, por ejemplo "t0=0.5"
def describir(parametros):
    if len(parametros) == 0:
        return "por defecto"
    return " ".join(f"{nombre}={valor}" for nombre, valor in parametros.items())

# Corre una tecnica sobre una copia del sudoku y retorna los faltantes, el tiempo y la memoria pico
# La memoria solo se mide si se pide, porque tracemalloc hace mas lenta la corrida
def correr(resolver, tablero, segundos, parametros, medir_memoria):
    copia = [fila[:] for fila in tablero]
    if medir_memoria:
        tracemalloc.start()
    inicio = time.perf_counter()
    resultado = resolver(copia, segundos, **parametros)
    tiempo = time.perf_counter() - inicio
    memoria = ""
    if medir_memoria:
        _, pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memoria = round(pico / 1024, 1)
    return contar_faltantes(resultado), tiempo, memoria

# Corre cada tecnica varias veces con cada limite y retorna una fila por corrida
def experimentar(sudoku, corridas, limites, probar_parametros, medir_memoria):
    nombre, tablero, p, semilla = sudoku
    filas = []
    for tecnica, resolver in TECNICAS.items():
        variantes = VARIANTES[tecnica] if probar_parametros else [{}]
        for parametros in variantes:
            for segundos in limites:
                for corrida in range(1, corridas + 1):
                    faltantes, tiempo, memoria = correr(resolver, tablero, segundos, parametros, medir_memoria)
                    print(tecnica, describir(parametros), nombre, "limite", segundos, "corrida", corrida, "faltan", faltantes, f"{tiempo:.3f} s", memoria)
                    filas.append({
                        "tecnica": tecnica,
                        "parametros": describir(parametros),
                        "sudoku": nombre,
                        "tamano": len(tablero),
                        "p": p,
                        "semilla": semilla,
                        "vacias": contar_vacias(tablero),
                        "limite": segundos,
                        "corrida": corrida,
                        "faltantes": faltantes,
                        "resuelto": 1 if faltantes == 0 else 0,
                        "tiempo": round(tiempo, 3),
                        "memoria_kb": memoria,
                    })
    return filas

# Guarda las filas en un archivo CSV
def guardar_csv(filas, ruta):
    with open(ruta, "w", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        escritor.writeheader()
        escritor.writerows(filas)

# Imprime, por tecnica, parametros, sudoku y limite, cuantas corridas resolvio y los promedios
def resumir(filas):
    grupos = {}
    for fila in filas:
        clave = (fila["tecnica"], fila["parametros"], fila["sudoku"], fila["limite"])
        if clave not in grupos:
            grupos[clave] = []
        grupos[clave].append(fila)
    print("tecnica, parametros, sudoku, limite, resueltas, faltantes promedio, tiempo promedio, memoria promedio")
    for (tecnica, parametros, sudoku, limite), grupo in grupos.items():
        resueltas = sum(fila["resuelto"] for fila in grupo)
        faltantes = sum(fila["faltantes"] for fila in grupo) / len(grupo)
        tiempo = sum(fila["tiempo"] for fila in grupo) / len(grupo)
        memorias = [fila["memoria_kb"] for fila in grupo if fila["memoria_kb"] != ""]
        memoria = f"{sum(memorias) / len(memorias):.1f} KB" if len(memorias) > 0 else "sin medir"
        print(f"{tecnica}, {parametros}, {sudoku}, {limite} s, {resueltas}/{len(grupo)}, {faltantes:.1f}, {tiempo:.3f} s, {memoria}")

if __name__ == "__main__":
    opciones = sys.argv[4:]
    if len(sys.argv) < 4 or any(opcion not in OPCIONES for opcion in opciones):
        print("Uso: python experimentos.py <corridas> <segundos> <archivo.csv> [parametros] [memoria] [generados]")
        print("Se pueden dar varios limites separados por coma, por ejemplo 1,5,10")
        print("Con la palabra parametros tambien prueba otros valores de la MRV y el recocido")
        print("Con la palabra memoria tambien mide la memoria pico, pero las corridas son mas lentas")
        print("Con la palabra generados usa sudokus del generador en vez de los de input")
        sys.exit(1)
    corridas = int(sys.argv[1])
    limites = [float(segundos) for segundos in sys.argv[2].split(",")]
    sudokus = sudokus_generados() if "generados" in opciones else sudokus_de_input()
    filas = []
    for sudoku in sudokus:
        filas += experimentar(sudoku, corridas, limites, "parametros" in opciones, "memoria" in opciones)
    guardar_csv(filas, sys.argv[3])
    print("Resultados guardados en", sys.argv[3])
    resumir(filas)
