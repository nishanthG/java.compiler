import ply.yacc as yacc
from lexer import tokens
from models import *
from stack import Stack
from SymbolTable import SymbolTable

symbolTables = []
symbolTable = SymbolTable(None)
symbolTables.append(symbolTable)
operatorStack = Stack()
operandStack = Stack()
priority = {  '+': 1,
              '-': 1,
              '*': 2,
              '/': 2,
              '%': 2,
              '^': 3,
              '==': 4,
              '!=': 4,
              '<': 5,
              '>': 5,
              '<=': 5,
              '>=': 5,
              '|': 6,
              '&': 7 }
arithOp = ['+', '-', '*', '/']
compOp = ['<', '>', '<=', '>=', '==', '!=', '&', '|']

def p_CompilationUnit(p):
  '''CompilationUnit : PACKAGE QualifiedIdentifier SEMICOLON ImportDeclarationList TypeDeclarationList 
                     | ImportDeclarationList TypeDeclarationList'''

def p_ImportDeclarationList(p):
  '''ImportDeclarationList : ImportDeclaration ImportDeclarationList
                       |  '''

def p_TypeDeclarationList(p):
  '''TypeDeclarationList : TypeDeclaration TypeDeclarationList
                     |  '''

def p_QualifiedIdentifier(p):
  '''QualifiedIdentifier : IDENTIFIER    
                         | IDENTIFIER DOT QualifiedIdentifier '''
  if(len(p) == 2):
    if(symbolTable.lookup(p[1])):
      p[0] = {'Type': symbolTable.lookup(p[1])['Type'], 'Value': Leaf('IDENTIFIER', p[1])}
    else:
      errorReport('Error at line no ' + str(p.lineno(1)) + ', ' + p[1] + ' not defined')


def p_QualifiedIdentifierList(p): 
  '''QualifiedIdentifierList : QualifiedIdentifier   
                             | QualifiedIdentifier COMMA QualifiedIdentifierList   '''
  
def p_ImportDeclaration(p):
  '''ImportDeclaration : IMPORT QualifiedIdentifier DOT_STAR SEMICOLON 
                       | IMPORT QualifiedIdentifier SEMICOLON
                       | IMPORT STATIC QualifiedIdentifier SEMICOLON
                       | IMPORT STATIC QualifiedIdentifier DOT_STAR SEMICOLON'''

def p_TypeDeclaration(p):
  '''TypeDeclaration : ClassOrInterfaceDeclaration
                     | SEMICOLON '''

def p_ClassOrInterfaceDeclaration(p):
  '''ClassOrInterfaceDeclaration : ModifierList ClassDeclaration '''
  symbolTable.table[len(symbolTable.table)-1]['Modifiers'] = p[1]

def p_ClassDeclaration(p): 
  '''ClassDeclaration : NormalClassDeclaration'''

def p_NormalClassDeclaration(p): 
  '''NormalClassDeclaration : CLASS IDENTIFIER ClassBody
                            | CLASS IDENTIFIER  EXTENDS Type  ClassBody
                            | CLASS IDENTIFIER  IMPLEMENTS TypeList  ClassBody
                            | CLASS IDENTIFIER  EXTENDS Type IMPLEMENTS TypeList  ClassBody'''
  if(symbolTable.lookup(p[1])):
    errorReport('Error at' + str(p.lineno(2)) + ' "' + p[2] + '" ' + ' is already defined')
  else:
    symbolTable.insert({'Name':p[2], 'Type':p[1]})    


def p_SquareBraceList(p):
  '''SquareBraceList : 
                  | L_SQUARE_BRACE R_SQUARE_BRACE SquareBraceList
                  | L_SQUARE_BRACE NUMINT R_SQUARE_BRACE SquareBraceList'''

def p_ModifierList(p):
  ''' ModifierList : Modifier ModifierList
               |  '''
  if(len(p) == 3):             
    p[0] = [p[1]] + p[2]
  else:
    p[0] = []

def p_Type(p): 
  '''Type : BasicType SquareBraceList
          | QualifiedIdentifier SquareBraceList''' 
  p[0] = p[1]

