import sys,re
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
'''
for node in nodes:
	print node , '\n'
print '\n\n'
'''

nonTerm = []
for i in range(len(nodes)):
    nodes[i]['left'] += '_' + str(i)
    nonTerm.append(nodes[i]['left'])

n = len(nodes)
for i in range(n):
	if(type(nodes[n-i-1]['right']) is list):
		for k in range(n-i-1):
			if(nodes[n-i-1]['right'] == nodes[k]['right']):
				nodes[n-i-1]['right'] = nodes[k]['left']
for i in range(n):
	if(type(nodes[n-i-1]['right']) is list):
	    for j in range(len(nodes[n-i-1]['right'])):
	    	if(type(nodes[n-i-1]['right'][j]) is list):
		    	for k in range(n-i-1):
		    		if(nodes[n-i-1]['right'][j] == nodes[k]['right']):
		    			nodes[n-i-1]['right'][j] = nodes[k]['left']

vis = []
def iter(i):
	if(type(nodes[i]['right']) is list ):
		for j in range(len(nodes[i]['right'])):
			if(nodes[i]['right'][j] in nonTerm):
				m = re.findall(r'\d+', nodes[i]['right'][j])
				iter(int(m[0]))
			else:
				for k in range(n):
					if(k not in vis):
						if(nodes[i]['right'][j] == nodes[k]['right']):
							nodes[i]['right'][j] = nodes[k]['left']
							vis.append(k)
	elif(nodes[i]['right'] in nonTerm):
		m = re.findall(r'\d+', nodes[i]['right'])
		iter(int(m[0]))


		    				


m = re.findall(r'\d+', nodes[n-1]['left'])
iter(int(m[0]))

'''
for node in nodes:
	print node , '\n'
'''

code = ''
for i in range(len(nodes)):
	if(type(nodes[n-1-i]['right']) is list):
		for prod in range(len(nodes[n-1-i]['right'])):
			code += nodes[n-1-i]['left'] + ' -> ' + '"' + nodes[n-1-i]['right'][prod] + '"' + '\n'
	if(type(nodes[n-1-i]['right']) is str):
		code += nodes[n-1-i]['left'] + ' -> ' + '"' + nodes[n-1-i]['right'] + '"' + '\n'

f = open('ptree.dot',"w+")
f.write('digraph G {\n' + code + '\n}')

