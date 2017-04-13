import sys,re
import ply.yacc as yacc
import ply.lex as lex

import semanticAnalysis
import lexer
from semanticAnalysis import symbolTables, ast



# Build the parser
lexer = lex.lex(module=lexer)
parser = yacc.yacc(module=semanticAnalysis)

f = open(sys.argv[1],"r")
contents = f.read()
f.close()

result = parser.parse(contents)
data = 'Name        Type        Value \n\n'
for symbolTable in symbolTables:
    for symbol in symbolTable.table:
        data += symbol['Name'] + "      " + symbol['Type'] + "      "+ str(symbol['Value'])  + '\n'
    data += '\n'
f = open('SymbolTable.text',"w+")
f.write(data)
f = open("Ast.text", "w+")
f.write(str(ast[1]))
f.close