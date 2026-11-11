import random
import sys

from sudoku import contar_faltantes, leer_sudoku

# Llena cada caja al azar con los numeros que le faltan
def llenar_cajas(tablero):
    tamano = len(tablero)
    caja = int(tamano ** 0.5)
    copia = [fila[:] for fila in tablero]
    for inicio_fila in range(0, tamano, caja):
        for inicio_columna in range(0, tamano, caja):
            presentes = set()
            vacias = []
            for i in range(inicio_fila, inicio_fila + caja):
                for j in range(inicio_columna, inicio_columna + caja):
                    if copia[i][j] == 0:
                        vacias.append((i, j))
                    else:
                        presentes.add(copia[i][j])
            faltantes = [n for n in range(1, tamano + 1) if n not in presentes]
            random.shuffle(faltantes)
            for (i, j), numero in zip(vacias, faltantes):
                copia[i][j] = numero
    return copia

# Cambia de lugar dos numeros de una caja que no sean pistas originales
def intercambiar(tablero, original):
    tamano = len(tablero)
    caja = int(tamano ** 0.5)
    inicio_fila = random.randrange(0, tamano, caja)
    inicio_columna = random.randrange(0, tamano, caja)
    vacias = []
    for i in range(inicio_fila, inicio_fila + caja):
        for j in range(inicio_columna, inicio_columna + caja):
            if original[i][j] == 0:
                vacias.append((i, j))
    if len(vacias) < 2:
        return None
    celda1, celda2 = random.sample(vacias, 2)
    f1, c1 = celda1
    f2, c2 = celda2
    tablero[f1][c1], tablero[f2][c2] = tablero[f2][c2], tablero[f1][c1]
    return celda1, celda2

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python recocido.py <archivo>")
        sys.exit(1)
    tablero = leer_sudoku(sys.argv[1])
    resultado = llenar_cajas(tablero)
    intercambiar(resultado, tablero)
    for fila in resultado:
        print(fila)
    print("Numeros que faltan:", contar_faltantes(resultado))
