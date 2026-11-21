# Proyecto 2: Sudoku

El programa recibe un sudoku sin resolver y devuelve la cuadrícula completa, o avisa que no la
encontró a tiempo. Lo resuelve con tres técnicas y las compara por el porcentaje de veces que
encuentran la solución y por el tiempo que tardan.

Un sudoku es una cuadrícula de n² × n² dividida en cajas de n × n. Algunas celdas traen pistas y
el objetivo es llenar el resto de modo que cada fila, cada columna y cada caja tenga los números
del 1 al n² una sola vez. Se trabaja con sudokus de 9 × 9 y de 16 × 16.

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
