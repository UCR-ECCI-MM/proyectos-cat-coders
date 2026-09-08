import sys
import ply.yacc as yacc
from calclex import tokens, lexer

error_sintactico = False

def p_archivo(p):
    '''
    ARCHIVO : ARCHIVO REGISTRO
            | REGISTRO
    '''
    pass

def p_registro(p):
    '''
    REGISTRO : RECORD_TYPE PIPE NUMBER10 PIPE STATE PIPE PEER_IP PIPE NUMERO_AS PIPE DESTINATION_PREFIX PIPE AS_PATH NEWLINE
    '''
    pass

def p_as_path(p):
    '''
    AS_PATH : AS_PATH NUMERO_AS
            | NUMERO_AS
    '''
    pass

def p_numero_as(p):
    '''
    NUMERO_AS : NUMBER1TO9
              | NUMBER10
    '''
    pass

#TODO -> Falta de agregar estas funciones
#LISTA_AS
#ELEMENTO_AS


def p_error(p):
    global error_sintactico
    error_sintactico = True

    if p:
        print(f"Error sintáctico en token '{p.value}' ({p.type}) en línea {p.lineno}.")
    else:
        print("Error sintáctico: fin de archivo inesperado.")


parser = yacc.yacc()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)

    archivo = sys.argv[1]

    try:
        with open(archivo, 'r') as archivo_entrada:
            data = archivo_entrada.read()

        if not data.endswith('\n'):
            data += '\n'

        lexer.lineno = 1
        parser.parse(data, lexer=lexer)

        if not error_sintactico:
            print("Archivo sintácticamente correcto.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'.")
        sys.exit(1)
