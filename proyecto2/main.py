import sys
import time

import fuerza_bruta
import mrv
import recocido
from sudoku import contar_faltantes, leer_sudoku

# Asocia el nombre que se escribe en la terminal con la funcion que resuelve
TECNICAS = {
    "fuerza_bruta": fuerza_bruta.resolver,
    "mrv": mrv.resolver,
    "recocido": recocido.resolver,
}

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in TECNICAS:
        print("Uso: python main.py <tecnica> <archivo>")
        print("Tecnicas:", ", ".join(TECNICAS))
        sys.exit(1)
    resolver = TECNICAS[sys.argv[1]]
    tablero = leer_sudoku(sys.argv[2])
    inicio = time.perf_counter()
    resultado = resolver(tablero)
    segundos = time.perf_counter() - inicio
    for fila in resultado:
        print(fila)
    faltan = contar_faltantes(resultado)
    if faltan == 0:
        print("Resuelto")
    else:
        print("No resuelto, faltan", faltan, "numeros")
    print(f"Tiempo: {segundos:.3f} s")
