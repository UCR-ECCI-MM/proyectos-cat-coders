# Proyecto 2: Sudoku

El programa recibe un sudoku sin resolver y devuelve la cuadrícula completa, o avisa que no la
encontró a tiempo. Lo resuelve con tres técnicas y las compara por el porcentaje de veces que
encuentran la solución y por el tiempo que tardan.

Un sudoku es una cuadrícula de n² × n² dividida en cajas de n × n. Algunas celdas traen pistas y
el objetivo es llenar el resto de modo que cada fila, cada columna y cada caja tenga los números
del 1 al n² una sola vez. Se trabaja con sudokus de 4 × 4, 9 × 9 y 16 × 16.

## Técnicas

| Técnica | Idea |
|---|---|
| Fuerza bruta | Vuelta atrás (backtracking) en orden fijo, celda por celda |
| Heurística MRV | Llena primero la celda con menos opciones, nunca se devuelve y se reinicia si falla |
| Simulated annealing | Intercambia dos celdas de una misma caja hasta que no falte ningún número en filas y columnas |

## Archivos de entrada

Los sudokus de prueba están en `input/`: uno de 9 × 9 y dos de 16 × 16. Cada línea del archivo
es una fila del sudoku, con los números separados por espacios. Las celdas vacías se escriben
con 0.

## Generador

`generador.py` crea un sudoku nuevo con el mismo formato. Primero llena una cuadrícula completa al
azar y después deja como pistas solo una proporción `p` de las celdas:

```bash
python3 generador.py <tamano> <p> <semilla> <archivo>
```

Por ejemplo, `python3 generador.py 9 0.4 7 nuevo.txt` crea un sudoku de 9 × 9 con el 40 % de las
celdas como pistas, y se resuelve con `python3 main.py mrv nuevo.txt`. Con la misma semilla
siempre sale el mismo sudoku.

## Cómo ejecutar

Solo se necesita Python 3, sin librerías externas. En Linux el comando es `python3` y en
Windows es `python`. Los comandos se corren desde la carpeta `proyecto2`:

```bash
python3 main.py <tecnica> <archivo> [segundos]
```

Las técnicas son `fuerza_bruta`, `mrv` y `recocido`. El último argumento es el límite de tiempo en
segundos, que por defecto es 60. Si se acaba, la técnica devuelve el mejor tablero al que llegó. Por
ejemplo, el recocido con un límite de 10 segundos:

```bash
python3 main.py recocido input/sudoku_9x9_1.txt 10
```

El programa imprime el tablero al que llegó, si quedó resuelto y cuánto tardó. Si no lo
resolvió, dice cuántos números faltan en sus filas, columnas y cajas. Ese número mide qué tan
cerca quedó de la solución, y 0 quiere decir resuelto.

Cada técnica también se puede correr sola, con el mismo límite opcional:

```bash
python3 fuerza_bruta.py input/sudoku_16x16_2.txt 10
```

## Experimentos

`experimentos.py` corre las tres técnicas varias veces sobre cada sudoku de `input/`, con el mismo
límite de tiempo, y guarda una fila por corrida en un archivo CSV:

```bash
python3 experimentos.py <corridas> <segundos> <archivo.csv> [parametros] [memoria] [generados]
```

Por ejemplo, `python3 experimentos.py 5 10 resultados.csv` corre 5 veces cada técnica con un
límite de 10 segundos. Se pueden dar varios límites separados por coma, como en
`python3 experimentos.py 3 1,5,10 resultados.csv`, para ver cómo mejora cada técnica con más tiempo.

Al final se pueden agregar estas palabras, en cualquier orden:

| Palabra | Qué hace |
|---|---|
| `parametros` | Prueba otros valores de los parámetros, cambiando uno a la vez. En la MRV: los reinicios y si la celda o el número se escogen al azar. En el recocido: la temperatura inicial `t0` (`t0=None` la calcula con la desviación estándar del costo), el factor de enfriamiento `alfa`, las iteraciones por temperatura y cuántas temperaturas sin mejorar espera antes de reiniciar |
| `memoria` | Mide la memoria pico de cada corrida. Hace más lentas las corridas, por eso conviene medirla aparte de los tiempos |
| `generados` | En vez de los sudokus de `input/`, usa sudokus del generador de 4 × 4, 9 × 9 y 16 × 16, con proporciones de pistas de 0,2 a 0,6 y tres semillas cada uno |

Cada fila del CSV trae la técnica, los parámetros, el sudoku, su tamaño, la proporción de pistas
`p`, la semilla (solo en los generados), cuántas celdas vacías tiene, el límite, el número de
corrida, los números que faltan, si quedó resuelto (1 o 0), el tiempo en segundos y la memoria en
KB (vacía si no se pidió). Al final se imprime un resumen con cuántas corridas resolvió cada técnica
y los promedios.

Los CSV de las corridas que usamos en el análisis están en `resultados/`. Su readme explica qué se
probó en cada uno.
