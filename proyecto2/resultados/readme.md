# Resultados de los experimentos

Cada CSV tiene una fila por corrida, con las columnas que explica el readme de `proyecto2`. En la
columna `parametros`, "por defecto" quiere decir los valores iniciales del código: en la MRV, 100
reinicios, desempate con la primera celda y número al azar, y en el recocido, `t0=1.0`, `alfa=0.95`, 500
iteraciones por temperatura y reinicio a las 20 temperaturas sin mejorar.

| Archivo | Corridas y límite | Qué se probó |
|---|---|---|
| `comparacion.csv` | 10 corridas con 1, 5, 10 y 30 s | Las tres técnicas con los valores iniciales en los sudokus de `input/` |
| `parametros-10s.csv` | 5 corridas de 10 s | Primera prueba de parámetros, cambiando uno a la vez |
| `generados-10s.csv` | 3 corridas de 10 s | Las tres técnicas en los 45 sudokus del generador |
| `memoria.csv` | 3 corridas de 10 s | Memoria pico de cada técnica |
| `parametros-30s.csv` | 10 corridas de 30 s | La prueba de parámetros con más tiempo |
| `generados-30s.csv` | 5 corridas de 30 s | Los sudokus del generador con más tiempo |
| `ajuste.csv` | 20 corridas de 10 s | Los valores de la propuesta (Lewis y De Souza y Romero), cambiando uno a la vez |
| `combinaciones.csv` | 20 corridas de 10 s | Los mejores valores del ajuste, juntos |
| `final-prueba.csv` | 20 corridas con 1, 5, 10 y 30 s | La MRV y el recocido con los valores elegidos, en los sudokus de `input/` |
| `final-generados.csv` | 5 corridas de 30 s | La MRV y el recocido con los valores elegidos, en los sudokus del generador |

Los valores elegidos son, en la MRV, la celda al azar y 1000 reinicios, y en el recocido, `t0=0.5`
y `alfa=0.9`. Los archivos `final` no traen la fuerza bruta porque siempre hace los mismos pasos:
sus resultados con 30 s están en `comparacion.csv` y `generados-30s.csv`.

Las rondas de `combinaciones` y `final` se corrieron con una copia de `experimentos.py` que solo
tenía esos valores en `VARIANTES`, con varios procesos a la vez (uno por sudoku), y después se
juntaron las filas en un solo archivo.
