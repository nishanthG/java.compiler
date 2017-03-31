import sys,re
import ply.yacc as yacc
import ply.lex as lex

import semanticAnalysis
import lexer
from semanticAnalysis import symbolTables



# Build the parser
lexer = lex.lex(module=lexer)
parser = yacc.yacc(module=semanticAnalysis)

f = open(sys.argv[1],"r")
contents = f.read()
f.close()

result = parser.parse(contents)
data = ''
for symbolTable in symbolTables:
    for symbol in symbolTable.table:
        data += str(symbol)  + '\n'
    data += '\n'
f = open('SymbolTable.text',"w+")
f.write(data)