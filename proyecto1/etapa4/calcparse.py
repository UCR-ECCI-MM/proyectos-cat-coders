import sys
import ply.yacc as yacc
from calclex import tokens, lexer

# TODO: Crear diccionarios para buscar rutas por AS y por prefijo.
# TODO: Crear un grafo con las conexiones entre AS de cada ruta.

error_sintactico = False

def p_archivo(p):
    '''
    archivo : archivo registro
            | registro
    '''
    # TODO: Guardar cada registro en los diccionarios y actualizar el grafo.
    pass

def p_registro(p):
    '''
    registro : RECORD_TYPE PIPE NUMBER10 PIPE STATE PIPE PEER_IP PIPE numero_as PIPE DESTINATION_PREFIX PIPE as_path NEWLINE
    '''
    # TODO: Guardar los siete campos leídos en un objeto o diccionario.
    # TODO: Validar que el Peer AS coincida con el primer AS del AS Path.
    pass

def p_as_path(p):
    '''
    as_path : as_path elemento_as
            | elemento_as
    '''
    # TODO: Construir la lista ordenada de AS de la ruta.
    pass

def p_elemento_as(p):
    '''
    elemento_as : numero_as
                | LBRACE lista_as RBRACE
    '''
        # TODO: Devolver un AS individual o un conjunto si viene entre llaves.

    pass

def p_lista_as(p):
    '''
    lista_as : lista_as COMMA numero_as
             | numero_as
    '''
    # TODO: Reunir los AS que están dentro de las llaves.
    pass

def p_numero_as(p):
    '''
    numero_as : NUMBER1TO9
              | NUMBER10
    '''
    pass


def p_error(p):
    global error_sintactico
    error_sintactico = True

    if p:
        print(f"Error sintáctico en token '{p.value}' ({p.type}) en línea {p.lineno}.")
    else:
        print("Error sintáctico: fin de archivo inesperado.")


parser = yacc.yacc()


def analizar_archivo(archivo):
    try:
        with open(archivo, 'r') as archivo_entrada:
            data = archivo_entrada.read()

        if not data.endswith('\n'):
            data += '\n'

        lexer.lineno = 1
        lexer.error_lexico = False
        parser.parse(data, lexer=lexer)

        if not error_sintactico and not lexer.error_lexico:
            print("Archivo sintácticamente correcto.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'.")
        sys.exit(1)
