import math
import random
import sys
import time

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

# Resuelve el sudoku con recocido simulado y retorna el mejor tablero encontrado
def resolver(tablero, segundos=60, t0=1.0, alfa=0.95, iteraciones=500):
    limite = time.perf_counter() + segundos
    actual = llenar_cajas(tablero)
    costo = contar_faltantes(actual)
    mejor = [fila[:] for fila in actual]
    menor_costo = costo
    temperatura = t0
    sin_mejorar = 0
    while costo > 0 and time.perf_counter() <= limite:
        mejoro = False
        for _ in range(iteraciones):
            if time.perf_counter() > limite:
                return mejor
            cambio = intercambiar(actual, tablero)
            if cambio is None:
                continue
            nuevo_costo = contar_faltantes(actual)
            delta = nuevo_costo - costo
            if delta <= 0 or random.random() < math.exp(-delta / temperatura):
                costo = nuevo_costo
                if costo < menor_costo:
                    menor_costo = costo
                    mejor = [fila[:] for fila in actual]
                    mejoro = True
                if costo == 0:
                    return actual
            else:
                (f1, c1), (f2, c2) = cambio
                actual[f1][c1], actual[f2][c2] = actual[f2][c2], actual[f1][c1]
        temperatura *= alfa
        if mejoro:
            sin_mejorar = 0
        else:
            sin_mejorar += 1
        if sin_mejorar == 20:
            actual = llenar_cajas(tablero)
            costo = contar_faltantes(actual)
            if costo < menor_costo:
                menor_costo = costo
                mejor = [fila[:] for fila in actual]
            temperatura = t0
            sin_mejorar = 0
    return mejor

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("Uso: python recocido.py <archivo> [segundos]")
        sys.exit(1)
    tablero = leer_sudoku(sys.argv[1])
    segundos = 60
    if len(sys.argv) == 3:
        segundos = float(sys.argv[2])
    resultado = resolver(tablero, segundos)
    for fila in resultado:
        print(fila)
    print("Numeros que faltan:", contar_faltantes(resultado))
