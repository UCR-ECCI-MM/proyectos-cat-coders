import sys
from pprint import pprint
from calcparse import analizar_archivo

# Responsable: Sebas.
def main(argumentos=None):
    if argumentos is None:
        argumentos = sys.argv[1:]
    if len(argumentos) != 1:
        print('Uso correcto: python main.py <archivo.txt>')
        return 1

    resultado = analizar_archivo(argumentos[0])
    if resultado is None:
        return 1

    print('Archivo analizado correctamente.')
    print('Estructuras creadas:')
    pprint(resultado['estructuras'])
    print('\n')
    print('Grafo creado:')
    pprint(resultado['grafo'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
