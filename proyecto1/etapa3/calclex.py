import ply.lex as lex
import sys
import os

# CONSTANTES
'''
Según el estándar de la IETF, para el formato MRT el TIMESTAMP es un campo de
4 octetos que representa la la cantidad de segundos transcurridos desde el
1 de enero de 1970 a las 00:00:00 UTC.
El ultimo valor representable es 0x7FFFFFFF, que en decimal 2147483647
'''
MAX_TIMESTAMP = 2147483647 # ya no se usa

'''
El AS tiene 4 octetos(32 bits) que se puede representar como un numero
entero maximo que es 2^32 = 4294967296, pero como se comienza desde 0 el maximo
pasa a ser 2^32 - 1 = 4294967295
'''
AS_VALOR_MAXIMO = 4294967295 # mismo caso que MAX_TIMESTAMP, la revision de rango del AS pasa al parser


# List of token names.   This is always required
tokens = (
    'RECORD_TYPE',
    'NUMBER10',
    'STATE',
    'PEER_IP',
    'NUMBER1TO9',
    'NEWLINE',
    'DESTINATION_PREFIX',
    'PIPE',
    'LBRACE',
    'RBRACE',
    'COMMA',

)

# Regular expression rules for simple tokens
t_PIPE = r'\|'

# Las llaves y la coma pasan a ser tokens propios
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r','

# Regular expression rules with some action code
def t_DESTINATION_PREFIX(t):
    r'([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])/([3][0-1]|[2][0-9]|[1][0-9]|[1-9]|[0])(?![0-9])'
    return t

def t_PEER_IP(t):
    r'([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])(?![0-9])'
    return t

def t_RECORD_TYPE(t):
    r'TABLE_DUMP2'
    return t

def t_LONGNUMBER(t):
    r'(?<!\d)\d{11,}(?!\d)'
    print(f"Error léxico en línea {t.lineno}: '{t.value}' tiene {len(t.value)} digitos, el maximo del formato es 10")

def t_NUMBER10(t):
    r'(?<!\d)\d{10}(?!\d)'
    t.value = int(t.value)
    return t

def t_STATE(t):
    r'[BAW]'
    return t

# AS_PATH y PEER_AS se van y los reemplaza NUMBER1TO9
def t_NUMBER1TO9(t):
    r'(?<!\d)\d{1,9}(?!\d)'
    t.value = int(t.value)
    return t


# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

 # Define a rule so we can track line numbers
def t_NEWLINE(t):
     r'\n+'
     t.lexer.lineno += len(t.value)
     return t

# Error handling rule
def t_error(t):
     print(f"Caracter ilegal '{t.value[0]}' en línea {t.lineno}")
     t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso correcto: python calclex.py <archivo.txt>")
        sys.exit(1)

    archivo = sys.argv[1]
    os.makedirs("output", exist_ok=True)

    nombre_archivo = os.path.basename(archivo)
    nombre_salida = os.path.join("output", f"salida_{nombre_archivo}")
    print(f"\nProcesando '{archivo}', se guarda en: '{nombre_salida}'")

    try:
        with open(archivo, 'r') as archivo_entrada, open(nombre_salida, 'w') as archivo_salida:
            data = archivo_entrada.read()
            lexer.input(data)
            contador = 0
            # Tokenize
            while True:
                tok = lexer.token()
                if not tok: break
                contador += 1
                archivo_salida.write(f"{tok}\n")
                #imprimimos 5 para evitar saturar la salida de la terminal
                if contador <= 5: print(tok)

        print(f"Se guardaron {contador} tokens válidos.")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{archivo}'.")