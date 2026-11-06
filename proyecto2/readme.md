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

Los sudokus de prueba están en `input/`. Cada línea del archivo es una fila del sudoku, con los
números separados por espacios. Las celdas vacías se escriben con 0.

## Cómo ejecutar

Pendiente. Se completa cuando el programa esté listo.