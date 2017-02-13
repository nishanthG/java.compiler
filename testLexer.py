import sys
import ply.lex as lex
import lexer


lexer = lex.lex(module=lexer)


f = open(sys.argv[1],"r")
contents = f.read()
f.close()

lexer.input(contents)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok.type, tok.value, tok.lineno, tok.lexpos)