# Etapa 5: Aplicación completa

El programa lee un dump de MRT y revisa que no tenga errores léxicos, sintácticos ni semánticos.
Si el archivo está correcto, guarda los datos en las estructuras y en el grafo, y abre un menú con
las tres funcionalidades de la aplicación.

Este es el entregable final del Proyecto 1, "Rutas en Internet". El enunciado pide un parser hecho
con PLY que valide los dumps de MRT y una aplicación que use esos datos. La etapa 5 cumple con
todas las partes:

| Parte del enunciado | Dónde se cumple |
|---|---|
| Entrada: leer el dump y reportar cualquier error | `main.py` y `analizar_archivo` en `sintactico.py` |
| Analizador léxico: tokens válidos para los 7 campos | `lexico.py` |
| Analizador sintáctico: campos en orden y AS Path que empieza con el Peer AS | `sintactico.py` |
| Funcionalidad 1: prefijos con más de un AS de origen | Opción 1 del menú |
| Funcionalidad 2: aristas de un AS con sus prefijos y AS Path, en tabla | Opción 2 del menú |
| Funcionalidad 3: rutas entre dos prefijos | Opción 3 del menú |

Las estructuras y el grafo se llenan en las acciones del parser, mientras se lee cada registro
(`estructuras.py` y `grafo.py`). Por eso la funcionalidad 3 no recorre todos los datos: busca los
orígenes de cada prefijo directamente en un diccionario y después avanza solo por los vecinos del
grafo.

La funcionalidad 3 puede buscar todas las rutas, como pide el enunciado. Por defecto usa un tope
para responder al instante con los dumps completos, como se explica en la sección de la opción 3.

## Requisitos (Linux)

- Python 3
- `python3-venv`
- `make`

Se pueden instalar con:

```bash
sudo apt update
sudo apt install python3 python3-venv make
```

Para ver el grafo de rutas en el archivo HTML se necesita conexión a internet, porque el navegador
descarga la biblioteca vis-network y la fuente Oswald.

## Ejecutar el proyecto

Desde la carpeta `etapa5` ejecutar:

```bash
make run
```

La primera vez que se ejecuta pasa lo siguiente:

1. Se crea un entorno virtual llamado `.venv`.
2. Se actualiza `pip`.
3. Se instala la biblioteca `ply`.
4. Se ejecuta `main.py` con el archivo `input/prueba.txt`.

`input/prueba.txt` tiene errores a propósito, para mostrar cómo se reportan. Para abrir el menú con
un archivo correcto se usa:

```bash
make run ARCHIVO=input/as_conjuntos.txt
```

## Analizar un dump

Los dumps están en la carpeta `chunks`. Para analizar uno se usa:

```bash
make run-dump
```

Por defecto usa `chunk_aa.txt`, que tiene 500 000 líneas y tarda alrededor de 45 segundos en
cargar. Para usar otro se indica el nombre:

```bash
make run-dump CHUNK=chunk_ab.txt
```

Los dumps disponibles son `chunk_aa.txt`, `chunk_ab.txt`, `chunk_ac.txt`, `chunk_ad.txt` y
`chunk_ae.txt`. También está `muestra_5k_aa.txt`, que son las primeras 5000 líneas de
`chunk_aa.txt` y carga en menos de un segundo.

## Menú

Si el archivo no tiene errores, el programa muestra cuánto tardó la carga y abre este menú:

```text
====== MENÚ PRINCIPAL ======
1. Reportar anomalías (Prefix Hijacking)
2. Buscar información de un AS
3. Buscar rutas entre dos prefijos
4. Salir
```

### 1. Reportar anomalías

Muestra los prefijos que tienen más de un AS de origen, es decir, que más de un AS reporta como
propios. El origen es el último AS del AS Path. Para cada prefijo se muestran sus AS Path
agrupados por origen. Esto puede indicar un posible prefix hijacking. Igual que en el ejemplo del
enunciado, basta con dos orígenes distintos para reportar un prefijo.

### 2. Buscar información de un AS

Pide un número de AS y muestra en una tabla cada IP del peer, los prefijos que conoce por esa IP y
el AS Path de cada uno. Solo se pueden consultar los AS que aparecen como peer en el campo 5 del
archivo. La tabla se muestra de 15 en 15 filas y al final se puede exportar a `reporte_as.html`.

