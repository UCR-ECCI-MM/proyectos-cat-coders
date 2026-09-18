import sys

from calcparse import analizar_archivo

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Uso correcto: python main.py <archivo.txt>')
        sys.exit(1)

    analizar_archivo(sys.argv[1])
