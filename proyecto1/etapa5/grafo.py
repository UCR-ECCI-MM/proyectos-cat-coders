'''
GRAFO

Los nodos son los AS y hay una arista entre dos AS cuando aparecen seguidos
en algun AS Path. Se guarda como un hashmap AS -> conjunto de AS vecinos.
Es no dirigido: si A y B aparecen seguidos, B queda en los vecinos de A y A en
los de B. Se usa en la funcionalidad 3, rutas entre dos prefijos.
'''

from collections import deque


def crear_grafo():
    return {}


def como_conjunto(elemento):
    # Un elemento del AS Path es un AS (int) o un conjunto de AS (frozenset)
    if isinstance(elemento, frozenset):
        return elemento
    return {elemento}


def conectar(grafo, a, b):
    if a not in grafo:
        grafo[a] = set()
    grafo[a].add(b)


def agregar_ruta(grafo, registro):
    as_path = registro['as_path']

    # Cada par de elementos seguidos del path es una conexion
    for i in range(len(as_path) - 1):
        for a in como_conjunto(as_path[i]):
            for b in como_conjunto(as_path[i + 1]):
                # Si el AS se repite no se conecta consigo mismo
                if a != b:
                    conectar(grafo, a, b)
                    conectar(grafo, b, a)


def es_alcanzable(grafo, origen, destino):
    """Verifica rápidamente mediante BFS si existe conectividad entre origen y destino."""
    if origen == destino:
        return True
    if origen not in grafo or destino not in grafo:
        return False

    visitados = {origen}
    cola = deque([origen])
    while cola:
        actual = cola.popleft()
        for vecino in grafo.get(actual, ()):
            if vecino == destino:
                return True
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino)
    return False


def buscar_caminos(grafo, origen, destino, limite=200, max_saltos=5):
    # Busca las rutas sin ciclos entre origen y destino: primero las de 1 salto, despues las de 2, y asi hasta max_saltos
    # Las cortas salen primero porque son las mas realistas, y la busqueda no se pierde en caminos largos
    # Con limite=float("inf") y max_saltos=len(grafo) no hay tope y busca todas las rutas
    # Devuelve las rutas y si se llego al limite
    if origen == destino:
        return [[origen]], False

    if not es_alcanzable(grafo, origen, destino):
        return [], False

    rutas = []
    try:
        for saltos in range(1, max_saltos + 1):
            buscar_con_saltos(grafo, [origen], destino, saltos, rutas, limite)
            if len(rutas) >= limite:
                return rutas, True
    except KeyboardInterrupt:
        # Ctrl+C detiene la busqueda y se devuelven las rutas encontradas hasta ese momento
        print("\nBúsqueda detenida con Ctrl+C.")
        return rutas, True
    return rutas, False


def buscar_con_saltos(grafo, camino, destino, saltos, rutas, limite):
    # DFS que solo guarda las rutas que llegan al destino con exactamente esa cantidad de saltos
    nodo = camino[-1]
    if len(camino) == saltos:
        # Ultimo salto: basta con preguntar si el destino es vecino
        if destino in grafo.get(nodo, ()) and len(rutas) < limite:
            rutas.append(camino + [destino])
        return

    for vecino in grafo.get(nodo, ()):
        if len(rutas) >= limite:
            return
        # Sin ciclos: no se repite un AS del camino ni se pasa por el destino antes de tiempo
        if vecino != destino and vecino not in camino:
            buscar_con_saltos(grafo, camino + [vecino], destino, saltos, rutas, limite)