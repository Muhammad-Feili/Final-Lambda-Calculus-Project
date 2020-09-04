import ply.lex as lex
import ply.yacc as yacc
import sys

tokens = [
    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MUL',
    'ASI',
    'POW',
    'GEQU','LEQU',
    'EQU','NOTEQU',
    'GRE','LES',
    'IF','THEN','END',
    'FOR','TO','DO'
    
]

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MUL = r'\*'
t_DIVIDE = r'\/'
t_GEQU = r'\>\='
t_LEQU = r'\<\='
t_EQU = r'\=\='
t_NOTEQU = r'\<\>'
t_GRE = r'\>'
t_LES = r'\<'
t_ASI = r'\='
t_POW=r'\^'
t_ignore= r' '


reserved = {
    'if' : 'IF',
    'then': 'THEN',
    'end':'END',
    'for':'FOR',
    'do':'DO',
    'to':'TO'
}

def t_IF(t):
    r'if'
    return t

def t_THEN(t):
    r'then'
    return t

def t_END(t):
    r'end'
    return t
def t_FOR(t):
    r'for'
    return t
def t_DO(t):
    r'do'
    return t
def t_TO(t):
    r'to'
    return t

def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_FLOAT(t):
    r'\d+.\d+'
    t.value = float(t.value)
    return t


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = 'NAME'
    return t

def t_error(t):
    print('Illegal char!')
    t.lexer.skip(1)



lexer = lex.lex()

precedence = (
    ('left','GEQU','LEQU','EQU','NOTEQU','GRE','LES'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIVIDE'),
    ('left', 'POW')
)


def p_loop(p):
    '''
    statement : FOR NAME ASI calc TO calc DO calc END
    '''
    
    for i in range(p[4],p[6],1):
        print(p[8])

def p_statement(p):
    '''
    statement : IF calc THEN statement END
          
    '''
    if run(p[2]) is False:
        print('SYNTAX ERRORRRRRRR!')

    elif run(p[2])>0: 
        pass
        

def p_statement_calc(p):
    '''
    statement : calc
              
    '''
    print(run(p[1]))
    

def p_calc(p):
    '''
    calc : expression
         | var_assign
    '''
    p[0] = run(p[1])
   
    

def p_var_assign(p):
    '''
    var_assign : NAME ASI expression
    '''
    p[0] = ('=',p[1],p[3])

def p_expression(p):
    '''
    expression : expression POW expression
               | expression MUL expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
               | expression GEQU expression
               | expression LEQU expression
               | expression EQU expression
               | expression NOTEQU expression
               | expression GRE expression
               | expression LES expression
    '''
    p[0] = (p[2], p[1],p[3])


def p_expression_int_float(p):
    '''
    expression : INT
               | FLOAT
    '''
    p[0]=p[1]

def p_expression_var(p):
    '''
    expression : NAME
    '''
    p[0] = ('var',p[1])

def p_error(p):
    print('SYNTAX ERROR')



parser = yacc.yacc()
env = {}
def run(p):
    global env
    if type(p)==tuple:
        
        if p[0]== '+':
            return run(p[1]) + run(p[2])
        elif p[0]== '-':
            return run(p[1]) - run(p[2])
        elif p[0]== '*':
            return run(p[1]) * run(p[2])
        elif p[0]== '^':
            return run(p[1]) ** run(p[2])
        elif p[0]== '/':
            return run(p[1]) / run(p[2])
        elif p[0]== '>=':
            return run(p[1]) >= run(p[2])
        elif p[0]== '<=':
            return run(p[1]) <= run(p[2])
        elif p[0]== '==':
            return run(p[1]) == run(p[2])
        elif p[0]== '<>':
            return run(p[1]) != run(p[2])
        elif p[0]== '<':
            return run(p[1]) < run(p[2])
        elif p[0]== '>':
            return run(p[1]) > run(p[2])
        elif p[0]== '=':
            env[p[1]] = run(p[2])
        elif p[0]== 'var':
            if p[1] not in env:
                raise ValueError('Undeclared variable found!')
            return env[p[1]]
    else:
        return p

"""while True :
    try:
        s = input('>> ')
    except EOFError:
        break
    try:
        parser.parse(s)
    except ValueError as e:
        print(e)"""

s= """ a=1 for i = 1 to 10 do  a=a+1 a end if a==11 then  for j=1 to 5 do  a=a-1 a end end """

parser.parse(s)







