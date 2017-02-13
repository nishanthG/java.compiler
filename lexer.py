import ply.lex as lex


#Reserved words
reserved = {
	'if' : 'IF',
	'else' : 'ELSE',
	#'then' : 'THEN',
	'while' : 'WHILE',
	'for' : 'FOR',
	'int' : 'INT',
	'short' : 'SHORT',
	'long' : 'LONG',
	'double' : 'DOUBLE',
	'float' : 'FLOAT',
	'char' : 'CHAR',
	'void' : 'VOID',
	'boolean' : 'BOOLEAN',
	'do' : 'DO',
	'switch' : 'SWITCH',
	'case' : 'CASE',
	'new' : 'NEW',
	'class' : 'CLASS',
	'import' : 'IMPORT',
	'private' : 'PRIVATE',
	'public' : 'PUBLIC',
	'protected' : 'PROTECTED',
	'return' : 'RETURN',
	'super' : 'SUPER',
	'this' : 'THIS',
	'extends' : 'EXTENDS',
	'implements' : 'IMPLEMENTS',
	'interface' : 'INTERFACE',
	#'try' : 'TRY',
	#'catch' : 'CATCH',
	#'System' : 'SYSTEM',
	#'out' : 'OUT',
	#'in' : 'IN',
	#'print' : 'PRINT',
	#'println' : 'PRINT_LN',
	'instanceof' : 'INSTANCEOF',
	'assert' : 'ASSERT',
	'default' : 'DEFAULT',
	'break' : 'BREAK',
	'continue' : 'CONTINUE',
	'synchronized' : 'SYNCHRONIZED',
	'throw' : 'THROW',
	'throws' : 'THROWS',
	#'finally' : 'FINALLY',
	'static' : 'STATIC',
	'abstract' : 'ABSTRACT',
	#'true' : 'TRUE',
	#'false' : 'FALSE',
	'final' : 'FINAL',
	'native' : 'NATIVE',
	'transient' : 'TRANSIENT',
	'volatile' : 'VOLATILE',
	'strictfp' : 'STRICTFP',
	'byte' : 'BYTE',
	'enum' : 'ENUM',
	'package' : 'PACKAGE'

}


#Tokens
tokens = [
	'IDENTIFIER',
	'NUMBER',
	'LITERAL',
	'PLUS',
	'MINUS',
	'TIMES',
	'DOT_STAR',
	'DIVIDE',
	'MOD',
	'ASSIGNMENT',
	'POWER',
	'OR',
	'AND',
	'EQUAL',
	'LE',
	'LT',
	'GE',
	'GT',
	'NOT_EQUAL',
	'NOT',
	'EXPLAMETARY',
	'L_BRACE',
	'R_BRACE',
	'L_CURL_BRACE',
	'R_CURL_BRACE',
	'L_SQUARE_BRACE',
	'R_SQUARE_BRACE',
	#'SINGLE_QUOTE',
	#'DOUBLE_QUOTE',
	'SEMICOLON',
	'COLON',
	'COMMA',
	'DOT',
	'L_SHIFT',
	'R_SHIFT',
	'RR_SHIFT',
	'TIMES_ASSIGNMENT',
	'DIVIDE_ASSIGNMENT',
	'PLUS_ASSIGNMENT',
	'MINUS_ASSIGNMENT',
	'L_SHIFT_ASSIGNMENT',
	'R_SHIFT_ASSIGNMENT',
	'RR_SHIFT_ASSIGNMENT',
	'POWER_ASSIGNMENT',
	'MOD_ASSIGNMENT',
	'AND_ASSIGNMENT',
	'OR_ASSIGNMENT',
	#'XOR_ASSIGNMENT',
	'PLUS_PLUS',
	'MINUS_MINUS',
	#'ELLIPSIS',
	'CURL_DASH',
	#'AT',

] + list(reserved.values())

#Regular expression rules
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DOT_STAR = r'\.\*'
t_DIVIDE = r'\/'
t_MOD = r'\%'
t_ASSIGNMENT = r'\='
t_POWER = r'\^'
t_OR = r'\|\| | \|'
t_AND = r'\& | \&\&'
t_EQUAL = r'\=\='
t_LE = r'\<\='
t_LT = r'\<'
t_GE = r'\>\='
t_GT = r'\>'
t_NOT_EQUAL = r'\!\='
t_NOT = r'\!'
t_EXPLAMETARY = r'\?'
t_L_BRACE = r'\('
t_R_BRACE = r'\)'
t_L_CURL_BRACE = r'\{'
t_R_CURL_BRACE = r'\}'
t_L_SQUARE_BRACE = r'\['
t_R_SQUARE_BRACE = r'\]'
#t_SINGLE_QUOTE = r'\''
#t_DOUBLE_QUOTE = r'\"'
t_SEMICOLON = r'\;'
t_COLON = r'\:'
t_COMMA = r'\,'
t_DOT = r'\.'
t_L_SHIFT = r'\<\<'
t_R_SHIFT = r'\>\>'
t_RR_SHIFT = r'\>\>\>'
t_TIMES_ASSIGNMENT = r'\*\='
t_DIVIDE_ASSIGNMENT = r'\/\='
t_PLUS_ASSIGNMENT = r'\+\='
t_MINUS_ASSIGNMENT = r'\-\='
t_POWER_ASSIGNMENT = r'\^\='
t_MOD_ASSIGNMENT = r'\%\='
t_L_SHIFT_ASSIGNMENT = r'\<\<\='
t_R_SHIFT_ASSIGNMENT = r'\>\>\='
t_RR_SHIFT_ASSIGNMENT = r'\>\>\>\='
t_AND_ASSIGNMENT = r'\&\='
t_OR_ASSIGNMENT = r'\|\='
#t_XOR_ASSIGNMENT = r'\^\='
t_PLUS_PLUS = r'\+\+'
t_MINUS_MINUS = r'\-\-'
t_NUMBER = r'\d+(.\d+)?(E[+-]?\d+)?'
#t_ELLIPSIS = r'\.\.\.'
t_CURL_DASH = r'\~'
#t_AT = r'\@'

def t_IDENTIFIER(t):
    r'[a-zA-Z]([a-zA-Z]|[0-9])*'
    t.type = reserved.get(t.value,'IDENTIFIER')
    return t

def t_LITERAL(t):
    r"(?P<start>\"|')[^\"']*(?P=start)"
    t.value = t.value.replace("\"", "").replace("'s", "")
    return t

# Line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

#Ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


