import ply.lex as lex

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
    r'([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])/([3][0-1]|[2][0-9]|[1][0-9]|[1-9]|[0])'
    return t

def t_PEER_IP(t):
    r'([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])\.([2][5][0-5]|[2][0-4][0-9]|[1][0-9][0-9]|[1-9][0-9]|[0-9])'
    return t

def t_RECORD_TYPE(t):
    r'TABLE_DUMP2'
    return t

def t_LONGNUMBER(t):
    r'\d{11,}'
    t.lexer.error_lexico = True
    print(f"Error léxico en línea {t.lineno}: '{t.value}' tiene {len(t.value)} digitos, el maximo del formato es 10")

def t_NUMBER10(t):
    r'\d{10}'
    t.value = int(t.value)
    return t

def t_STATE(t):
    r'[BAW]'
    return t

# AS_PATH y PEER_AS se van y los reemplaza NUMBER1TO9
def t_NUMBER1TO9(t):
    r'\d{1,9}'
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
     t.lexer.error_lexico = True
     print(f"Caracter ilegal '{t.value[0]}' en línea {t.lineno}")
     t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# El parser la revisa para no dar por correcto un archivo que el lexer rechazo
lexer.error_lexico = False