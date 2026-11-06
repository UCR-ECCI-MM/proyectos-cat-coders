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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python sudoku.py <archivo>")
        sys.exit(1)
    tablero = leer_sudoku(sys.argv[1])
    # Muestra lo que se leyo para revisar que este bien
    for fila in tablero:
        print(fila)
