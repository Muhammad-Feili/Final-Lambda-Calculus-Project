import fileinput
import ply.lex as lex
import ply.yacc as yacc


tokens = (
    'IF',
    'THEN',
    'FOR',
    'DO',
    'TO',
    'END',
    'SEMICOLON',
    'NUMBER',
    'NAME',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'LESS',
    'GRTR',
    'LEQ',
    'GEQ',
    'NEQ',
    'EQU',
    'EQUALS'
)

t_SEMICOLON = r';'
t_NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
#t_LPAREN = r'\('
#t_RPAREN = r'\)'
t_LESS = r'\<'
t_GRTR = r'\>'
t_LEQ = r'\<\='
t_GEQ = r'\>\='
t_EQU = r'\=\='
t_NEQ = r'\<\>'
t_EQUALS = r'\='
t_ignore = ' \t'

reserved = {
    'if': 'IF',
    'for': 'FOR',
    'do': 'DO',
    'end': 'END',
    'to': 'TO',
    'then': 'THEN'
}

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

names = {}


def t_NUMBER(token):
    r'\d+'
    token.value = int(token.value)
    if token.lexer.paren_count == 0:
        return token


def t_LPAREN(token):
    r'\('
    token.lexer.paren_count += 1
    return token


def t_RPAREN(token):
    r'\)'
    token.lexer.paren_count -= 1
    return token


def t_newline(token):
    r'\n'
    token.lexer.lineno += len(token.value)


def t_error(token):
    print("Illegal character '%s'" % token.value[0])
    token.lexer.skip(1)


lex.lex()


# Yacc

def p_statement_if(p):
    '''statement : IF comparison THEN statement END'''
    if p[3]:
        p[0] = p[5]


def p_comparison_binop(p):
    '''comparison : expression EQU expressoin
                    |expression NEQ expression
                    |expression GEQ expression
                    |expression LEQ expression
                    |expression GRTR expression
                    |expression LESS expressoin'''

    if p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '<>':
        p[0] = p[1] != p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]


def p_expression_group(p):
    '''expression : LPAREN expression LPAREN'''
    p[0] = p[2]


def p_expression_number(p):
    '''expression : NUMBER'''
    p[0] = p[1]


def p_expression_name(p):
    '''expression : NAME'''
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_statement_assign(p):
    '''statement : NAME EQUALS expression'''
    names[p[1]] = p[3]


def p_statement_expression(p):
    '''statement : expression'''
    print(p[1])


def p_statement_for(p):
    '''statement : FOR statement TO expression DO statement END'''
    for i in range(names[p[2]], p[4], 1):
        p[6]


def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]
    #  p that is a sequence containing the values of each grammar symbol in the corresponding rule


def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]


def p_expression_times(p):
    'expression : expression TIMES term'
    p[0] = p[1] * p[3]


def p_expression_divide(p):
    'expression : expression DIVIDE term'
    if p[3] == 0:
        raise ZeroDivisionError('Divide by zero!')
    else:
        p[0] = p[1] / p[3]


def p_expression_term(p):
    'expression : term'
    p[0] = p[1]


def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]


def p_term_divide(p):
    'term : term DIVIDE factor'
    if p[3] == 0:
        raise ZeroDivisionError('Divide by zero!')
    else:
        p[0] = p[1] / p[3]


def p_term_factor(p):
    'term : factor'
    p[0] = p[1]


def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]


def p_factor_expression(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[1]


def p_error(p):
    print("Syntax error in '%s'" % p.value)


yacc.yacc()


code = 'i = 1'
yacc.parse(code)
