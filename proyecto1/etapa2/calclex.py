# ------------------------------------------------------------
 # calclex.py
 #
 # tokenizer for a simple expression evaluator for
 # numbers and +,-,*,/
 # ------------------------------------------------------------
import ply.lex as lex
import sys


# CONSTANTES
''' 
El TIMESTAMP se maneja como un número entero CON SIGNO de 32 bits. 
Al reservar 1 bit para el signo (+/-), nos quedan 31 bits para el valor, por eso
su máximo es 2^31 - 1 = 2147483647
'''
MAX_TIMESTAMP = 2147483647
''' 
El AS tiene 4 octetos(32 bits) que se puede representar como un numero 
entero maximo que es 2^32 = 4294967296, pero como se comienza desde 0 el maximo 
pasa a ser 2^32 - 1 = 4294967295
'''
AS_VALOR_MAXIMO = 4294967295 


# List of token names.   This is always required
tokens = (
    'RECORD_TYPE',
    'TIMESTAMP',
    'STATE',
    'PEER_IP',
    'PEER_AS',
    'DESTINATION_PREFIX',
    'AS_PATH',
    'PIPE',
    
)

# Regular expression rules for simple tokens
t_PIPE = r'\|'

# Regular expression rules with some action code
def t_RECORD_TYPE(t):
    r'TABLE_DUMP2'
    return t

def t_TIMESTAMP(t):
    r'\d{10}(?!\d)'
    t.value = int(t.value)
    
    if t.value > MAX_TIMESTAMP:
        print(f"Error léxico: Timestamp fuera de rango: {t.value}")
        return None
    else:
        return t

def t_STATE(t):
    r'[BAW]'
    return t

def t_DESTINATION_PREFIX(t):
    r'([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])/([3][0-1]|[2][0-9]|[1][0-9]|[1-9])(?![0-9])'
    return t

def t_PEER_IP(t):
    r'([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])(?![0-9])'
    return t


def t_PEER_AS(t):
    r'(?<!\d)\d{1,10}(?!\d)'
    if int(t.value) > AS_VALOR_MAXIMO:
        print(f"AS fuera del rango valido: {t.value}")
        return None

    t.value = int(t.value)
    return t


def t_AS_PATH(t):
    r'(?<!\d)\d{1,10}(?:[ \t]+\d{1,10})*[ \t]*(?=\r?\n|$)'

     #TODO
    ''' 
        r'\d{1,10}(?!\d)' agregar a la presentacion porque aqui se iban aceptando los ultimos y no deberia ser asi
        53046 61626 14840 3356 7493232523432
    
        53046 61626 14840 3356 749
        
    '\d{1,10}(?:[ \t]+\d{1,10})*[ \t]*(?=\r?\n|$)'
    '''
    lista_as = t.value.split()

    for asn in lista_as:
        if int(asn) > AS_VALOR_MAXIMO:
            print(f"AS fuera del rango valido: {asn}")
            return None

    return t



# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

 # Define a rule so we can track line numbers
def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)

# Error handling rule
def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso correcto: python calclex.py <archivo.txt>")
        sys.exit(1)
        
    archivo = sys.argv[1]
    nombre_salida = f"salida_{archivo}"
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