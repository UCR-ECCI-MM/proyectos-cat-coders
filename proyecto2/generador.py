import random
import sys

from sudoku import contar_faltantes, puede_ir

# Busca la primera celda vacia del tablero
def buscar_vacia(tablero):
    for fila in range(len(tablero)):
        for columna in range(len(tablero)):
            if tablero[fila][columna] == 0:
                return fila, columna
    return None

# Llena el tablero con backtracking al azar sin pasarse del tope de pasos
def llenar(tablero, pasos, tope):
    if pasos[0] >= tope:
        return False
    vacia = buscar_vacia(tablero)
    if vacia is None:
        return True
    fila, columna = vacia
    numeros = list(range(1, len(tablero) + 1))
    random.shuffle(numeros)
    for numero in numeros:
        if puede_ir(tablero, fila, columna, numero):
            tablero[fila][columna] = numero
            pasos[0] += 1
            if llenar(tablero, pasos, tope):
                return True
            tablero[fila][columna] = 0
    return False

# Genera una cuadricula completa valida de tamano x tamano
def cuadricula_completa(tamano):
    tope = tamano * tamano * 20
    while True:
        tablero = [[0] * tamano for _ in range(tamano)]
        pasos = [0]
        if llenar(tablero, pasos, tope):
            return tablero

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python generador.py <tamano>")
        sys.exit(1)
    tamano = int(sys.argv[1])
    tablero = cuadricula_completa(tamano)
    for fila in tablero:
        print(fila)
    print("Numeros que faltan:", contar_faltantes(tablero))