def p_BasicType(p):
  '''BasicType : BYTE
               | SHORT
               | CHAR
               | INT
               | LONG
               | FLOAT
               | DOUBLE
               | BOOLEAN
               | STRING'''
  p[0] = p[1]

def p_TypeList(p):
  '''TypeList : QualifiedIdentifier  
              | QualifiedIdentifier COMMA TypeList   '''

def p_Modifier(p):
  '''Modifier : PUBLIC
              | PROTECTED
              | PRIVATE
              | STATIC 
              | ABSTRACT
              | FINAL
              | NATIVE
              | SYNCHRONIZED
              | TRANSIENT
              | VOLATILE
              | STRICTFP'''
  p[0] = p[1]

def p_ClassBody(p):
  '''ClassBody : L_CURL_BRACE Marker1 ClassBodyDeclarationList R_CURL_BRACE '''
  global symbolTable
  symbolTable = symbolTable.parent

def p_Marker1(p):
  '''Marker1 :  '''
  global symbolTable
  symbolTable = SymbolTable(symbolTable)
  symbolTables.append(symbolTable)

def p_ClassBodyDeclarationList(p):
  ''' ClassBodyDeclarationList : ClassBodyDeclaration ClassBodyDeclarationList
                           |  '''

def p_ClassBodyDeclaration(p):
  '''ClassBodyDeclaration : SEMICOLON 
                          | ModifierList MemberDecl 
                          | STATIC  Block
                          | Block'''
  if(len(p) == 3 and p[1] != 'static'):
    symbolTable.table[len(symbolTable.table)-1]['Modifiers'] = p[1]

  
def p_MemberDecl(p):
  '''MemberDecl : MethodOrFieldDecl
                | VOID IDENTIFIER VoidMethodDeclaratorRest
                | ClassDeclaration'''
  if(len(p)==4):
    if(symbolTable.lookupScope(p[2])):
      errorReport('Error at' + str(p.lineno(2)) + ' "' + p[2] + '" ' + ' is already defined')
    else:
      symbolTable.insert({'Name':p[2], 'Type':p[1]})  
  
def p_MethodOrFieldDecl(p):
  '''MethodOrFieldDecl : Type IDENTIFIER MethodOrFieldRest'''
  if(p[3][0] == ';'):
    if(symbolTable.lookupScope(p[2])):
      errorReport('Error at line no ' + str(p.lineno(2)) + '"' + p[2] + '"' + ' is already defined')
    else:
      if(type(p[3][1]) is dict):
        if(p[3][1]['Type'] == p[1]):
          symbolTable.insert({'Name':p[2], 'Type':p[1], 'value':p[3][1]['Value']})
        else:
          errorReport(message='Error at line no ' + str(p.lineno(2)) + ', Type Mismatch: expected "' + p[1] + '"' + ' but found "' + p[3][1]['Type'] + '"')
      else:
        symbolTable.insert({'Name':p[2], 'Type':p[1], 'value': 0})
      
    for i in range(2, len(p[3])):
      if(type(p[3][i]) is dict):
        if(symbolTable.lookupScope(p[3][i]['Name'])):
          errorReport('Error at line no ' + str(p.lineno(2)) + ', '+ '"' + p[3][i]['Name'] + '"' + ' is already defined')       
        else:
          if(p[3][i]['Type'] == p[1]):
            symbolTable.insert({'Name':p[3][i]['Name'], 'Type':p[1], 'Value':p[3][i]['Value']})
          else:
            errorReport(message='Error at line no ' + str(p.lineno(2)) + ', '+ ' Type Mismatch: expected "' + p[1] + '"' + ' but found "' + p[3][i]['Type'] + '"')
      else:
        if(symbolTable.lookupScope(p[3][i])):
          errorReport('Error at line no ' + str(p.lineno(2)) + ', ' + '"' + p[3][i] + '"' + ' is already defined')
        else:
          symbolTable.insert({'Name':p[3][i], 'Type':p[1], 'Value':0})
  else:
    if(symbolTable.lookupScope(p[2])):
      errorReport('Error at line no ' + str(p.lineno(2)) + ', '+ '"' + p[2] + '"' + ' is already defined')
    else:
      symbolTable.insert({'Name':p[2], 'Type': 'Method', 'ReturnType':p[1]})
  
