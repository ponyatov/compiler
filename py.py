class Sym:
    tag = 'sym'
    def __init__(self, V, L): self.val = V ; self.nest = [] ; self.attr = {}
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
class Lambda(Sym):
    tag = 'lambda'
    def __init__(self): Sym.__init__(self, '', 0)
class Vector(Sym):
    tag = 'vector'
    def __init__(self, L): Sym.__init__(self, '', L)

import ply.lex  as lex
import ply.yacc as yacc

tokens = [ 'SYM' , 'NUM' , 'OP' , 'EQ' ,
          'ADD','SUB','MUL',
          'LC','RC','COLON',
          'LP','RP','COMMA' ]

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
def t_LP(t):
    r'\('
    t.value = Op(t.value, t.lineno) ; return t
def t_RP(t):
    r'\)'
    t.value = Op(t.value, t.lineno) ; return t
def t_LC(t):
    r'\{'
    t.value = Op(t.value, t.lineno) ; return t
def t_RC(t):
    r'\}'
    t.value = Op(t.value, t.lineno) ; return t
def t_COLON(t):
    r'\:'
    t.value = Op(t.value, t.lineno) ; return t
def t_COMMA(t):
    r'\,'
    t.value = Op(t.value, t.lineno) ; return t
def t_EQ(t):
    r'\='
    t.value = Op(t.value, t.lineno) ; return t
def t_OP(t):
    r'[\/\^]'
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
def p_ex_eq(p):
    ' ex : ex EQ ex '
    p[0] = p[2] ; p[0] += p[1] ; p[0] += p[3]
def p_ex_add(p):
    ' ex : ex ADD ex '
    p[0] = p[2] ; p[0] += p[1] ; p[0] += p[3]
def p_ex_mul(p):
    ' ex : ex MUL ex '
    p[0] = p[2] ; p[0] += p[1] ; p[0] += p[3]
    
def p_ex_lambda(p):
    ' ex : LC lambda RC '
    p[0] = p[2]
def p_lambda_new(p):
    ' lambda : '
    p[0] = Lambda()
def p_lambda_param(p):
    ' lambda : lambda SYM COLON '
    p[0] = p[1] ; p[0].attr[p[2].val] = p[2]
def p_lambda_ex(p):
    ' lambda : lambda ex '
    p[0] = p[1] ; p[0] += p[2]
def p_ex_fncall(p):
    ' ex : SYM LP params RP '
    p[0] = p[1] ; p[0] += p[3]
def p_params_none(p):
    ' params : '
    p[0] = Vector(0)
def p_params(p):
    ' params : params ex COMMA '
    p[0] = p[1] ; p[0] += p[2]
def p_params_single(p):
    ' params : params ex '
    p[0] = p[1] ; p[0] += p[2]
    
def t_error(t): print 'error/lexer', t
def p_error(p): print 'parse/lexer', p

lex.lex()
yacc.yacc(debug=False, write_tables=False).parse('''

# comment
a =-01
b =+2.3
c = -3e+04
a+b*c
pp = {X:Y}
pp(1,2,Z=3)  

''')
