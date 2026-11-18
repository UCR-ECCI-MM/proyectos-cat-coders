import random
import sys
import time

from sudoku import contar_faltantes, leer_sudoku, puede_ir

# Retorna la lista de numeros que pueden ir en una celda
def opciones_celda(tablero, fila, columna):
    opciones = []
    for numero in range(1, len(tablero) + 1):
        if puede_ir(tablero, fila, columna, numero):
            opciones.append(numero)
    return opciones

# Busca la celda vacia con menos opciones disponibles
def buscar_mejor_celda(tablero):
    mejor = None
    for fila in range(len(tablero)):
        for columna in range(len(tablero)):
            if tablero[fila][columna] == 0:
                opciones = opciones_celda(tablero, fila, columna)
                if mejor is None or len(opciones) < len(mejor[2]):
                    mejor = (fila, columna, opciones)
    return mejor

# Intenta llenar el sudoku eligiendo siempre la celda con menos opciones y se reinicia si falla
def resolver(tablero, segundos=60):
    mejor = [fila[:] for fila in tablero]
    menor_faltantes = contar_faltantes(mejor)
    limite = time.perf_counter() + segundos
    for _ in range(100):
        if time.perf_counter() > limite:
            break
        copia = [fila[:] for fila in tablero]
        while time.perf_counter() <= limite:
            celda = buscar_mejor_celda(copia)
            if celda is None:
                return copia
            fila, columna, opciones = celda
            if len(opciones) == 0:
                break
            copia[fila][columna] = random.choice(opciones)
        faltantes = contar_faltantes(copia)
        if faltantes < menor_faltantes:
            menor_faltantes = faltantes
            mejor = copia
    return mejor

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Uso: python mrv.py <archivo> [segundos]")
        sys.exit(1)
    tablero = leer_sudoku(sys.argv[1])
    segundos = 60
    if len(sys.argv) == 3:
        segundos = float(sys.argv[2])
    resultado = resolver(tablero, segundos)
    for fila in resultado:
        print(fila)
    print("Numeros que faltan:", contar_faltantes(resultado))
