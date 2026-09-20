'''
ESTRUCTURAS

Se implementan dos hashmaps:

1. por_prefijo:
   Permite buscar los registros utilizando el prefijo de destino, usado 
   principalmente para la funcionalidad 1 ya que identifica si varios sistemas 
   autónomos reportan un prefijo como propio.

2. por_numero_as:
   Permite buscar información utilizando el número de AS, cumple con
   la funcionalidad 2, donde se deben obtener las IP de los peers 
   y los prefijos conocidos por cada uno.

Se mantiene un contador para asignar un identificador único
a cada registro, este identificador se usa posteriormente en el grafo.
'''

def crear_estructuras():
    return { "por_prefijo": {}, "por_numero_as": {}, "siguiente_id": 0 }


def agregar_registro(estructuras, registro):
    registro_id = estructuras["siguiente_id"]
    estructuras["siguiente_id"] += 1

    prefijo = registro['destination_prefix']
    peer_as = registro["peer_as"]
    peer_ip = registro["peer_ip"]
    as_path = registro["as_path"]
    origen = as_path[-1] # El último elemento del AS Path es el AS de origen

    # Se hace el hashmap por prefijo
    if prefijo not in estructuras["por_prefijo"]:
        estructuras["por_prefijo"][prefijo] = {"origenes": set(),"rutas": []}

    estructuras["por_prefijo"][prefijo]["origenes"].add(origen)
    estructuras["por_prefijo"][prefijo]["rutas"].append(as_path)

    # Se hace el hashmap por numero de AS
    if peer_as not in estructuras["por_numero_as"]:
        estructuras["por_numero_as"][peer_as] = {}

    # Verifica si la IP del peer todavía no está asociada con el AS
    if peer_ip not in estructuras["por_numero_as"][peer_as]:
        estructuras["por_numero_as"][peer_as][peer_ip] = []

    # Guarda el prefijo y el AS Path asociados con el peer
    estructuras["por_numero_as"][peer_as][peer_ip].append({"prefijo": prefijo,"as_path": as_path})

    return registro_id
