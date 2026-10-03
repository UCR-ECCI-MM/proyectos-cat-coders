# aplicacion.py
# Aquí va el código de cada uno para el menú principal.

def anomalias(estructuras):
    print("\n--- 1. Analizando Anomalías ---")
    
    # TODO: Integrante 1
    # 1. Recorrer estructuras["por_prefijo"]
    # 2. Revisar si len(origenes) > 1 para algún prefijo.
    # 3. Si pasa, imprimir el prefijo y los AS Path que tienen orígenes distintos.
    
    print("Falta programar esta parte...\n")


# Códigos de escape ANSI para darle estilo y color a la terminal
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
RED = "\033[31m"
WHITE = "\033[37m"


def formatear_as_path(as_path):
    """Convierte la lista de AS Path (con enteros y frozenset) a texto legible con flechas."""
    elementos = []
    for elem in as_path:
        if isinstance(elem, (set, frozenset)):
            # Formato {AS1, AS2, ...}
            elementos.append("{" + ", ".join(str(x) for x in sorted(elem)) + "}")
        else:
            elementos.append(str(elem))
    return " -> ".join(elementos)


def buscar_as(estructuras):
    print(f"\n{BOLD}{CYAN}{'=' * 65}{RESET}")
    print(f"{BOLD}{CYAN}           2. BÚSQUEDA DE INFORMACIÓN DE UN AS{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 65}{RESET}")
    
    por_as = estructuras.get("por_numero_as", {})
    if not por_as:
        print(f"{YELLOW}Aviso: No hay registros de AS cargados en memoria.{RESET}\n")
        return

    # 1. Pedir el número de AS y validar entrada
    entrada = input(f"{BOLD}Ingrese el número de AS a consultar{RESET} (o 'c' para cancelar): ").strip()
    if entrada.lower() == 'c':
        print(f"{YELLOW}Búsqueda cancelada.{RESET}\n")
        return

    try:
        as_buscado = int(entrada)
    except ValueError:
        print(f"{RED}Error: '{entrada}' no es un número de AS válido.{RESET}\n")
        return

    # 2. Revisar si existe en estructuras["por_numero_as"]
    if as_buscado not in por_as:
        print(f"\n{RED}El AS {as_buscado} no fue encontrado en los registros de peers analizados.{RESET}")
        print(f"{DIM}(Recuerde que este índice contiene los AS de los Peers recolectores).{RESET}\n")
        return

    # 3. Recopilar todas las filas asociadas
    datos_peer = por_as[as_buscado]
    filas = []
    for peer_ip, anuncios in datos_peer.items():
        for item in anuncios:
            filas.append({
                "ip": peer_ip,
                "prefijo": item["prefijo"],
                "path": formatear_as_path(item["as_path"])
            })

    total_rutas = len(filas)
    print(f"\n{GREEN}[+] Se encontraron {total_rutas} ruta(s) para el AS {BOLD}{as_buscado}{RESET}{GREEN}:{RESET}")
    
    # 4. Calcular anchos dinámicos para que nunca corte texto de las rutas
    ancho_ip = 18
    ancho_prefijo = 20
    ancho_max_path = max(len(f["path"]) for f in filas) if filas else 45
    # Damos ancho suficiente para mostrar la ruta completa sin cortarla
    ancho_path = max(ancho_max_path + 4, 45)

    separador = f"{BLUE}+{'-' * ancho_ip}+{'-' * ancho_prefijo}+{'-' * ancho_path}+{RESET}"
    
    col_h_ip = "IP Peer".ljust(ancho_ip - 2)
    col_h_pref = "Prefijo Destino".ljust(ancho_prefijo - 2)
    col_h_path = "AS Path".ljust(ancho_path - 2)
    encabezado = f"{BLUE}|{RESET} {BOLD}{WHITE}{col_h_ip}{RESET} {BLUE}|{RESET} {BOLD}{WHITE}{col_h_pref}{RESET} {BLUE}|{RESET} {BOLD}{WHITE}{col_h_path}{RESET} {BLUE}|{RESET}"

    print(separador)
    print(encabezado)
    print(separador)

    # Mostrar con paginación de 15 en 15 si son muchas
    TAM_PAGINA = 15
    for i, fila in enumerate(filas):
        path_str = fila['path']
        max_path = ancho_path - 2
        if len(path_str) > max_path:
            path_str = path_str[:max_path - 3] + "..."

        col_ip = f"{CYAN}{fila['ip'].ljust(ancho_ip - 2)}{RESET}"
        col_prefijo = f"{GREEN}{fila['prefijo'].ljust(ancho_prefijo - 2)}{RESET}"
        col_path = f"{MAGENTA}{path_str.ljust(ancho_path - 2)}{RESET}"

        print(f"{BLUE}|{RESET} {col_ip} {BLUE}|{RESET} {col_prefijo} {BLUE}|{RESET} {col_path} {BLUE}|{RESET}")

        # Paginador
        if (i + 1) % TAM_PAGINA == 0 and (i + 1) < total_rutas:
            print(separador)
            opc = input(f"{BOLD}{YELLOW}Mostrando {i + 1} de {total_rutas}. ¿Ver siguientes? [S/n]: {RESET}").strip().lower()
            if opc == 'n':
                break
            print(separador)
            print(encabezado)
            print(separador)

    print(separador + "\n")


def buscar_rutas(grafo, estructuras):
    print("\n--- 3. Buscar rutas entre Prefijos ---")
    
    # TODO: Integrante 3
    # 1. Pedir prefijo A y prefijo B usando input()
    # 2. Buscar en estructuras["por_prefijo"] los orígenes de A y B
    # 3. Usar el grafo para buscar TODAS las rutas posibles entre esos orígenes.
    
    print("Falta programar esta parte...\n")
