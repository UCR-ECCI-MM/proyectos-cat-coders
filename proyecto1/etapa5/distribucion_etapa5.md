# Entregable 5: ¿Qué hace cada uno?

¡Hola gente! Para esta última etapa tenemos que hacer la aplicación que usa los datos que ya logramos extraer. Son 3 opciones en el menú, así que nos toca una a cada uno. 

En `main.py` ya dejé armado el menú interactivo, y en `aplicacion.py` hay una función vacía para cada uno de nosotros. 

## 1. Detección de Anomalías (Prefix Hijacking)
**Encargado:** _____________________
* **¿Qué hay que hacer?** Buscar en el diccionario (`estructuras["por_prefijo"]`) si hay prefijos que tengan más de un AS de origen (el origen es el último número del AS Path). Si hay, imprimir el prefijo y los caminos que muestran el problema.
* **Dónde:** Llenar la función `anomalias()` en `aplicacion.py`.

## 2. Buscar info de un AS
**Encargado:** _____________________
* **¿Qué hay que hacer?** Pedir un número de AS por consola. Buscarlo en `estructuras["por_numero_as"]` y mostrar en formato de tabla (bien acomodado) todas las IP de sus aristas, qué prefijos se conocen por ahí y el AS Path de cada uno.
* **Dónde:** Llenar la función `buscar_as()` en `aplicacion.py`.

## 3. Buscar rutas entre dos Prefijos
**Encargado:** _____________________
* **¿Qué hay que hacer?** Pedir dos prefijos al usuario (ej. prefijo A y prefijo B). Averiguar quiénes son los AS de origen de esos prefijos. Luego, hacer una búsqueda en el `grafo` para encontrar **todas** las rutas que conecten los orígenes de A con los orígenes de B. ¡Ojo con no quedarse pegados en un ciclo infinito!
* **Dónde:** Llenar la función `buscar_rutas()` en `aplicacion.py`.

---
¡Eso es todo! Solo metemos el código en `aplicacion.py` y probamos.
