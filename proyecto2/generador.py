import random
import sys

from sudoku import puede_ir

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

# Genera un sudoku dejando una proporcion p de celdas como pistas
def generar(tamano, p, semilla=None):
    random.seed(semilla)
    tablero = cuadricula_completa(tamano)
    celdas = [(fila, columna) for fila in range(tamano) for columna in range(tamano)]
    pistas = set(random.sample(celdas, round(p * tamano * tamano)))
    for fila in range(tamano):
        for columna in range(tamano):
            if (fila, columna) not in pistas:
                tablero[fila][columna] = 0
    return tablero

# Guarda el tablero en un archivo con una fila por linea y numeros separados por espacios
def guardar_sudoku(tablero, ruta):
    with open(ruta, "w") as archivo:
        for fila in tablero:
            archivo.write(" ".join(str(numero) for numero in fila) + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python generador.py <tamano> <p> <semilla> <archivo>")
        sys.exit(1)
    tamano = int(sys.argv[1])
    p = float(sys.argv[2])
    semilla = int(sys.argv[3])
    ruta = sys.argv[4]
    tablero = generar(tamano, p, semilla)
    guardar_sudoku(tablero, ruta)