def p_MethodOrFieldRest(p):
  '''MethodOrFieldRest : FieldDeclaratorsRest SEMICOLON
                       | MethodDeclaratorRest'''
  if(len(p) == 3):
    p[0] = [p[2]] + p[1]
  else:
    p[0] = ['Method']
  
def p_CommaVariableDeclarators(p):
  '''CommaVariableDeclarators : COMMA VariableDeclarator CommaVariableDeclarators
                        |  '''
  if(len(p) == 4):
    p[0] = [p[2]] + p[3]
  else:
    p[0] = []

def p_FieldDeclaratorsRest(p):
  '''FieldDeclaratorsRest : VariableDeclaratorRest CommaVariableDeclarators '''
  p[0] = [p[1]] + p[2]
  
def p_MethodDeclaratorRest(p):
  '''MethodDeclaratorRest : FormalParameters Block
                          | FormalParameters SEMICOLON
                          | FormalParameters THROWS QualifiedIdentifierList Block 
                          | FormalParameters THROWS QualifiedIdentifierList SEMICOLON '''
  
def p_VoidMethodDeclaratorRest(p):
  '''VoidMethodDeclaratorRest : FormalParameters Block 
                              | FormalParameters SEMICOLON  
                              | FormalParameters THROWS QualifiedIdentifierList Block
                              | FormalParameters THROWS QualifiedIdentifierList SEMICOLON '''
  
def p_FormalParameters(p):
  '''FormalParameters : L_BRACE Marker2 R_BRACE
                      | L_BRACE Marker2 FormalParameterDecls R_BRACE '''
  global symbolTable
  symbolTable = symbolTable.parent

def p_Marker2(p):
  '''Marker2 :  '''
  global symbolTable
  symbolTable = SymbolTable(symbolTable)
  symbolTables.append(symbolTable)

  
def p_VariableModifier(p):
  ''' VariableModifier : 
                       | FINAL VariableModifier '''
  if(len(p) == 3):
    p[0] = [p[1]] + p[2]
  else:
    p[0] = []
  
def p_FormalParameterDecls(p):
  '''FormalParameterDecls : Type FormalParameterDeclsRest
                          | VariableModifier Type FormalParameterDeclsRest'''
  if(len(p) == 3):
    if(symbolTable.lookupScope(p[2])):
      errorReport('Error : '+ p[2] + ' is already defined')
    else:
      symbolTable.insert({'Name': p[2], 'Type':p[1], 'Value': None})
  else:
    if(symbolTable.lookupScope(p[3])):
      errorReport('Error :' + p[3] + ' is already defined')
    else:
      symbolTable.insert({'Name': p[3], 'Type':p[2], 'VariableModifier': p[1], 'Value': None})
  
def p_FormalParameterDeclsRest(p):
  '''FormalParameterDeclsRest : VariableDeclaratorId 
                              | VariableDeclaratorId COMMA FormalParameterDecls 
                              | DOT DOT DOT VariableDeclaratorId'''
  if(len(p) == 2):
    p[0] = p[1]
  elif(len(p) == 4):
    p[0] = p[1]

def p_VariableDeclaratorId(p):
  '''VariableDeclaratorId : IDENTIFIER SquareBraceList '''
  p[0] = p[1]

def p_VariableDeclarators(p):
  '''VariableDeclarators : VariableDeclarator
                         | VariableDeclarator COMMA VariableDeclarators   '''
  if(len(p) == 2):
    p[0] = [p[1]]
  else:
    p[0] = [p[1]] + p[3]
  
def p_VariableDeclarator(p):
  '''VariableDeclarator : IDENTIFIER VariableDeclaratorRest'''
  if(type(p[2]) is dict):
    p[0] = {'Name':p[1], 'Value':p[2]['Value'], 'Type': p[2]['Type']}
  else:
    p[0] = p[1]


  
