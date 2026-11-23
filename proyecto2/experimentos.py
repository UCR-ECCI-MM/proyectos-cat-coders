import csv
import os
import sys
import time
import tracemalloc

import fuerza_bruta
import mrv
import recocido
from sudoku import contar_faltantes, leer_sudoku

# Tecnicas que se comparan, todas reciben el limite de tiempo
TECNICAS = {
    "fuerza_bruta": fuerza_bruta.resolver,
    "mrv": mrv.resolver,
    "recocido": recocido.resolver,
}

# Columnas del CSV, una fila por corrida
COLUMNAS = ["tecnica", "sudoku", "tamano", "vacias", "limite", "corrida", "faltantes", "resuelto", "tiempo", "memoria_kb"]

# Retorna cuantas celdas vacias tiene el tablero
def contar_vacias(tablero):
    return sum(fila.count(0) for fila in tablero)

# Corre una tecnica sobre una copia del sudoku y retorna los faltantes, el tiempo y la memoria pico
# La memoria solo se mide si se pide, porque tracemalloc hace mas lenta la corrida
def correr(resolver, tablero, segundos, medir_memoria):
    copia = [fila[:] for fila in tablero]
    if medir_memoria:
        tracemalloc.start()
    inicio = time.perf_counter()
    resultado = resolver(copia, segundos)
    tiempo = time.perf_counter() - inicio
    memoria = ""
    if medir_memoria:
        _, pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        memoria = round(pico / 1024, 1)
    return contar_faltantes(resultado), tiempo, memoria

# Corre cada tecnica varias veces con cada limite y retorna una fila por corrida
def experimentar(archivo, corridas, limites, medir_memoria):
    tablero = leer_sudoku(os.path.join("input", archivo))
    filas = []
    for tecnica, resolver in TECNICAS.items():
        for segundos in limites:
            for corrida in range(1, corridas + 1):
                faltantes, tiempo, memoria = correr(resolver, tablero, segundos, medir_memoria)
                print(tecnica, archivo, "limite", segundos, "corrida", corrida, "faltan", faltantes, f"{tiempo:.3f} s", memoria)
                filas.append({
                    "tecnica": tecnica,
                    "sudoku": archivo,
                    "tamano": len(tablero),
                    "vacias": contar_vacias(tablero),
                    "limite": segundos,
                    "corrida": corrida,
                    "faltantes": faltantes,
                    "resuelto": 1 if faltantes == 0 else 0,
                    "tiempo": round(tiempo, 3),
                    "memoria_kb": memoria,
                })
    return filas

# Guarda las filas en un archivo CSV
def guardar_csv(filas, ruta):
    with open(ruta, "w", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        escritor.writeheader()
        escritor.writerows(filas)

# Imprime, por tecnica, sudoku y limite, cuantas corridas resolvio y los promedios
def resumir(filas):
    grupos = {}
    for fila in filas:
        clave = (fila["tecnica"], fila["sudoku"], fila["limite"])
        if clave not in grupos:
            grupos[clave] = []
        grupos[clave].append(fila)
    print("tecnica, sudoku, limite, resueltas, faltantes promedio, tiempo promedio, memoria promedio")
    for (tecnica, sudoku, limite), grupo in grupos.items():
        resueltas = sum(fila["resuelto"] for fila in grupo)
        faltantes = sum(fila["faltantes"] for fila in grupo) / len(grupo)
        tiempo = sum(fila["tiempo"] for fila in grupo) / len(grupo)
        memorias = [fila["memoria_kb"] for fila in grupo if fila["memoria_kb"] != ""]
        memoria = f"{sum(memorias) / len(memorias):.1f} KB" if len(memorias) > 0 else "sin medir"
        print(f"{tecnica}, {sudoku}, {limite} s, {resueltas}/{len(grupo)}, {faltantes:.1f}, {tiempo:.3f} s, {memoria}")

if __name__ == "__main__":
    if len(sys.argv) not in (4, 5) or (len(sys.argv) == 5 and sys.argv[4] != "memoria"):
        print("Uso: python experimentos.py <corridas> <segundos> <archivo.csv> [memoria]")
        print("Se pueden dar varios limites separados por coma, por ejemplo 1,5,10")
        print("Con la palabra memoria al final tambien mide la memoria pico, pero las corridas son mas lentas")
        sys.exit(1)
    corridas = int(sys.argv[1])
    limites = [float(segundos) for segundos in sys.argv[2].split(",")]
    medir_memoria = len(sys.argv) == 5
    filas = []
    for archivo in sorted(os.listdir("input")):
        filas += experimentar(archivo, corridas, limites, medir_memoria)
    guardar_csv(filas, sys.argv[3])
    print("Resultados guardados en", sys.argv[3])
    resumir(filas)
