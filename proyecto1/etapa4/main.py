import sys

from calcparse import analizar_archivo

# Responsable: Sebas.
# TODO: Recibir el resultado del análisis y mostrar las estructuras creadas o los errores.

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Uso correcto: python main.py <archivo.txt>')
        sys.exit(1)

    analizar_archivo(sys.argv[1])