def p_VariableDeclaratorRest(p):
  '''VariableDeclaratorRest : SquareBraceList  
                            | SquareBraceList ASSIGNMENT VariableInitializer  '''
  if(len(p) == 4):
    p[0] = p[3]


def p_VariableInitializer(p):
  '''VariableInitializer : ArrayInitializer
                         | Expression'''
  p[0] = p[1] #for expression only, Array still need to be considered
  
def p_VariableInitializerList(p):
  ''' VariableInitializerList : VariableInitializer
                          | VariableInitializer COMMA VariableInitializerList '''
                       
def p_ArrayInitializer(p):
  ''' ArrayInitializer : L_SQUARE_BRACE VariableInitializerList R_SQUARE_BRACE 
                       | L_SQUARE_BRACE VariableInitializerList R_SQUARE_BRACE COMMA '''
  
def p_Block(p):
  '''Block : L_CURL_BRACE Marker3 BlockStatements R_CURL_BRACE'''
  global symbolTable
  symbolTable = symbolTable.parent

def p_Marker3(p):
  '''Marker3 :  '''
  global symbolTable
  symbolTable = SymbolTable(symbolTable)
  symbolTables.append(symbolTable)
  
def p_BlockStatements(p):
  '''BlockStatements : BlockStatement BlockStatements 
                     | '''

def p_BlockStatement(p):
  '''BlockStatement : LocalVariableDeclarationStatement
                    | ClassOrInterfaceDeclaration
                    | Statement
                    | IDENTIFIER COLON  Statement'''
  
def p_LocalVariableDeclarationStatement(p):
  '''LocalVariableDeclarationStatement : Type VariableDeclarators SEMICOLON
                                       | VariableModifier Type VariableDeclarators SEMICOLON'''
  if(len(p) == 4):
    for i in range(0, len(p[2])):
      if(type(p[2][i]) is dict):
        if(symbolTable.lookupScope(p[2][i]['Name'])):
          errorReport('Error: ' + '"' + p[2][i]['Name'] + '"' + ' is already defined')
        else:
          if(p[2][i]['Type'] == p[1]):
            symbolTable.insert({'Name':p[2][i]['Name'], 'Type':p[1], 'Value':p[2][i]['Value']})
          else:
            errorReport(message= 'Error at line no ' + str(p.lineno(3))+ 'Type Mismatch: expected "' + p[1]['Type'] + '"' + ' but found "' + p[2]['Type'] + '"')
      else:
        if(symbolTable.lookupScope(p[2][i])):
          errorReport('Error at line no ' + str(p.lineno(3)) + ', ' + '"' + p[2][i] + '"' + ' is already defined')
        else:
          symbolTable.insert({'Name':p[2][i], 'Type':p[1], 'Value':0})
  else:
    for i in range(0, len(p[3])):
      if(type(p[3][i]) is dict):
        if(symbolTable.lookupScope(p[3][i]['Name'])):
          errorReport('Error: ' + '"' + p[3][i]['Name'] + '"' + ' is already defined')
        else:
          if(p[3][i]['Type'] == p[2]):
            symbolTable.insert({'Name':p[3][i]['Name'], 'Type':p[2], 'VariableModifier': p[1], 'Value':p[3][i]['Value']})
          else:
            errorReport(message='Error at line no ' + str(p.lineno(3)) + ', '+ 'Type Mismatch: expected "' + p[2]['Type'] + '"' + ' but found "' + p[3]['Type'] + '"')
      else:
        if(symbolTable.lookupScope(p[3][i], scope)):
          errorReport('Error at line no ' + str(p.lineno(3)) + ', '+ '"' + p[3][i] + '"' + ' is already defined')
        else:
          symbolTable.insert({'Name':p[3][i], 'Type':p[2], 'VariableModifier': p[1], 'Value':0})

  
