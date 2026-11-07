import sys

# Lee el sudoku de un archivo y lo retorna como una lista de filas
def leer_sudoku(ruta):
    tablero = []
    with open(ruta) as archivo:
        for linea in archivo:
            if linea.strip():
                fila = [int(numero) for numero in linea.split()]
                tablero.append(fila)
    return tablero

# Retorna True si el numero no se repite en la fila, la columna ni la caja
def puede_ir(tablero, fila, columna, numero):
    tamano = len(tablero)
    caja = int(tamano ** 0.5)
    for i in range(tamano):
        if tablero[fila][i] == numero or tablero[i][columna] == numero:
            return False
    inicio_fila = fila - fila % caja
    inicio_columna = columna - columna % caja
    for i in range(inicio_fila, inicio_fila + caja):
        for j in range(inicio_columna, inicio_columna + caja):
            if tablero[i][j] == numero:
                return False
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python sudoku.py <archivo>")
        sys.exit(1)
    tablero = leer_sudoku(sys.argv[1])
    # Muestra lo que se leyo para revisar que este bien
    for fila in tablero:
        print(fila)
