import sys

from sudoku import contar_faltantes, leer_sudoku, puede_ir

# Retorna la fila y la columna de la primera celda vacia, o None si no hay
def buscar_vacia(tablero):
    for fila in range(len(tablero)):
        for columna in range(len(tablero)):
            if tablero[fila][columna] == 0:
                return fila, columna
    return None

# Llena las celdas vacias con backtracking, retorna True si lo logra
def llenar(tablero):
    vacia = buscar_vacia(tablero)
    if vacia is None:
        return True
    fila, columna = vacia
    for numero in range(1, len(tablero) + 1):
        if puede_ir(tablero, fila, columna, numero):
            tablero[fila][columna] = numero
            if llenar(tablero):
                return True
            tablero[fila][columna] = 0
    return False

# Retorna una copia del tablero con las celdas que logro llenar
def resolver(tablero):
    copia = [fila[:] for fila in tablero]
    llenar(copia)
    return copia

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python fuerza_bruta.py <archivo>")
        sys.exit(1)
    tablero = leer_sudoku(sys.argv[1])
    resultado = resolver(tablero)
    for fila in resultado:
        print(fila)
    print("Numeros que faltan:", contar_faltantes(resultado))
