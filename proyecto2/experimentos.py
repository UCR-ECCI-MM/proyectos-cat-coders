import csv
import os
import sys
import time

import fuerza_bruta
import mrv
from sudoku import contar_faltantes, leer_sudoku

# Tecnicas que se comparan, todas reciben el limite de tiempo
TECNICAS = {
    "fuerza_bruta": fuerza_bruta.resolver,
    "mrv": mrv.resolver,
}

# Columnas del CSV, una fila por corrida
COLUMNAS = ["tecnica", "sudoku", "tamano", "vacias", "limite", "corrida", "faltantes", "resuelto", "tiempo"]

# Retorna cuantas celdas vacias tiene el tablero
def contar_vacias(tablero):
    return sum(fila.count(0) for fila in tablero)

# Corre una tecnica sobre una copia del sudoku y retorna los faltantes y el tiempo
def correr(resolver, tablero, segundos):
    copia = [fila[:] for fila in tablero]
    inicio = time.perf_counter()
    resultado = resolver(copia, segundos)
    tiempo = time.perf_counter() - inicio
    return contar_faltantes(resultado), tiempo

# Corre cada tecnica varias veces sobre un sudoku y retorna una fila por corrida
def experimentar(archivo, corridas, segundos):
    tablero = leer_sudoku(os.path.join("input", archivo))
    filas = []
    for tecnica, resolver in TECNICAS.items():
        for corrida in range(1, corridas + 1):
            faltantes, tiempo = correr(resolver, tablero, segundos)
            print(tecnica, archivo, "corrida", corrida, "faltan", faltantes, f"{tiempo:.3f} s")
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
            })
    return filas

# Guarda las filas en un archivo CSV
def guardar_csv(filas, ruta):
    with open(ruta, "w", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        escritor.writeheader()
        escritor.writerows(filas)

# Imprime, por tecnica y sudoku, cuantas corridas resolvio y los promedios
def resumir(filas):
    grupos = {}
    for fila in filas:
        clave = (fila["tecnica"], fila["sudoku"])
        if clave not in grupos:
            grupos[clave] = []
        grupos[clave].append(fila)
    print("tecnica, sudoku, resueltas, faltantes promedio, tiempo promedio")
    for (tecnica, sudoku), grupo in grupos.items():
        resueltas = sum(fila["resuelto"] for fila in grupo)
        faltantes = sum(fila["faltantes"] for fila in grupo) / len(grupo)
        tiempo = sum(fila["tiempo"] for fila in grupo) / len(grupo)
        print(f"{tecnica}, {sudoku}, {resueltas}/{len(grupo)}, {faltantes:.1f}, {tiempo:.3f} s")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python experimentos.py <corridas> <segundos> <archivo.csv>")
        sys.exit(1)
    corridas = int(sys.argv[1])
    segundos = float(sys.argv[2])
    filas = []
    for archivo in sorted(os.listdir("input")):
        filas += experimentar(archivo, corridas, segundos)
    guardar_csv(filas, sys.argv[3])
    print("Resultados guardados en", sys.argv[3])
    resumir(filas)
