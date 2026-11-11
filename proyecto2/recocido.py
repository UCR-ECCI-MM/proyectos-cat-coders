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

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python recocido.py <archivo>")
        sys.exit(1)
    tablero = leer_sudoku(sys.argv[1])
    resultado = llenar_cajas(tablero)
    for fila in resultado:
        print(fila)
    print("Numeros que faltan:", contar_faltantes(resultado))
