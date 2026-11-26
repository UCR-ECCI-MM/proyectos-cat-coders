import os
import time

from main import TECNICAS
from sudoku import contar_faltantes, leer_sudoku

AZUL = "\033[94m"
NORMAL = "\033[0m"
SUDOKU_9X9 = "input/sudoku_9x9_1.txt"
SUDOKU_16X16 = "input/sudoku_16x16_2.txt"

# Imprime el tablero con los numeros nuevos en azul
def imprimir(original, resultado):
    ancho = len(str(len(resultado)))
    for fila_original, fila in zip(original, resultado):
        numeros = []
        for antes, numero in zip(fila_original, fila):
            texto = str(numero).rjust(ancho)
            if antes == 0 and numero != 0:
                texto = AZUL + texto + NORMAL
            numeros.append(texto)
        print(" ".join(numeros))

# Retorna el texto que dice si quedo resuelto o cuantos numeros faltan
def estado(faltan):
    if faltan == 0:
        return "Resuelto"
    return f"No resuelto, faltan {faltan}"

# Corre una tecnica sobre un sudoku, imprime el tablero y retorna los faltantes y el tiempo
def correr(tecnica, archivo, segundos):
    tablero = leer_sudoku(archivo)
    print(f"\n{tecnica} con {os.path.basename(archivo)}, limite de {segundos:g} s")
    inicio = time.perf_counter()
    resultado = TECNICAS[tecnica]([fila[:] for fila in tablero], segundos)
    tiempo = time.perf_counter() - inicio
    imprimir(tablero, resultado)
    faltan = contar_faltantes(resultado)
    print(f"{estado(faltan)}. Tiempo: {tiempo:.3f} s")
    return faltan, tiempo

# Corre las tres tecnicas sobre el mismo sudoku y al final imprime un resumen
def correr_tres(archivo, segundos):
    resumen = []
    for tecnica in TECNICAS:
        faltan, tiempo = correr(tecnica, archivo, segundos)
        resumen.append((tecnica, faltan, tiempo))
    print("\nResumen")
    for tecnica, faltan, tiempo in resumen:
        print(f"{tecnica:<14}{estado(faltan):<24}{tiempo:7.3f} s")

# Muestra una lista numerada y retorna el elemento escogido
def escoger(pregunta, elementos):
    for i, elemento in enumerate(elementos, 1):
        print(f"{i}. {elemento}")
    while True:
        respuesta = input(pregunta).strip()
        if respuesta.isdigit() and 1 <= int(respuesta) <= len(elementos):
            return elementos[int(respuesta) - 1]
        print("Opcion no valida")

# Pide la tecnica, el sudoku y el limite, y corre esa combinacion
def correr_una():
    tecnica = escoger("Tecnica: ", list(TECNICAS))
    archivo = escoger("Sudoku: ", sorted(os.listdir("input")))
    while True:
        texto = input("Limite en segundos (Enter para 30): ").strip()
        if texto == "":
            segundos = 30
            break
        try:
            segundos = float(texto)
            break
        except ValueError:
            print("Escriba un numero")
    correr(tecnica, os.path.join("input", archivo), segundos)

if __name__ == "__main__":
    os.system("")  # activa los colores en la consola de Windows
    while True:
        print("\nProyecto 2: sudoku")
        print("1. Las tres tecnicas en el 9x9, con 30 s")
        print("2. Las tres tecnicas en el 16x16 #2, con 10 s")
        print("3. Escoger tecnica, sudoku y limite")
        print("0. Salir")
        opcion = input("Opcion: ").strip()
        if opcion == "1":
            correr_tres(SUDOKU_9X9, 30)
        elif opcion == "2":
            correr_tres(SUDOKU_16X16, 10)
        elif opcion == "3":
            correr_una()
        elif opcion == "0":
            break
        else:
            print("Opcion no valida")
