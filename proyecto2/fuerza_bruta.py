import sys
import time

from sudoku import contar_faltantes, leer_sudoku, puede_ir

# Retorna la fila y la columna de la primera celda vacia, o None si no hay
def buscar_vacia(tablero):
    for fila in range(len(tablero)):
        for columna in range(len(tablero)):
            if tablero[fila][columna] == 0:
                return fila, columna
    return None

# Llena las celdas vacias con backtracking, retorna True si lo logra antes del limite
def llenar(tablero, limite, mejor):
    if time.perf_counter() > limite:
        return False
    vacia = buscar_vacia(tablero)
    if vacia is None:
        return True
    fila, columna = vacia
    # Guarda una copia cada vez que llega mas lejos que nunca
    posicion = fila * len(tablero) + columna
    if posicion > mejor["posicion"]:
        mejor["posicion"] = posicion
        mejor["tablero"] = [f[:] for f in tablero]
    for numero in range(1, len(tablero) + 1):
        if puede_ir(tablero, fila, columna, numero):
            tablero[fila][columna] = numero
            if llenar(tablero, limite, mejor):
                return True
            tablero[fila][columna] = 0
    return False

# Retorna el tablero resuelto, o el mas lleno al que llego si se acabo el tiempo
def resolver(tablero, segundos=60):
    copia = [fila[:] for fila in tablero]
    mejor = {"tablero": [fila[:] for fila in tablero], "posicion": -1}
    limite = time.perf_counter() + segundos
    if llenar(copia, limite, mejor):
        return copia
    return mejor["tablero"]

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Uso: python fuerza_bruta.py <archivo> [segundos]")
        sys.exit(1)
    tablero = leer_sudoku(sys.argv[1])
    segundos = 60
    if len(sys.argv) == 3:
        segundos = float(sys.argv[2])
    resultado = resolver(tablero, segundos)
    for fila in resultado:
        print(fila)
    print("Numeros que faltan:", contar_faltantes(resultado))
