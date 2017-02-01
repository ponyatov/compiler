class Sym:
    tag = 'sym'
    def __init__(self, V, L):
        self.val = V ; self.nest = []
        self.attr = {'line':L}
    def __iadd__(self,o): return self.push(o)
    def push(self, o): self.nest.append(o) ; return self
    def __repr__(self): return self.head()
    def head(self): return '<%s:%s>' % (self.tag, self.val)
    def dump(self, depth=0):
        S = '\n' + '\t' * depth + self.head()
        for i in self.attr: S += ',%s=%s'%(i,self.attr[i])
        for i in self.nest: S += i.dump(depth + 1)
        return S
class Num(Sym):
    tag = 'num'
    def __init__(self, V, L): Sym.__init__(self, V, L) ; self.val = float(V)
class Op(Sym):
    tag = 'op'

import ply.lex  as lex
import ply.yacc as yacc

tokens = [ 'SYM' , 'NUM' , 'OP' , 'ADD','SUB','MUL' ]

t_ignore_comment = r'\#.*'
t_ignore = ' \t\r'
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    
def t_NUM(t):
    r'\d+(\.\d*)?([eE][\+\-]?\d+)?'
    t.value = Num(t.value, t.lineno) ; return t
def t_SYM(t):
    r'[a-zA-Z0-9_]+'
    t.value = Sym(t.value, t.lineno) ; return t
def t_ADD(t):
    r'\+'
    t.value = Op(t.value, t.lineno) ; return t
def t_SUB(t):
    r'\-'
    t.value = Op(t.value, t.lineno) ; return t
def t_MUL(t):
    r'\*'
    t.value = Op(t.value, t.lineno) ; return t
def t_OP(t):
    r'[\=\/\^]'
    t.value = Op(t.value, t.lineno) ; return t

precedence = [
    ('left','ADD','SUB'),
    ('left','MUL'),
    ('right','PFX'),
    ]

def p_REPL_none(p):
    ' REPL : '
def p_REPL_recur(p):
    ' REPL : REPL ex '
    print p[2].dump()
def p_ex_scalar(p):
    ''' ex : SYM
            | NUM
            | OP    '''
    p[0] = p[1]
def p_ex_pfx_add(p):
    ' ex  : ADD ex %prec PFX '
    p[0] = p[1] ; p[0] += p[2]
def p_ex_pfx_sub(p):
    ' ex  : SUB ex %prec PFX '
    p[0] = p[1] ; p[0] += p[2]
def p_ex_add(p):
    ' ex : ex ADD ex '
    p[0] = p[2] ; p[0] += p[1] ; p[0] += p[3]
def p_ex_mul(p):
    ' ex : ex MUL ex '
    p[0] = p[2] ; p[0] += p[1] ; p[0] += p[3]
    
def t_error(t): print 'error/lexer', t
def p_error(p): print 'parse/lexer', p

lex.lex()
yacc.yacc(debug=False, write_tables=False).parse('''

# comment
a =-01
b =+2.3
c = -3e+04
a+b*c

''')
