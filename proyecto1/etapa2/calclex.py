# ------------------------------------------------------------
 # calclex.py
 #
 # tokenizer for a simple expression evaluator for
 # numbers and +,-,*,/
 # ------------------------------------------------------------
import ply.lex as lex
 
# List of token names.   This is always required
tokens = (
    'RECORD_TYPE',
    'TIMESTAMP',
    'STATE',
    'PEER_IP',
    'PEER_AS',
    'DESTINATION_PREFIX',
    'PIPE',
)

# Regular expression rules for simple tokens
t_PIPE = r'\|'

# Regular expression rules with some action code
def t_RECORD_TYPE(t):
    r'TABLE_DUMP2'
    return t

def t_TIMESTAMP(t):
    r'\d{10}'
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

#TODO
#def t_PEER_AS(t):

#TODO
#def t_AS_PATH(t):



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


# Tokenize
while True:
     tok = lexer.token()
     if not tok: 
         break      # No more input
     print(tok)



#CODIGO QUE VENIA CON EL PROGRAMA

# A regular expression rule with some action code
def t_NUMBER(t):
     r'\d+'
     t.value = int(t.value)    
     return t
 
 # Define a rule so we can track line numbers
def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)
 
# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'
 
# Error handling rule
def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)
 
# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
3 + 4 * 10
  + -20 *2
'''
 
# Give the lexer some input
lexer.input(data)
 
# Tokenize
while True:
     tok = lexer.token()
     if not tok: 
         break      # No more input
     print(tok)
