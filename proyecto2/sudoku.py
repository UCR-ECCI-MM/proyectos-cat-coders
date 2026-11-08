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

# Retorna cuantos numeros faltan en filas, columnas y cajas, 0 si esta resuelto
def contar_faltantes(tablero):
    tamano = len(tablero)
    caja = int(tamano ** 0.5)
    faltan = 0
    for i in range(tamano):
        fila = {tablero[i][j] for j in range(tamano)}
        columna = {tablero[j][i] for j in range(tamano)}
        faltan += tamano - len(fila - {0})
        faltan += tamano - len(columna - {0})
    for inicio_fila in range(0, tamano, caja):
        for inicio_columna in range(0, tamano, caja):
            numeros = set()
            for i in range(inicio_fila, inicio_fila + caja):
                for j in range(inicio_columna, inicio_columna + caja):
                    numeros.add(tablero[i][j])
            faltan += tamano - len(numeros - {0})
    return faltan

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python sudoku.py <archivo>")
        sys.exit(1)
    tablero = leer_sudoku(sys.argv[1])
    # Muestra lo que se leyo para revisar que este bien
    for fila in tablero:
        print(fila)
