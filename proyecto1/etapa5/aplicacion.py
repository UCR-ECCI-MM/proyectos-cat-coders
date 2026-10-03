# aplicacion.py
# Aquí va el código de cada uno para el menú principal.

from grafo import buscar_caminos
from visualizador import imprimir_diagrama_consola, generar_html_rutas, generar_html_tabla_as


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
    print(f"{BOLD}{CYAN}           2. BUSQUEDA DE INFORMACION DE UN AS{RESET}")
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

    # Opción sencilla para exportar la tabla a HTML
    try:
        opc_html = input("¿Desea exportar esta tabla a un archivo HTML? [s/N]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        opc_html = 'n'

    if opc_html == 's':
        generar_html_tabla_as(as_buscado, filas)
        print("Archivo HTML generado con éxito: reporte_as.html\n")

def extraer_ases_origen(origenes_raw):
    """Extrae todos los identificadores numéricos de AS de los orígenes (soporta enteros y conjuntos)."""
    ases = set()
    for elem in origenes_raw:
        if isinstance(elem, (set, frozenset)):
            ases.update(elem)
        elif isinstance(elem, int):
            ases.add(elem)
    return sorted(ases)


def buscar_rutas(grafo, estructuras):
    print(f"\n{BOLD}{CYAN}{'=' * 65}{RESET}")
    print(f"{BOLD}{CYAN}           3. BUSQUEDA DE RUTAS ENTRE DOS PREFIJOS{RESET}")
    print(f"{BOLD}{CYAN}{'=' * 65}{RESET}")
    
    por_prefijo = estructuras.get("por_prefijo", {})
    if not por_prefijo:
        print(f"{YELLOW}Aviso: No hay registros de prefijos cargados en memoria.{RESET}\n")
        return

    # 1. Pedir prefijo A y validar entrada
    try:
        entrada_a = input(f"{BOLD}Ingrese el Prefijo A{RESET} (o 'c' para cancelar): ").strip()
    except (EOFError, KeyboardInterrupt):
        print(f"\n{YELLOW}Búsqueda cancelada.{RESET}\n")
        return
    if entrada_a.lower() == 'c':
        print(f"{YELLOW}Búsqueda cancelada.{RESET}\n")
        return

    if entrada_a not in por_prefijo:
        print(f"\n{RED}Error: El prefijo A '{entrada_a}' no fue encontrado en los registros analizados.{RESET}\n")
        return

    # 2. Pedir prefijo B y validar entrada
    try:
        entrada_b = input(f"{BOLD}Ingrese el Prefijo B{RESET} (o 'c' para cancelar): ").strip()
    except (EOFError, KeyboardInterrupt):
        print(f"\n{YELLOW}Búsqueda cancelada.{RESET}\n")
        return
    if entrada_b.lower() == 'c':
        print(f"{YELLOW}Búsqueda cancelada.{RESET}\n")
        return

    if entrada_b not in por_prefijo:
        print(f"\n{RED}Error: El prefijo B '{entrada_b}' no fue encontrado en los registros analizados.{RESET}\n")
        return

    # 3. Averiguar quiénes son los AS de origen de esos prefijos
    origenes_a = extraer_ases_origen(por_prefijo[entrada_a].get("origenes", set()))
    origenes_b = extraer_ases_origen(por_prefijo[entrada_b].get("origenes", set()))

    if not origenes_a:
        print(f"\n{RED}Error: No se encontraron AS de origen para el Prefijo A ({entrada_a}).{RESET}\n")
        return

    if not origenes_b:
        print(f"\n{RED}Error: No se encontraron AS de origen para el Prefijo B ({entrada_b}).{RESET}\n")
        return

    str_orig_a = ", ".join(str(x) for x in origenes_a)
    str_orig_b = ", ".join(str(x) for x in origenes_b)
    print(f"\n{CYAN}[i] Prefijo A ({BOLD}{entrada_a}{RESET}{CYAN}) -> AS de origen: {GREEN}{str_orig_a}{RESET}")
    print(f"{CYAN}[i] Prefijo B ({BOLD}{entrada_b}{RESET}{CYAN}) -> AS de origen: {GREEN}{str_orig_b}{RESET}")

    if entrada_a == entrada_b:
        print(f"{DIM}(Nota: Se ingresó el mismo prefijo para A y B).{RESET}")

    print(f"\n{YELLOW}Buscando rutas en el grafo... por favor espere.{RESET}")

    # 4. Buscar todas las rutas posibles en el grafo entre los orígenes de A y B
    filas = []
    limite_global = False
    rutas_vistas = set()

    for o_a in origenes_a:
        for o_b in origenes_b:
            caminos, lim = buscar_caminos(grafo, o_a, o_b)
            if lim:
                limite_global = True
            for c in caminos:
                clave_ruta = tuple(c)
                if clave_ruta not in rutas_vistas:
                    rutas_vistas.add(clave_ruta)
                    filas.append({
                        "origen_a": o_a,
                        "origen_b": o_b,
                        "saltos": len(c) - 1,
                        "path": formatear_as_path(c),
                        "raw_ruta": c
                    })

    total_rutas = len(filas)
    if total_rutas == 0:
        print(f"\n{RED}[!] No se encontraron rutas que conecten los orígenes de ambos prefijos en el grafo.{RESET}\n")
        return

    print(f"\n{GREEN}[+] Se encontraron {total_rutas} ruta(s) disponible(s) entre {BOLD}{entrada_a}{RESET}{GREEN} y {BOLD}{entrada_b}{RESET}{GREEN}:{RESET}")
    if limite_global:
        print(f"{YELLOW}Aviso: Se alcanzó el límite de rutas por par de orígenes para prevenir desbordamiento.{RESET}")

    # Diagrama de flujo visual en consola
    imprimir_diagrama_consola(origenes_a, origenes_b, [f["raw_ruta"] for f in filas])

    # 5. Formato tabular organizado y dinámico
    ancho_num = 6
    ancho_orig_a = 12
    ancho_orig_b = 12
    ancho_saltos = 8
    ancho_max_path = max(len(f["path"]) for f in filas) if filas else 40
    ancho_path = max(ancho_max_path + 4, 40)

    separador = f"{BLUE}+{'-' * ancho_num}+{'-' * ancho_orig_a}+{'-' * ancho_orig_b}+{'-' * ancho_saltos}+{'-' * ancho_path}+{RESET}"

    col_h_num = "#".ljust(ancho_num - 2)
    col_h_orig_a = "Origen A".ljust(ancho_orig_a - 2)
    col_h_orig_b = "Origen B".ljust(ancho_orig_b - 2)
    col_h_saltos = "Saltos".ljust(ancho_saltos - 2)
    col_h_path = "Ruta (AS Path)".ljust(ancho_path - 2)

    encabezado = (
        f"{BLUE}|{RESET} {BOLD}{WHITE}{col_h_num}{RESET} "
        f"{BLUE}|{RESET} {BOLD}{WHITE}{col_h_orig_a}{RESET} "
        f"{BLUE}|{RESET} {BOLD}{WHITE}{col_h_orig_b}{RESET} "
        f"{BLUE}|{RESET} {BOLD}{WHITE}{col_h_saltos}{RESET} "
        f"{BLUE}|{RESET} {BOLD}{WHITE}{col_h_path}{RESET} {BLUE}|{RESET}"
    )

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

        col_num = f"{WHITE}{str(i + 1).ljust(ancho_num - 2)}{RESET}"
        col_oa = f"{CYAN}{str(fila['origen_a']).ljust(ancho_orig_a - 2)}{RESET}"
        col_ob = f"{GREEN}{str(fila['origen_b']).ljust(ancho_orig_b - 2)}{RESET}"
        col_saltos = f"{YELLOW}{str(fila['saltos']).ljust(ancho_saltos - 2)}{RESET}"
        col_p = f"{MAGENTA}{path_str.ljust(ancho_path - 2)}{RESET}"

        print(f"{BLUE}|{RESET} {col_num} {BLUE}|{RESET} {col_oa} {BLUE}|{RESET} {col_ob} {BLUE}|{RESET} {col_saltos} {BLUE}|{RESET} {col_p} {BLUE}|{RESET}")

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

    # Opción sencilla para generar archivo HTML
    try:
        opc_html = input("¿Desea generar un archivo HTML con el grafo de rutas? [s/N]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        opc_html = 'n'

    if opc_html == 's':
        rutas_crudas = [f["raw_ruta"] for f in filas]
        generar_html_rutas(entrada_a, origenes_a, entrada_b, origenes_b, rutas_crudas)
        print("Archivo HTML generado con éxito: visualizador_rutas.html\n")
