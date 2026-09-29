# Entregable 5: Distribucion

En `aplicacion.py` estan las 3 funciones a agregar, hay que dividir cual hace cada uno

## 1. Detección de Anomalías (Prefix Hijacking)
* **Tarea:** Buscar en el diccionario (`estructuras["por_prefijo"]`) si hay prefijos que tengan más de un AS de origen (el origen es el último número del AS Path). Si hay, imprimir el prefijo y los caminos que muestran el problema.
* **Dónde:** `anomalias()` en `aplicacion.py`.

## 2. Buscar info de un AS
* **Tarea** Pedir un número de AS por consola. Buscarlo en `estructuras["por_numero_as"]` y mostrar en formato de tabla (bien acomodado) todas las IP de sus aristas, qué prefijos se conocen por ahí y el AS Path de cada uno.
* **Dónde:**  `buscar_as()` en `aplicacion.py`.

## 3. Buscar rutas entre dos Prefijos
* **Tarea** Pedir dos prefijos al usuario (ej. prefijo A y prefijo B). Averiguar quiénes son los AS de origen de esos prefijos. Luego, hacer una búsqueda en el `grafo` para encontrar **todas** las rutas que conecten los orígenes de A con los orígenes de B. Verificar que no sucedan ciclos infinitos
* **Dónde:** `buscar_rutas()` en `aplicacion.py`.
