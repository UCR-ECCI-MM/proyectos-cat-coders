# Etapa 4 - Creación de estructuras de datos

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
4. Se ejecuta `main.py`, que llama al parser usando `input/prueba.txt`.

Y para volver a ejecutar es igual con el mismo comando:

```bash
make run
```

## Archivo de entrada

El programa usa por defecto:

```text
input/prueba.txt
```

Esto está definido en el `Makefile` por: "ARCHIVO = input/prueba.txt"

Si se desea utilizar otro archivo, se puede cambiar esa línea por:

```makefile
ARCHIVO = otro_archivo.txt
```

o tambien se podria el siguiente comando para usar otro archivo:

```text
make run ARCHIVO=nombreArchivo.txt
```

## Analizar un dump

Para correr el lexer contra uno de los dumps de la etapa 2:

```bash
make run-dump
```

Por defecto usa `chunk_aa.txt` de `../etapa2/input`. Para usar otro:

```text
make run-dump CHUNK=chunk_ab.txt
```

## Salida del programa

A diferencia de la etapa 2, el parser no genera un archivo de salida: imprime el
resultado en la terminal.

Si el archivo no tiene errores imprime:

```text
Archivo sintácticamente correcto.
```

Si encuentra un error de sintaxis imprime el token, su tipo y la línea:

```text
Error sintáctico en token '83.68.192.0' (PEER_IP) en línea 7.
```

Y si el archivo se termina antes de completar un registro:

```text
Error sintáctico: fin de archivo inesperado.
```

Los errores léxicos los sigue reportando `calclex.py`.

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
