import sys
import time
from sintactico import analizar_archivo
import aplicacion

def main(argumentos=None):
    if argumentos is None:
        argumentos = sys.argv[1:]
    if len(argumentos) != 1:
        print('Uso correcto: python3 main.py <archivo.txt>')
        return 1

    print("Analizando archivo, por favor espere...")
    inicio = time.time()
    resultado = analizar_archivo(argumentos[0])
    if resultado is None:
        return 1

    duracion = time.time() - inicio
    estructuras = resultado['estructuras']
    grafo = resultado['grafo']
    total_prefijos = len(estructuras.get('por_prefijo', {}))
    total_nodos = len(grafo)

    print(f"Archivo analizado correctamente en {duracion:.2f}s ({total_prefijos:,} prefijos, {total_nodos:,} AS en grafo).\n")

    # Menú interactivo
    while True:
        print("====== MENÚ PRINCIPAL ======")
        print("1. Reportar anomalías (Prefix Hijacking)")
        print("2. Buscar información de un AS")
        print("3. Buscar rutas entre dos prefijos")
        print("4. Salir")
        try:
            opcion = input("Seleccione una opción (1-4): ")
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo del programa...")
            break

        if opcion == '1':
            aplicacion.anomalias(estructuras)
        elif opcion == '2':
            aplicacion.buscar_as(estructuras)
        elif opcion == '3':
            aplicacion.buscar_rutas(grafo, estructuras)
        elif opcion == '4':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.\n")

    return 0


if __name__ == '__main__':
    sys.exit(main())
