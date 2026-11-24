import csv
import os
import sys
import time
import tracemalloc

import fuerza_bruta
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
VARIANTES = {
    "fuerza_bruta": [{}],
    "mrv": [{}, {"reinicios": 1000}, {"reinicios": 10000}, {"celda_azar": True}, {"valor_azar": False}],
    "recocido": [{}, {"t0": None}, {"t0": 0.5}, {"t0": 5.0}, {"alfa": 0.9}, {"alfa": 0.99},
                 {"iteraciones": 100}, {"iteraciones": 2000}, {"reinicio": 5}, {"reinicio": 100}],
}

# Palabras que se pueden agregar al final del comando
OPCIONES = ["parametros", "memoria"]

# Columnas del CSV, una fila por corrida
COLUMNAS = ["tecnica", "parametros", "sudoku", "tamano", "vacias", "limite", "corrida", "faltantes", "resuelto", "tiempo", "memoria_kb"]

# Retorna cuantas celdas vacias tiene el tablero
def contar_vacias(tablero):
    return sum(fila.count(0) for fila in tablero)

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
def experimentar(archivo, corridas, limites, probar_parametros, medir_memoria):
    tablero = leer_sudoku(os.path.join("input", archivo))
    filas = []
    for tecnica, resolver in TECNICAS.items():
        variantes = VARIANTES[tecnica] if probar_parametros else [{}]
        for parametros in variantes:
            for segundos in limites:
                for corrida in range(1, corridas + 1):
                    faltantes, tiempo, memoria = correr(resolver, tablero, segundos, parametros, medir_memoria)
                    print(tecnica, describir(parametros), archivo, "limite", segundos, "corrida", corrida, "faltan", faltantes, f"{tiempo:.3f} s", memoria)
                    filas.append({
                        "tecnica": tecnica,
                        "parametros": describir(parametros),
                        "sudoku": archivo,
                        "tamano": len(tablero),
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
        print("Uso: python experimentos.py <corridas> <segundos> <archivo.csv> [parametros] [memoria]")
        print("Se pueden dar varios limites separados por coma, por ejemplo 1,5,10")
        print("Con la palabra parametros tambien prueba otros valores de la MRV y el recocido")
        print("Con la palabra memoria tambien mide la memoria pico, pero las corridas son mas lentas")
        sys.exit(1)
    corridas = int(sys.argv[1])
    limites = [float(segundos) for segundos in sys.argv[2].split(",")]
    filas = []
    for archivo in sorted(os.listdir("input")):
        filas += experimentar(archivo, corridas, limites, "parametros" in opciones, "memoria" in opciones)
    guardar_csv(filas, sys.argv[3])
    print("Resultados guardados en", sys.argv[3])
    resumir(filas)
