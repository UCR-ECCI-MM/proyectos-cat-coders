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

# Corre una tecnica sobre una copia del sudoku y retorna los faltantes y el tiempo
def correr(resolver, tablero, segundos):
    copia = [fila[:] for fila in tablero]
    inicio = time.perf_counter()
    resultado = resolver(copia, segundos)
    tiempo = time.perf_counter() - inicio
    return contar_faltantes(resultado), tiempo

# Corre cada tecnica varias veces sobre un sudoku e imprime cada corrida
def experimentar(archivo, corridas, segundos):
    tablero = leer_sudoku(os.path.join("input", archivo))
    for tecnica, resolver in TECNICAS.items():
        for corrida in range(1, corridas + 1):
            faltantes, tiempo = correr(resolver, tablero, segundos)
            print(tecnica, archivo, "corrida", corrida, "faltan", faltantes, f"{tiempo:.3f} s")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python experimentos.py <corridas> <segundos>")
        sys.exit(1)
    corridas = int(sys.argv[1])
    segundos = float(sys.argv[2])
    for archivo in sorted(os.listdir("input")):
        experimentar(archivo, corridas, segundos)
