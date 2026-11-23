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

# Columnas del CSV, una fila por corrida
COLUMNAS = ["tecnica", "sudoku", "tamano", "vacias", "limite", "corrida", "faltantes", "resuelto", "tiempo", "memoria_kb"]

# Retorna cuantas celdas vacias tiene el tablero
def contar_vacias(tablero):
    return sum(fila.count(0) for fila in tablero)

# Corre una tecnica sobre una copia del sudoku y retorna los faltantes, el tiempo y la memoria pico
def correr(resolver, tablero, segundos):
    copia = [fila[:] for fila in tablero]
    tracemalloc.start()
    inicio = time.perf_counter()
    resultado = resolver(copia, segundos)
    tiempo = time.perf_counter() - inicio
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return contar_faltantes(resultado), tiempo, pico / 1024

# Corre cada tecnica varias veces con cada limite y retorna una fila por corrida
def experimentar(archivo, corridas, limites):
    tablero = leer_sudoku(os.path.join("input", archivo))
    filas = []
    for tecnica, resolver in TECNICAS.items():
        for segundos in limites:
            for corrida in range(1, corridas + 1):
                faltantes, tiempo, memoria = correr(resolver, tablero, segundos)
                print(tecnica, archivo, "limite", segundos, "corrida", corrida, "faltan", faltantes, f"{tiempo:.3f} s", f"{memoria:.1f} KB")
                filas.append({
                    "tecnica": tecnica,
                    "sudoku": archivo,
                    "tamano": len(tablero),
                    "vacias": contar_vacias(tablero),
                    "limite": segundos,
                    "corrida": corrida,
                    "faltantes": faltantes,
                    "resuelto": 1 if faltantes == 0 else 0,
                    "tiempo": round(tiempo, 3),
                    "memoria_kb": round(memoria, 1),
                })
    return filas

# Guarda las filas en un archivo CSV
def guardar_csv(filas, ruta):
    with open(ruta, "w", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        escritor.writeheader()
        escritor.writerows(filas)

# Imprime, por tecnica, sudoku y limite, cuantas corridas resolvio y los promedios
def resumir(filas):
    grupos = {}
    for fila in filas:
        clave = (fila["tecnica"], fila["sudoku"], fila["limite"])
        if clave not in grupos:
            grupos[clave] = []
        grupos[clave].append(fila)
    print("tecnica, sudoku, limite, resueltas, faltantes promedio, tiempo promedio, memoria promedio")
    for (tecnica, sudoku, limite), grupo in grupos.items():
        resueltas = sum(fila["resuelto"] for fila in grupo)
        faltantes = sum(fila["faltantes"] for fila in grupo) / len(grupo)
        tiempo = sum(fila["tiempo"] for fila in grupo) / len(grupo)
        memoria = sum(fila["memoria_kb"] for fila in grupo) / len(grupo)
        print(f"{tecnica}, {sudoku}, {limite} s, {resueltas}/{len(grupo)}, {faltantes:.1f}, {tiempo:.3f} s, {memoria:.1f} KB")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python experimentos.py <corridas> <segundos> <archivo.csv>")
        print("Se pueden dar varios limites separados por coma, por ejemplo 1,5,10")
        sys.exit(1)
    corridas = int(sys.argv[1])
    limites = [float(segundos) for segundos in sys.argv[2].split(",")]
    filas = []
    for archivo in sorted(os.listdir("input")):
        filas += experimentar(archivo, corridas, limites)
    guardar_csv(filas, sys.argv[3])
    print("Resultados guardados en", sys.argv[3])
    resumir(filas)
