import sys,re
import ply.yacc as yacc
import ply.lex as lex

import semanticAnalysis
import lexer
from semanticAnalysis import symbolTables, ast
from codeGen import CodeGen


# Build the parser
lexer = lex.lex(module=lexer)
parser = yacc.yacc(module=semanticAnalysis)

f = open(sys.argv[1],"r")
contents = f.read()
f.close()

result = parser.parse(contents)

f = open("Ast.text", "w+")
f.write(str(ast[1]))

tac = ast[1].genTac()

f1 = open("tac.text", "w+")
f2 = open("tac1.text", "w+")
#print "\n"
#print tac.getTemps()
#print "\n"
tac.getTacFile("tac.text")
tac.optimizeTac()
tac.getTacFile("tac1.text")
#print tac.getTemps()
#print "\n"

codeGen = CodeGen(symbolTables, tac.getTac(), tac.getTemps())

codeGen.genMipsCode()
f3 = open("mips.s", "w+")
codeGen.getMipsFile("mips.s")
#print codeGen.getMethods()
#print codeGen.getGlobVars()


data = '    Name        Type        Value \n\n'
for symbolTable in symbolTables:
    data += symbolTable._name + ":\n\n"
    for symbol in symbolTable.table:
    	if "Offset" in symbol:
        	data += "   " + symbol['Name'] + "      " + str(symbol['Type']) + "      "+ str(symbol['Value'])+ "		"  + str(symbol["Offset"]) +'\n'
        else:
        	data += "   " + symbol['Name'] + "      " + str(symbol['Type']) + "      "+ str(symbol['Value'])  + '\n'

        #data += str(symbol)
    data += '\n'
f = open('SymbolTable.csv',"w+")
f.write(data)
