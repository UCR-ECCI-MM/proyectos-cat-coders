'''
GRAFO

Los nodos son los AS y hay una arista entre dos AS cuando aparecen seguidos
en algun AS Path. Se guarda como un hashmap AS -> conjunto de AS vecinos.
Es no dirigido: si A y B aparecen seguidos, B queda en los vecinos de A y A en
los de B. Se usa en la funcionalidad 3, rutas entre dos prefijos.
'''


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