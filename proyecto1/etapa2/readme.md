# Etapa 2 - Lexer

## Requisitos (Linux)

- Python 3
- `python3-venv`
- `make`

Se pueden instalar con:

```bash
sudo apt update
sudo apt install python3 python3-venv make
```

## Ejecutar el proyecto

Desde la carpeta del proyecto ejecutar:

```bash
make run
```

La primera vez que se ejecuta va a pasar lo siguiente:

1. Se crea un entorno virtual llamado `.venv`.
2. Se actualiza `pip`.
3. Se instala la librería `ply`.
4. Se ejecuta `calclex.py` usando `prueba.txt`.

Y para volver a ejecutar es igual con el mismo comando:

```bash
make run
```

## Archivo de entrada

El programa usa por defecto:

```text
prueba.txt
```

Esto está definido en el `Makefile` por: "ARCHIVO = prueba.txt"

Si se desea utilizar otro archivo, se puede cambiar esa línea por:

```makefile
ARCHIVO = otro_archivo.txt
```
o tambien se podria el siguiente comando para usar otro archivo como lo puede ser un dump:

```text
make run ARCHIVO=nombreArchivo.txt
```

## Archivo de salida

Al ejecutar el programa se crea el archivo:
```text
salida_prueba.txt
```

Este archivo contiene los tokens válidos encontrados por el analizador léxico.

## Limpieza

Para eliminar los archivos de salida y la carpeta `__pycache__`:

```bash
make clean
```

## Eliminar entorno virtual

Para eliminar los archivos generados y además borrar `.venv`:

```bash
make clean-all
```
