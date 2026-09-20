import ply.yacc as yacc
from calclex import tokens, lexer
from estructuras import crear_estructuras, agregar_registro
from grafo import crear_grafo, agregar_ruta

# Responsable: Sebas.

error_sintactico = False

def p_archivo(p):
    '''
    archivo : archivo registro
            | registro
    '''
    # El registro  es el último elemento de p.
    registro = p[len(p) - 1]

    # Si hay algun fallo descartamos el registro
    if registro is None or error_sintactico or p.parser.error_semantico or lexer.error_lexico:
        return
    if p.parser.estructuras is not None and p.parser.grafo is not None:

        # Si se lee correctamente el registro se guarda  y devuelve su id
        # y se usa ese mismo id para hacer las conexiones del grafo
        registro_id = agregar_registro(p.parser.estructuras, registro)
        agregar_ruta(p.parser.grafo, registro, registro_id)

def p_registro(p):
    '''
    registro : RECORD_TYPE PIPE NUMBER10 PIPE STATE PIPE PEER_IP PIPE numero_as PIPE DESTINATION_PREFIX PIPE as_path NEWLINE
    '''
    # Posiciones en p:
        # RECORD_TYPE = 1
        # NUMBER10 = 3
        # STATE = 5
        # PEER_IP = 7
        # numero_as = 9
        # DESTINATION_PREFIX = 11
        # as_path = 13
        # PIPE = 2, 4, 6, 8, 10, 12
        # NEWLINE = 14
    peer_as = p[9]
    as_path = p[13]

    # Se revisa que el primer elemento del AS Path es un AS individual y no un conjunto
    # ademas que el primer AS sea igual al Peer AS
    if not isinstance(as_path[0], int) or peer_as != as_path[0]:
        p.parser.error_semantico = True
        print(f"Error semántico en línea {p.lineno(1)}: el Peer AS {peer_as} "
              "debe coincidir con el primer AS individual del AS Path.")
        p[0] = None
        return

    # Se guarda el registro en un diccionario
    p[0] = {
        'record_type': p[1],
        'timestamp': p[3],
        'state': p[5],
        'peer_ip': p[7],
        'peer_as': peer_as,
        'destination_prefix': p[11],
        'as_path': as_path,
    }

def p_as_path(p):
    '''
    as_path : as_path elemento_as
            | elemento_as
    '''
    # Si la longitud es 2 quiere decir solo hay un elemento_as, por lo que lo asignamos
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        # p[1] es la ruta construida entonces usamos append para seguir el orden 
        # y las repeticiones sin copiar toda la lista.
        p[1].append(p[2])
        p[0] = p[1]

def p_elemento_as(p):
    '''
    elemento_as : numero_as
                | LBRACE lista_as RBRACE
    '''
    # Si solo es un numero_as lo guardamos pero en caso de que sea un conjunto
    # lo guardamos en un set que no puede modificarse
    p[0] = p[1] if len(p) == 2 else frozenset(p[2])

def p_lista_as(p):
    '''
    lista_as : lista_as COMMA numero_as
             | numero_as
    '''
    # Si el conjunto es solo 1 numero_as lo guardamos entre llaves.
    if len(p) == 2:
        p[0] = {p[1]}
    else:
        # En caso de ser mas numeros los guardamos como un conjunto que elimina duplicados
        # y no mantienen un orden.
        p[1].add(p[3])
        p[0] = p[1]

def p_numero_as(p):
    '''
    numero_as : NUMBER1TO9
              | NUMBER10
    '''
    # Se guarda directamente ya que el lexer ya lo casteo  a int
    p[0] = p[1]


def p_error(p):
    # Sin token (p es None), el archivo terminó antes de completar la regla.
    global error_sintactico
    error_sintactico = True

    if p:
        print(f"Error sintáctico en token '{p.value}' ({p.type}) en línea {p.lineno}.")
    else:
        print("Error sintáctico: fin de archivo inesperado.")

# Se construye el parser con las reglas
parser = yacc.yacc(write_tables=False, debug=False)


def analizar_archivo(archivo):
    """Devuelve {'estructuras': ..., 'grafo': ...}, o None si falla.

    Los registros son diccionarios de siete campos; as_path contiene enteros
    y frozenset para los grupos entre llaves, conservando el orden de la ruta.
    """
    global error_sintactico
    error_sintactico = False
    parser.error_semantico = False
    parser.estructuras = None
    parser.grafo = None
    lexer.lineno = 1
    lexer.error_lexico = False

    # Si no se puede abrir o leer el archivo, se informa y se devuelve None.
    try:
        with open(archivo, 'r') as archivo_entrada:
            data = archivo_entrada.read()
    except (OSError, UnicodeError) as error:
        print(f"Error: No se pudo leer el archivo '{archivo}': {error}")
        return None

    # Como la gramática ocupa NEWLINE al final de cada registro en caso de que no este lo agregamos
    if not data.endswith('\n'):
        data += '\n'

    # Preparamos los contenedores que se van a ir llenando
    parser.estructuras = crear_estructuras()
    parser.grafo = crear_grafo()
    parser.parse(data, lexer=lexer)

    # Se descartan los resultados si hubo errores
    if error_sintactico or lexer.error_lexico or parser.error_semantico:
        parser.estructuras = None
        parser.grafo = None
        return None

    # Verificar que los otros modulos esten implementados o no devuelven los contenedores
    if parser.estructuras is None or parser.grafo is None:
        print("Error: falta implementar crear_estructuras o crear_grafo para completar la etapa 4.")
        return None

    # En caso de que todo este correcto se devuelven ambas partes para que el main pueda acceder a ellas
    return {
        'estructuras': parser.estructuras, 
        'grafo': parser.grafo
        }
