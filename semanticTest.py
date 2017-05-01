import sys,re
import ply.yacc as yacc
import ply.lex as lex

import semanticAnalysis
import lexer
from semanticAnalysis import symbolTables, ast
from ast import tac



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
        data += symbol['Name'] + "      " + str(symbol['Type']) + "      "+ str(symbol['Value'])  + '\n'
        #data += str(symbol)
    data += '\n'
f = open('SymbolTable.csv',"w+")
f.write(data)
f = open("Ast.text", "w+")
f.write(str(ast[1]))
#print ast
ast[1].getTac()

f1 = open("tac.text", "w+")
f2 = open("tac1.text", "w+")
print tac.getVariables()
print "\n"
print tac.getTemps()
print "\n"
tac.getTacFile("tac.text")
tac.optimizeTac()
tac.getTacFile("tac1.text")
print tac.getTemps()
print "\n"
