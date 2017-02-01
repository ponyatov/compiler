SRC = '''
# comment
a =-01
b =+2.3
c = -3e+04
'''

import ply.lex  as lex
import ply.yacc as yacc

tokens = [ 'SYM' , 'NUM' , 'OP' ]

t_ignore_comment = r'\#.*'
t_ignore = ' \t\r'
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    
def t_NUM(t):
    r'\d+(\.\d*)?([eE][\+\-]?\d+)?'
    t.value = float(t.value) ; return t
def t_SYM(t):
    r'[a-zA-Z0-9_]+'
    return t
def t_OP(t):
    r'[\=\+\-\*\/\^]'
    return t

def p_REPL_none(p):
    ' REPL : '
def p_REPL_recur(p):
    ' REPL : REPL ex '
    print p[2]
def p_ex_scalar(p):
    ''' ex : SYM
            | NUM
            | OP    '''
    p[0] = p[1]
    
def t_error(t): print 'error/lexer', t
def p_error(p): print 'parse/lexer', p

lexer = lex.lex()
yacc.yacc(debug=False, write_tables=False).parse(SRC)