### 3. Buscar rutas entre dos prefijos

Pide dos prefijos, escritos igual que en el campo 6 del archivo (por ejemplo `37.52.0.0/14`).
Busca los AS de origen de cada prefijo y después busca en el grafo las rutas sin ciclos entre
esos orígenes. Como pide el enunciado, no se queda con la ruta más corta: muestra todas las que
encuentra, incluidas varias rutas desde un mismo AS. Primero encuentra las más cortas.

Antes de buscar, pregunta si se quieren todas las rutas sin límite:

- Si se responde que no, que es la opción por defecto, la búsqueda llega hasta 5 saltos y hasta
  200 rutas por cada par de orígenes. Así responde al instante incluso con los dumps completos.
- Si se responde que sí, busca todas las rutas, sin ningún tope. Con archivos pequeños termina y
  las muestra todas. Con un dump no termina, así que se presiona Ctrl+C para detener la búsqueda
  y se muestran las rutas encontradas hasta ese momento.

Con un dump no termina porque la cantidad de rutas crece demasiado con cada salto. Por ejemplo, en
`chunk_aa.txt`, entre el AS 15169 (Google) y el AS 13335 (Cloudflare) hay 80 rutas de hasta 3
saltos, 7277 de hasta 4 y 178 806 de hasta 5. Incluso en `muestra_5k_aa.txt`, que tiene solo 149
AS, la búsqueda sin tope pasa de 400 000 rutas en unos 4 segundos. El tope por defecto de 5 saltos
cubre casi todas las rutas reales: en `chunk_aa.txt`, el 98 % de los AS Path tienen 5 saltos o
menos.

El archivo `input/rutas_todas.txt` sirve para ver la diferencia entre los dos modos. Su grafo tiene
ciclos y una cadena larga de 6 saltos. Se usa con `make run ARCHIVO=input/rutas_todas.txt`, la
opción 3, el prefijo A `10.0.0.0/8` y el prefijo B `20.0.0.0/8`. Si se responde que no, se
encuentran 8 rutas, todas de hasta 5 saltos. Si se responde que sí, se encuentran 9: las mismas 8
y la de 6 saltos `100 -> 900 -> 901 -> 902 -> 903 -> 904 -> 600`. Los ciclos no dejan pegada la
búsqueda, porque una ruta nunca repite un AS.

Al final se puede generar `visualizador_rutas.html`, que dibuja las 20 rutas más cortas de
izquierda a derecha. El origen de A va en azul a la izquierda, el origen de B en celeste a la
derecha y los AS intermedios en el medio.

## Ver los archivos HTML

Los archivos HTML se crean en la carpeta `etapa5`. Desde WSL se pueden abrir en el navegador de
Windows con:

```bash
explorer.exe visualizador_rutas.html
```

## Pruebas

Para revisar que se reportan los errores:

```bash
make test
```

Corre `main.py` con los archivos de `input/` que tienen errores: `archivo.txt`, `registro.txt`,
`as_path.txt`, `elemento_as.txt`, `lista_as.txt`, `numero_as.txt` y `prueba.txt`. Cada uno
muestra sus errores.

Para probar con archivos válidos:

```bash
make test-etapa4
```

Corre `main.py` con `as_repetidos.txt` y `as_conjuntos.txt`. Como son válidos, cada uno abre el
menú, y se sale con la opción 4.

Para la funcionalidad 3 está `input/rutas_todas.txt`, que se explica en la sección de la opción 3.

## Errores

Si el archivo tiene errores, se reportan y no se abre el menú.

Un error de sintaxis muestra el token, su tipo y la línea:

```text
Error sintáctico en token '1' (NUMBER1TO9) en línea 7.
```

Un error léxico muestra el valor que no es válido:

```text
Error léxico en línea 9: '7493232523432' tiene 13 digitos, el maximo del formato es 10
```

Un error semántico muestra el valor que pasa del máximo permitido:

```text
Error semántico en línea 8: el timestamp 4294967300 pasa del máximo 2147483647.
```

## Limpieza

Para borrar los archivos HTML generados y la carpeta `__pycache__`:

```bash
make clean
```

Para borrar además el entorno virtual `.venv`:

```bash
make clean-all
```