import sys
import ply.yacc as yacc
import ply.lex as lex

import parser
import lexer
from parser import nodes



# Build the parser
lexer = lex.lex(module=lexer)
parser = yacc.yacc(module=parser)

f = open(sys.argv[1],"r")
contents = f.read()
f.close()

result = parser.parse(contents)

visited = []
n = 0
for i in range(len(nodes)):
    current = nodes[i]
    if(type(current['right']) is list):
        for j in range(len(current['right'])):
            for k in range(len(visited)):
                if(current['right'][j] == visited[k]['right']):
                    current['right'][j] = visited[k]['left']
    else:
        for k in range(len(visited)):
                if(current['right'] == visited[k]['right']):
                    current['right'].replace(current['right'], visited[k]['left'])
                    

    temp = {'left' : current['left'] + str(i), 'right' : current['right']}
    visited.append(temp)

code = ''
n = len(visited)
for i in range(n):
    current = visited[n -i -1]
    if(type(current['right']) is list):
        for prod in current['right']:
            code += current['left'] + ' -> ' + '"' + str(prod) + '"' + '\n'
    else:
        code += current['left'] + ' -> ' + '"' + current['right'] + '"' + '\n'

code = code.replace('[','')
code = code.replace(']','')

f = open('ptree.dot',"w+")
f.write('digraph G {\n' + code + '\n}')











