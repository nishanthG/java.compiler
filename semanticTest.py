import sys,re
import ply.yacc as yacc
import ply.lex as lex

import semanticAnalysis
import lexer
from semanticAnalysis import symbolTable



# Build the parser
lexer = lex.lex(module=lexer)
parser = yacc.yacc(module=semanticAnalysis)

f = open(sys.argv[1],"r")
contents = f.read()
f.close()

result = parser.parse(contents)
data = ''
for symbol in symbolTable.table:
    data += str(symbol)  + '\n'
f = open('SymbolTable.text',"w+")
f.write(data)