def p_Statement(p):
  '''Statement : Block
              | SEMICOLON
              | StatementExpression SEMICOLON
              | IF ParExpression Statement
              | IF ParExpression Statement ELSE Statement  
              | ASSERT Expression SEMICOLON
              | ASSERT Expression COLON Expression SEMICOLON
              | SWITCH ParExpression L_CURL_BRACE SwitchBlockStatementGroups R_CURL_BRACE     
              | WHILE ParExpression Statement
              | DO Statement WHILE ParExpression SEMICOLON
              | FOR  L_BRACE ForControl R_BRACE Statement
              | BREAK SEMICOLON
              | BREAK IDENTIFIER SEMICOLON
              | CONTINUE SEMICOLON
              | CONTINUE IDENTIFIER  SEMICOLON
              | RETURN SEMICOLON
              | RETURN Expression SEMICOLON
              | THROW Expression SEMICOLON
              | SYNCHRONIZED ParExpression Block '''
              #| IDENTIFIER COLON Statement
  if(p[1] in ['if', 'while']):
    if (p[2]['Type'] != 'boolean'):
      errorReport('Error at line no ' + str(p.lineno(1))+ ', expected ' + '"boolean value" ' + 'but found "' + p[2]['Type'] + '"')
  if(p[1] == 'do'):
    if (p[4]['Type'] != 'boolean'):
      errorReport('Error at line no ' + str(p.lineno(3))+ ', expected ' + '"boolean value" ' + 'but found "' + p[4]['Type'] + '"')

             

def p_StatementExpression(p):
  '''StatementExpression : Expression'''
  
def p_SwitchBlockStatementGroups(p):
  '''SwitchBlockStatementGroups : SwitchBlockStatementGroup SwitchBlockStatementGroups
                                |  '''
  
def p_SwitchBlockStatementGroup(p):
  '''SwitchBlockStatementGroup : SwitchLabels BlockStatements'''
  
def p_SwitchLabels(p):
  '''SwitchLabels : SwitchLabel
                  | SwitchLabel  SwitchLabels'''
  
def p_SwitchLabel(p):
  '''SwitchLabel : CASE Expression COLON
                 | DEFAULT COLON'''


def p_ForControl(p):
  '''ForControl : ForVarControl
                | ForUpdate SEMICOLON SEMICOLON 
                | ForUpdate SEMICOLON   Expression  SEMICOLON   
                | ForUpdate SEMICOLON   SEMICOLON   ForUpdate
                | ForUpdate SEMICOLON   Expression  SEMICOLON   ForUpdate '''
  
def p_ForVarControl(p):
  '''ForVarControl :  Type VariableDeclaratorId  ForVarControlRest
                   |  VariableModifier   Type VariableDeclaratorId  ForVarControlRest'''
  if(len(p)==4):
    if(symbolTable.lookupScope(p[2])):
      errorReport('Error at line no ' + str(p.lineno(2)) +', '+ '"' + p[2] + '"' + ' is already defined')
    else:
      if(p[1] == p[3][0]['Type']):
        symbolTable.insert({'Name':p[2], 'Type':p[1], 'Value':p[3][0]['Value']})
      else:
        errorMessage(message='Error at line no ' + str(p.lineno(2)) +', '+ 'Type Mismatch: expected "' + p[1]['Type'] + '"' + ' but found "' + p[2]['Type'] + '"')
    for i in range(1, len(p[3])):
      if(symbolTable.lookupScope(p[3][i]['Name'])):
        errorReport('Error at line no ' + str(p.lineno(2)) +', '+ '"' + p[3][i]['Name'] + '"' + ' is already defined')
      else:
        if(p[1] == p[3][i]['Type']):
          symbolTable.insert({'Name':p[3][i]['Name'], 'Type':p[1], 'Value':p[3][i]['Value']}) 
        else:
          errorMessage('Error at line no ' + str(p.lineno(2))+', '+ 'Type Mismatch: expected "' + p[1]['Type'] + '"' + ' but found "' + p[3]['Type'] + '"')
  else:
    if(symbolTable.lookupScope(p[3])):
      errorReport('Error at line no ' + str(p.lineno(3)) + ', '+ '"' + p[3] + '"' + ' is already defined')
    else:
      if(p[2] == p[4][0]['Type']):
        symbolTable.insert({'Name':p[3], 'Type':p[2], 'Value':p[4][0]['Value']})
      else:
        errorMessage(message='Error at line no ' + str(p.lineno(3)) + ', Type Mismatch: expected "' + p[2]['Type'] + '"' + ' but found "' + p[3]['Type'] + '"')
    for i in range(1, len(p[4])):
      if(symbolTable.lookupScope(p[4][i]['Name'])):
        errorReport('Error: ' + '"' + p[4][i]['Name'] + '"' + ' is already defined')  
      else:
        if(p[2] == p[4][i]['Type']):
          symbolTable.insert({'Name':p[4][i]['Name'], 'Type':p[2], 'Value':p[4][i]['Value']})
        else:
          errorMessage(message='Error at line no ' + str(p.lineno(3)) + ', Type Mismatch: expected "' + p[2]['Type'] + '"' + ' but found "' + p[4]['Type'] + '"')

  
