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


def buscar_caminos(grafo, origen, destino, limite=200, max_profundidad=7):
    """
    Encuentra todos los caminos simples (sin ciclos) entre origen y destino
    utilizando búsqueda en profundidad (DFS) con retroceso (backtracking).

    Parámetros:
      - grafo: Diccionario de adyacencia AS -> set(AS vecinos).
      - origen: Número de AS inicial (int).
      - destino: Número de AS final (int).
      - limite: Máximo número de rutas a recolectar para evitar explosión combinatoria.
      - max_profundidad: Cota de saltos AS máximos. En BGP los caminos reales
                        rara vez exceden 5-6 saltos. Evita explorar ramas irrelevantes
                        de decenas de saltos en routers núcleo con miles de conexiones.

    Retorna:
      (rutas, limite_alcanzado): Lista de rutas (listas de ints) y booleano indicando
                                  si se alcanzó el límite de seguridad.
    """
    if origen == destino:
        return [[origen]], False

    if not es_alcanzable(grafo, origen, destino):
        return [], False

    rutas = []
    visitados = {origen}
    camino = [origen]
    limite_alcanzado = False

    def dfs(nodo):
        nonlocal limite_alcanzado
        if len(rutas) >= limite:
            limite_alcanzado = True
            return

        if len(camino) > max_profundidad:
            return

        for vecino in grafo.get(nodo, ()):
            if vecino == destino:
                rutas.append(list(camino) + [destino])
                if len(rutas) >= limite:
                    limite_alcanzado = True
                    return
            elif vecino not in visitados:
                if len(camino) < max_profundidad:
                    visitados.add(vecino)
                    camino.append(vecino)
                    dfs(vecino)
                    camino.pop()
                    visitados.remove(vecino)
                    if limite_alcanzado:
                        return

    dfs(origen)
    return rutas, limite_alcanzado
