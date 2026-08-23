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
    'AS_PATH',
)
 
# Regular expression rules for simple tokens
def t_RECORD_TYPE(t):
    r'TABLE_DUMP2'
    return t

#TODO
#def t_timestamp_TIMESTAMP(t):

def t_STATE(t):
    r'[BAW]'
    return t

#TODO
#def t_PEER_IP(t):

#TODO
#def t_PEER_AS(t):


#TODO
#def t_DESTINATION_PREFIX(t):

#TODO
#def t_AS_PATH(t):












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