def p_ForVarControlRest(p): 
  '''ForVarControlRest : ForVariableDeclaratorsRest SEMICOLON SEMICOLON 
                       | ForVariableDeclaratorsRest SEMICOLON   Expression  SEMICOLON 
                       | ForVariableDeclaratorsRest SEMICOLON   SEMICOLON   ForUpdate
                       | ForVariableDeclaratorsRest SEMICOLON   Expression  SEMICOLON   ForUpdate 
                       | COLON Expression'''
  if(p[1] != ':'):
    p[0] = p[1]
  
def p_ForVariableDeclaratorsRest(p):
  '''ForVariableDeclaratorsRest : ASSIGNMENT VariableInitializer CommaVariableDeclarators  '''
  p[0] = [p[2]] + p[3]

def p_ForUpdate(p):
  '''ForUpdate : StatementExpression
               | StatementExpression  COMMA ForUpdate   ''' 

def p_Expression(p):
  '''Expression : Expression1
                | Expression1  AssignmentOperator Expression1'''
  if(len(p) == 2):
    p[0] = p[1]
  else:
    if(p[1]['Type'] == p[3]['Type']):
      p[0] = {'Type': p[1]['Type'], 'Value': BinaryExpression(p[1], p[2], p[3])}
    else:
      errorReport(message='Error near ' + p[2] + ' Type Mismatch: expected "' + p[1]['Type'] + '"' + ' but found "' + p[3]['Type'] + '"' )
  
def p_AssignmentOperator(p):
  '''AssignmentOperator : ASSIGNMENT 
                        | PLUS_ASSIGNMENT
                        | MINUS_ASSIGNMENT 
                        | TIMES_ASSIGNMENT
                        | DIVIDE_ASSIGNMENT
                        | AND_ASSIGNMENT
                        | OR_ASSIGNMENT
                        | POWER_ASSIGNMENT
                        | MOD_ASSIGNMENT
                        | L_SHIFT_ASSIGNMENT
                        | R_SHIFT_ASSIGNMENT
                        | RR_SHIFT_ASSIGNMENT'''
  p[0] = p[1]
  
def p_Expression1(p) :
  '''Expression1 : Expression2
                 | Expression2   Expression1Rest '''
  if(len(p) == 2):
    p[0] = p[1]
  else:
    if(p[1]['Type'] == 'boolean'):
      p[0] = {'Type' : p[2]['Type'], 'Value': ConditionalExpression(p[1], p[2]['IfTrue'], p[2]['IfFalse'])}
    else:
      errorReport(message='Error : ' + 'Type Mismatch: expected "boolean"'  + ' but found "' + p[1]['Type'] + '"' )

  
def p_Expression1Rest(p):
  '''Expression1Rest : EXPLAMETARY Expression COLON Expression1'''
  if(p[2]['Type'] == p[4]['Type']):
    p[0] = {'Type': p[2]['Type'], 'IfTrue': p[2], 'IfFalse': p[4]}
  else:
    errorReport(message='Error at line no ' + str(p.lineno(1)) + ', Type Mismatch: expected "' + p[2]['Type'] + '"' + ' but found "' + p[4]['Type'] + '"')

def p_Expression2(p) :
  '''Expression2 : Expression3
                 | Expression3 Expression2Rest '''
  
  while(operatorStack.isNotEmpty()):
    if(operatorStack.top() in arithOp):
        if((operandStack.top()['Type'] in ['float', 'double']) and (operandStack.nthFromTop(2)['Type'] in ['int', 'long', 'float', 'double'])):
          operandStack.push({'Type': operandStack.top()['Type'], 'Value': BinaryExpression(operandStack.pop(), operatorStack.pop(), operandStack.pop())})
        elif((operandStack.top()['Type'] in ['int', 'long', 'float', 'double']) and (operandStack.nthFromTop(2)['Type'] in ['float', 'double'])):
          operandStack.push({'Type': operandStack.nthFromTop(2)['Type'], 'Value': BinaryExpression(operandStack.pop(), operatorStack.pop(), operandStack.pop())})
        elif((operandStack.top()['Type'] == operandStack.nthFromTop(2)['Type']) and (operandStack.top()['Type'] in ['int', 'long', 'float', 'double']) ):
          operandStack.push({'Type': operandStack.top()['Type'], 'Value': BinaryExpression(operandStack.pop(), operatorStack.pop(), operandStack.pop())})
        else:
          errorReport('Error:' + str(p.lineno(1))+ ', Type Mismatch')
    elif(operatorStack.top() in compOp):
        if(operandStack.top()['Type'] == operandStack.nthFromTop(2)['Type']):
          operandStack.push({'Type': 'boolean', 'Value': BinaryExpression(operandStack.pop(), operatorStack.pop(), operandStack.pop())})
        else:
          errorReport('Error: ' + str(p.lineno(1)) +', Error: cannot perform comparision on different types')
  p[0] = operandStack.pop()
  

  
def p_infixOp_expression3(p):
  ''' infixOp_expression3 : InfixOp Expression3 infixOp_expression3
                          | '''

  
def p_Expression2Rest(p):
  '''Expression2Rest : InfixOp Expression3 infixOp_expression3
                     | INSTANCEOF Type'''    

  
def p_InfixOp(p):
  '''InfixOp : OR 
             | AND
             | POWER
             | EQUAL
             | NOT_EQUAL
             | LT
             | GT
             | LE
             | GE
             | L_SHIFT
             | R_SHIFT
             | RR_SHIFT
             | PLUS
             | MINUS
             | TIMES
             | DIVIDE
             | MOD'''
  p[0] = p[1]
  if(operatorStack.isEmpty()):
    operatorStack.push(p[0])
  else:
    while(priority[operatorStack.top()] >= priority[p[0]]):
      if(operatorStack.top() in arithOp):
        if((operandStack.top()['Type'] in ['float', 'double']) and (operandStack.nthFromTop(2)['Type'] in ['int', 'long', 'float', 'double'])):
          operandStack.push({'Type': operandStack.top()['Type'], 'Value': BinaryExpression(operandStack.pop(), operatorStack.pop(), operandStack.pop())})
        elif((operandStack.top()['Type'] in ['int', 'long', 'float', 'double']) and (operandStack.nthFromTop(2)['Type'] in ['float', 'double'])):
          operandStack.push({'Type': operandStack.nthFromTop(2)['Type'], 'Value': BinaryExpression(operandStack.pop(), operatorStack.pop(), operandStack.pop())})
        elif((operandStack.top()['Type'] == operandStack.nthFromTop(2)['Type']) and (operandStack.top()['Type'] in ['int', 'long', 'float', 'double']) ):
          operandStack.push({'Type': operandStack.top()['Type'], 'Value': BinaryExpression(operandStack.pop(), operatorStack.pop(), operandStack.pop())})
        else:
          errorReport('Error at line no ' + str(p.lineno(1))+', Type Mismatch')
      elif(operatorStack.top() in compOp):
        if(operandStack.top()['Type'] == operandStack.nthFromTop(2)['Type']):
          operandStack.push({'Type': 'boolean', 'Value': BinaryExpression(operandStack.pop(), operatorStack.pop(), operandStack.pop())})
        else:
          errorReport('Error at line no ' + str(p.lineno(1))+', cannot perform comparision on different types')
      
      if(operatorStack.isEmpty()):
        break
    operatorStack.push(p[0])

def p_PostfixOpList(p): 
  ''' PostfixOpList : PostfixOp PostfixOpList 
                | '''
  if(len(p)==3):
    p[0] = [p[1]] + p[2]
  else:
    p[0] = []
  
def p_Expression3(p):
  '''Expression3 : PrefixOp Expression3
                 | L_BRACE  Expression R_BRACE  Expression3
                 | L_BRACE  Type R_BRACE  Expression3
                 | Primary  DOT QualifiedIdentifier  PostfixOpList 
                 | Primary PostfixOpList  '''
  if(len(p) == 3):
    if(type(p[2]) is dict):
      if(len(p[1]) == 0):
        p[0] = p[2]
      else:
        p[0] = {'Type': p[2]['Type'], 'Value': UnaryExpression(p[1], p[2])}
    else:
      if(len(p[2]) == 0):
        p[0] = p[1]
      else:
        p[0] = {'Type': p[1]['Type'], 'Value': UnaryExpression(p[2], p[1])}
  elif(len(p) == 5):
    p[0] = {'Type': p[2], 'Value': p[4]}
  operandStack.push(p[0])
  
def p_PrefixOp(p):
  '''PrefixOp : PLUS_PLUS
              | MINUS_MINUS
              | NOT
              | CURL_DASH
              | PLUS
              | MINUS'''
  p[0] = p[1]
  
def p_PostfixOp(p):
  '''PostfixOp : PLUS_PLUS
               | MINUS_MINUS'''
  p[0] = p[1]
  
def p_Primary(p):
  '''Primary : Literal
             | ParExpression
             | THIS
             | THIS Arguments 
             | SUPER SuperSuffix 
             | QualifiedIdentifier 
             | QualifiedIdentifier IdentifierSuffix
             | BasicType SquareBraceList DOT CLASS
             | VOID DOT CLASS'''
  if(len(p) == 2):
    p[0] = p[1]

  
def p_Literal(p):
  '''Literal : LITERAL
             | NUMINT
             | NUMFLOAT
             | TRUE
             | FALSE'''
  if(p[1] in ['True', 'False']):
    p[0] = {'Type': 'boolean', 'Value': Leaf('KEYWORD', p[1])} 
  elif(type(p[1]) is int):
    p[0] = {'Type': 'int', 'Value': Leaf('LITERAL', p[1])}
  elif(type(p[1]) is float):
    p[0] = {'Type': 'float', 'Value': Leaf('LITERAL', p[1])}
  else:
    p[0] = {'Type': 'String', 'Value': Leaf('LITERAL', p[1])}
  
def p_ParExpression(p):
  '''ParExpression : L_BRACE Expression R_BRACE'''
  p[0] = p[2]
  
def p_ExpressionList(p):
  '''ExpressionList : Expression
                    | Expression COMMA ExpressionList   '''
  
def p_Arguments(p):
  '''Arguments :  L_BRACE ExpressionList L_BRACE '''
  
def p_SuperSuffix(p):
  '''SuperSuffix : Arguments 
                 | DOT IDENTIFIER   Arguments '''
  
def p_IdentifierSuffix(p):
  '''IdentifierSuffix : L_BRACE  SquareBraceList DOT CLASS R_BRACE
                      | L_BRACE  SquareBraceList DOT Expression R_BRACE
                      | Arguments 
                      | DOT  CLASS    
                      | DOT  THIS  
                      | DOT  SUPER Arguments '''
  

def p_error(p):
    print("Syntax error at line: " + str(p.lineno))

def errorReport(message):
  print message
  exit()