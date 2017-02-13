import ply.yacc as yacc
from lexer import tokens


nodes = []
def p_CompilationUnit(p):
  '''CompilationUnit : PACKAGE QualifiedIdentifier SEMICOLON importDeclaration typeDeclaration 
                     | importDeclaration typeDeclaration'''
  if(len(p)==6):
    p[0] = [p[1],p[2],p[3],p[4],p[5]]
  else:
    p[0] = [p[1],p[2]]
  nodes.append({'left':'CompilationUnit','right':p[0]})

def p_importDeclaration(p):
  '''importDeclaration : ImportDeclaration importDeclaration
                       |  '''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = 'Empty'
  nodes.append({'left' : 'importDeclaration', 'right' : p[0]})

def p_typeDeclaration(p):
  '''typeDeclaration : TypeDeclaration typeDeclaration
                     |  '''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = 'Empty'
  nodes.append({'left' : 'typeDeclaration', 'right' : p[0]})

def p_QualifiedIdentifier(p):
  '''QualifiedIdentifier : IDENTIFIER    
                         | IDENTIFIER DOT QualifiedIdentifier '''
  if(len(p) == 2):
    p[0] = p[1]
  else: 
    p[0] = [p[1],p[2],p[3]]
  nodes.append({'left' : 'QualifiedIdentifier', 'right' : p[0]})

def p_QualifiedIdentifierList(p): 
  '''QualifiedIdentifierList : QualifiedIdentifier   
                             | QualifiedIdentifier COMMA QualifiedIdentifierList   '''
  if(len(p) == 2):
    p[0] = p[1]
  else: 
    p[0] = [p[1],p[2],p[3]] 
  nodes.append({'left':'QualifiedIdentifierList','right':p[0]})   

def p_ImportDeclaration(p):
  '''ImportDeclaration : IMPORT QualifiedIdentifier DOT_STAR SEMICOLON 
                       | IMPORT QualifiedIdentifier SEMICOLON
                       | IMPORT STATIC QualifiedIdentifier SEMICOLON
                       | IMPORT STATIC QualifiedIdentifier DOT_STAR SEMICOLON'''
  if(len(p) == 4 ):
    p[0] = [p[1], p[2], p[3]]  

  elif(len(p) == 6 ):
    p[0] = [p[1], p[2], p[3], p[4], p[5]]
    
  elif(len(p) == 5 ):
    p[0] = [p[1], p[2], p[3], p[4]]
    
  elif(len(p) == 7 ):
    p[0] = [p[1], p[2], p[3], p[4], p[5], p[6]]
  nodes.append({'left' : 'ImportDeclaration', 'right' : p[0]})

def p_TypeDeclaration(p):
  '''TypeDeclaration : ClassOrInterfaceDeclaration
                     | SEMICOLON '''
  p[0] = p[1]
  nodes.append({'left':'TypeDeclaration','right':p[0]})

def p_ClassOrInterfaceDeclaration(p):
  '''ClassOrInterfaceDeclaration : modifier ClassDeclaration '''
  p[0] = [p[1], p[2]]
  nodes.append({'left':'ClassOrInterfaceDeclaration','right':p[0]})

def p_ClassDeclaration(p): 
  '''ClassDeclaration : NormalClassDeclaration'''
  p[0] = p[1]
  nodes.append({'left':'ClassDeclaration','right':p[0]})


def p_NormalClassDeclaration(p): 
  '''NormalClassDeclaration : CLASS IDENTIFIER ClassBody
                            | CLASS IDENTIFIER  EXTENDS Type  ClassBody
                            | CLASS IDENTIFIER  IMPLEMENTS TypeList  ClassBody
                            | CLASS IDENTIFIER  EXTENDS Type IMPLEMENTS TypeList  ClassBody'''
  if(len(p) == 4):
    p[0] = [p[1],p[2],p[3]]
  elif(len(p) == 6):
    p[0] = [p[1],p[2],p[3], p[4], p[5]]
  elif(len(p) == 8):
    p[0] = [p[1],p[2],p[3], p[4], p[5], p[6], p[7]]

  nodes.append({'left':'NormalClassDeclaration','right':p[0]})



def p_square_brace(p):
  '''square_brace : 
                  | L_SQUARE_BRACE R_SQUARE_BRACE square_brace'''
  if(len(p) == 4):
    p[0] = [p[1],p[2], p[3]]
  else:
    p[0] = 'Empty'

  nodes.append({'left':'square_brace','right':p[0]})

def p_modifier(p):
  ''' modifier : Modifier modifier
               |  '''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = 'Empty'
  nodes.append({'left':'modifier','right':p[0]})

def p_Type(p): 
  '''Type : BasicType square_brace
          | QualifiedIdentifier square_brace''' 
  p[0] = [p[1],p[2]]
  nodes.append({'left':'Type','right':p[0]})

def p_BasicType(p):
  '''BasicType : BYTE
               | SHORT
               | CHAR
               | INT
               | LONG
               | FLOAT
               | DOUBLE
               | BOOLEAN'''
  p[0] = p[1]
  nodes.append({'left':'BasicType','right':p[0]})

def p_TypeList(p):
  '''TypeList : QualifiedIdentifier  
              | QualifiedIdentifier COMMA TypeList   '''
  if(len(p) == 4):
    p[0] = [p[1],p[2], p[3]]
  else:
    p[0] = p[1]
  nodes.append({'left':'TypeList','right':p[0]})

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
  nodes.append({'left':'Modifier','right':p[0]})


def p_ClassBody(p):
  '''ClassBody : L_CURL_BRACE classBodyDeclaration R_CURL_BRACE '''
  p[0] = [p[1], p[2], p[3]]
  nodes.append({'left':'ClassBody','right':p[0]})


def p_classBodyDeclaration(p):
  ''' classBodyDeclaration : ClassBodyDeclaration classBodyDeclaration
                           |  '''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = 'Empty'
  nodes.append({'left':'classBodyDeclaration','right':p[0]})

def p_ClassBodyDeclaration(p):
  '''ClassBodyDeclaration : SEMICOLON 
                          | modifier MemberDecl 
                          | STATIC  Block
                          | Block'''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = p[1]
  nodes.append({'left':'ClassBodyDeclaration','right':p[0]})

def p_MemberDecl(p):
  '''MemberDecl : MethodOrFieldDecl
                | VOID IDENTIFIER VoidMethodDeclaratorRest
                | ClassDeclaration'''
  if(len(p) == 4):
    p[0] = [p[1],p[2], p[3]]
  else:
    p[0] = p[1]
  nodes.append({'left':'MemberDecl','right':p[0]})

def p_MethodOrFieldDecl(p):
  '''MethodOrFieldDecl : Type IDENTIFIER MethodOrFieldRest'''
  p[0] = [p[1], p[2], p[3]]
  nodes.append({'left':'MethodOrFieldDecl','right':p[0]})

def p_MethodOrFieldRest(p):
  '''MethodOrFieldRest : FieldDeclaratorsRest SEMICOLON
                       | MethodDeclaratorRest'''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = p[1]
  nodes.append({'left':'MethodOrFieldRest','right':p[0]})

def p_variableDeclarator(p):
  '''variableDeclarator : COMMA VariableDeclarator variableDeclarator
                        |  '''
  if(len(p) == 4):
    p[0] = [p[1],p[2], p[3]]
  else:
    p[0] = 'Empty'
  nodes.append({'left':'variableDeclarator','right':p[0]})

def p_FieldDeclaratorsRest(p):
  '''FieldDeclaratorsRest : VariableDeclaratorRest variableDeclarator '''
  p[0] = [p[1], p[2]]
  nodes.append({'left':'FieldDeclaratorsRest','right':p[0]})

def p_MethodDeclaratorRest(p):
  '''MethodDeclaratorRest : FormalParameters Block
                          | FormalParameters SEMICOLON
                          | FormalParameters THROWS QualifiedIdentifierList Block 
                          | FormalParameters THROWS QualifiedIdentifierList SEMICOLON '''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = [p[1], p[2], p[3], p[4]]
  nodes.append({'left':'MethodDeclaratorRest','right':p[0]})

def p_VoidMethodDeclaratorRest(p):
  '''VoidMethodDeclaratorRest : FormalParameters Block 
                              | FormalParameters SEMICOLON  
                              | FormalParameters THROWS QualifiedIdentifierList Block
                              | FormalParameters THROWS QualifiedIdentifierList SEMICOLON '''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = [p[1], p[2], p[3], p[4]]
  nodes.append({'left':'VoidMethodDeclaratorRest','right':p[0]})

def p_FormalParameters(p):
  '''FormalParameters : L_BRACE R_BRACE
                      | L_BRACE FormalParameterDecls R_BRACE '''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = [p[1], p[2], p[3]]
  nodes.append({'left':'FormalParameters','right':p[0]})

def p_variableModifier(p):
  ''' variableModifier : 
                       | FINAL variableModifier '''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = 'Empty'
  nodes.append({'left':'variableModifier','right':p[0]})

def p_FormalParameterDecls(p):
  '''FormalParameterDecls : Type FormalParameterDeclsRest
                          | variableModifier Type FormalParameterDeclsRest'''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = [p[1], p[2], p[3]]
  nodes.append({'left':'FormalParameterDecls','right':p[0]})

def p_FormalParameterDeclsRest(p):
  '''FormalParameterDeclsRest : VariableDeclaratorId 
                              | VariableDeclaratorId COMMA FormalParameterDecls 
                              | DOT DOT DOT VariableDeclaratorId'''
  if(len(p) == 5):
    p[0] = [p[1],p[2], p[3], p[4]]
  elif(len(p) == 4):
    p[0] = [p[1], p[2], p[3]]
  else:
    p[0] = p[1]
  nodes.append({'left':'FormalParameterDeclsRest','right':p[0]})


def p_VariableDeclaratorId(p):
  '''VariableDeclaratorId : IDENTIFIER square_brace '''
  p[0] = [p[1], p[2]]
  nodes.append({'left':'VariableDeclaratorId','right':p[0]})


def p_VariableDeclarators(p):
  '''VariableDeclarators : VariableDeclarator
                         | VariableDeclarator COMMA VariableDeclarators   '''
  if(len(p) == 4):
    p[0] = [p[1],p[2], p[3]]
  else:
    p[0] = p[1]
  nodes.append({'left':'VariableDeclarators','right':p[0]})

def p_VariableDeclarator(p):
  '''VariableDeclarator : IDENTIFIER VariableDeclaratorRest'''
  p[0] = [p[1], p[2]]
  nodes.append({'left':'VariableDeclarator','right':p[0]})

def p_VariableDeclaratorRest(p):
  '''VariableDeclaratorRest : square_brace  
                            | square_brace ASSIGNMENT VariableInitializer  '''
  if(len(p) == 2):
    p[0] = p[1]
  else:
    p[0] = [p[1], p[2], p[3]]
  nodes.append({'left':'VariableDeclaratorRest','right':p[0]})

def p_VariableInitializer(p):
  '''VariableInitializer : ArrayInitializer
                         | Expression'''
  p[0] = p[1]
  nodes.append({'left':'VariableInitializer','right':p[0]})

def p_variableInitializer(p):
  ''' variableInitializer : VariableInitializer
                          | VariableInitializer COMMA variableInitializer '''
  if(len(p) == 2):
    p[0] = p[1]
  else:
    p[0] = [p[1], p[2], p[3]]
  nodes.append({'left':'variableInitializer','right':p[0]})
                     
def p_ArrayInitializer(p):
  ''' ArrayInitializer : L_SQUARE_BRACE variableInitializer R_SQUARE_BRACE 
                       | L_SQUARE_BRACE variableInitializer R_SQUARE_BRACE COMMA '''
  if(len(p) == 4):
    p[0] = [p[1],p[2], p[3]]
  else:
    p[0] = [p[1], p[2], p[3], p[4]]
  nodes.append({'left':'ArrayInitializer','right':p[0]})

def p_Block(p):
  '''Block : L_CURL_BRACE  BlockStatements R_CURL_BRACE'''
  p[0] = [p[1], p[2], p[3]]
  nodes.append({'left':'Block','right':p[0]})

def p_BlockStatements(p):
  '''BlockStatements : BlockStatement BlockStatements 
                     | '''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = 'Empty'
  nodes.append({'left':'BlockStatements','right':p[0]})

def p_BlockStatement(p):
  '''BlockStatement : LocalVariableDeclarationStatement
                    | ClassOrInterfaceDeclaration
                    | Statement
                    | IDENTIFIER COLON  Statement'''
  if(len(p) == 2):
    p[0] = p[1]
  else:
    p[0] = [p[1], p[2], p[3]]
  nodes.append({'left':'BlockStatement','right':p[0]})

def p_LocalVariableDeclarationStatement(p):
  '''LocalVariableDeclarationStatement : Type VariableDeclarators SEMICOLON
                                       | variableModifier Type VariableDeclarators SEMICOLON'''
  if(len(p) == 4):
    p[0] = [p[1],p[2], p[3]]
  else:
    p[0] = [p[1], p[2], p[3], p[4]]
  nodes.append({'left':'LocalVariableDeclarationStatement','right':p[0]})

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
  if(len(p) == 6 ):
    p[0] = [p[1], p[2], p[3], p[4], p[5]]  
  elif(len(p) == 4 ):
    p[0] = [p[1], p[2], p[3]]
  elif(len(p) == 3 ):
    p[0] = [p[1], p[2]]
  elif(len(p) == 2 ):
    p[0] = p[1] 
  nodes.append({'left':'Statement','right':p[0]})        
             

def p_StatementExpression(p):
  '''StatementExpression : Expression'''
  p[0] = p[1]
  nodes.append({'left':'StatementExpression','right':p[0]})

def p_SwitchBlockStatementGroups(p):
  '''SwitchBlockStatementGroups : SwitchBlockStatementGroup SwitchBlockStatementGroups
                                |  '''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = 'Empty'
  nodes.append({'left':'SwitchBlockStatementGroups','right':p[0]})

def p_SwitchBlockStatementGroup(p):
  '''SwitchBlockStatementGroup : SwitchLabels BlockStatements'''
  p[0] = [p[1], p[2]]
  nodes.append({'left':'SwitchBlockStatementGroup','right':p[0]})

def p_SwitchLabels(p):
  '''SwitchLabels : SwitchLabel
                  | SwitchLabel  SwitchLabels'''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = p[1]
  nodes.append({'left':'SwitchLabels','right':p[0]})

def p_SwitchLabel(p):
  '''SwitchLabel : CASE Expression COLON
                 | DEFAULT COLON'''
  if(len(p) == 4):
    p[0] = [p[1],p[2], p[3]]
  else:
    p[0] = [p[1], p[2]]
  nodes.append({'left':'SwitchLabel','right':p[0]})



def p_ForControl(p):
  '''ForControl : ForVarControl
                | ForUpdate SEMICOLON SEMICOLON 
                | ForUpdate SEMICOLON   Expression  SEMICOLON   
                | ForUpdate SEMICOLON   SEMICOLON   ForUpdate
                | ForUpdate SEMICOLON   Expression  SEMICOLON   ForUpdate '''
  if(len(p) == 6 ):
    p[0] = [p[1], p[2], p[3], p[4], p[5]]  
  elif(len(p) == 5 ):
    p[0] = [p[1], p[2], p[3], p[4]]  
  elif(len(p) == 4 ):
    p[0] = [p[1], p[2], p[3]]
  elif(len(p) == 2 ):
    p[0] = p[1]   
  nodes.append({'left':'ForControl','right':p[0]})

def p_ForVarControl(p):
  '''ForVarControl :  Type VariableDeclaratorId  ForVarControlRest
                   |  variableModifier   Type VariableDeclaratorId  ForVarControlRest'''
  if(len(p) == 4 ):
    p[0] = [p[1], p[2], p[3]]
    
  elif(len(p) == 3 ):
    p[0] = [p[1], p[2]]
  nodes.append({'left':'ForVarControl','right':p[0]})

def p_ForVarControlRest(p): 
  '''ForVarControlRest : ForVariableDeclaratorsRest SEMICOLON SEMICOLON 
                       | ForVariableDeclaratorsRest SEMICOLON   Expression  SEMICOLON 
                       | ForVariableDeclaratorsRest SEMICOLON   SEMICOLON   ForUpdate
                       | ForVariableDeclaratorsRest SEMICOLON   Expression  SEMICOLON   ForUpdate 
                       | COLON Expression'''
  if(len(p) == 6 ):
    p[0] = [p[1], p[2], p[3], p[4], p[5]]  

  elif(len(p) == 5 ):
    p[0] = [p[1], p[2], p[3], p[4]]
    
  elif(len(p) == 4 ):
    p[0] = [p[1], p[2], p[3]]

  elif(len(p) == 2 ):
    p[0] = p[1]
  nodes.append({'left':'ForVarControlRest','right':p[0]})

def p_ForVariableDeclaratorsRest(p):
  '''ForVariableDeclaratorsRest : ASSIGNMENT VariableInitializer variableDeclarator  '''
  p[0] = [p[1], p[2], p[3]]
  nodes.append({'left':'ForVariableDeclaratorsRest','right':p[0]})
 

def p_ForUpdate(p):
  '''ForUpdate : StatementExpression
               | StatementExpression  COMMA ForUpdate   ''' 
  if(len(p) == 4):
    p[0] = [p[1],p[2], p[3]]
  else:
    p[0] = p[1]   
  nodes.append({'left':'ForUpdate','right':p[0]})

def p_Expression(p):
  '''Expression : Expression1
                | Expression1  AssignmentOperator Expression1'''
  if(len(p) == 4):
    p[0] = [p[1],p[2], p[3]]
  else:
    p[0] = p[1]
  nodes.append({'left':'Expression','right':p[0]})

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
  nodes.append({'left':'AssignmentOperator','right':p[0]})

def p_Expression1(p) :
  '''Expression1 : Expression2
                 | Expression2   Expression1Rest '''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = p[1]
  nodes.append({'left':'Expression1','right':p[0]})

def p_Expression1Rest(p):
  '''Expression1Rest : EXPLAMETARY Expression COLON Expression1'''
  p[0] = [p[1], p[2], p[3], p[4]]
  nodes.append({'left':'Expression1Rest','right':p[0]})

def p_Expression2(p) :
  '''Expression2 : Expression3
                 | Expression3 Expression2Rest '''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = p[1]
  nodes.append({'left':'Expression2','right':p[0]})

def p_infixOp_expression3(p):
  ''' infixOp_expression3 : InfixOp Expression3 infixOp_expression3
                          | '''
  if(len(p) == 4):
    p[0] = [p[1],p[2], p[3]]
  else:
    p[0] = 'Empty'
  nodes.append({'left':'infixOp_expression3','right':p[0]})

def p_Expression2Rest(p):
  '''Expression2Rest : InfixOp Expression3 infixOp_expression3
                     | INSTANCEOF Type'''
  if(len(p) == 4):
    p[0] = [p[1],p[2], p[3]]
  else:
    p[0] = [p[1], p[2]]
  nodes.append({'left':'Expression2Rest','right':p[0]})

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
  nodes.append({'left':'InfixOp','right':p[0]})


def p_postfixOp(p): 
  ''' postfixOp : PostfixOp postfixOp 
                | '''
  if(len(p) == 3):
    p[0] = [p[1],p[2]]
  else:
    p[0] = 'Empty'
  nodes.append({'left':'postfixOp','right':p[0]})

def p_Expression3(p):
  '''Expression3 : PrefixOp Expression3
                 | L_BRACE  Expression R_BRACE  Expression3
                 | L_BRACE  Type R_BRACE  Expression3
                 | Primary  DOT QualifiedIdentifier  postfixOp 
                 | Primary postfixOp  '''
  if(len(p) == 5):
    p[0] = [p[1],p[2], p[3], p[4]]
  else:
    p[0] = [p[1], p[2]]
  nodes.append({'left':'Expression3','right':p[0]})

def p_PrefixOp(p):
  '''PrefixOp : PLUS_PLUS
              | MINUS_MINUS
              | NOT
              | CURL_DASH
              | PLUS
              | MINUS'''
  p[0] = p[1]
  nodes.append({'left':'PrefixOp','right':p[0]})

def p_PostfixOp(p):
  '''PostfixOp : PLUS_PLUS
               | MINUS_MINUS'''
  p[0] = p[1]
  nodes.append({'left':'PostfixOp','right':p[0]})

def p_Primary(p):
  '''Primary : Literal
             | ParExpression
             | THIS
             | THIS Arguments 
             | SUPER SuperSuffix 
             | QualifiedIdentifier 
             | QualifiedIdentifier IdentifierSuffix
             | BasicType square_brace DOT CLASS
             | VOID DOT CLASS'''
  if(len(p) == 5):
    p[0] = [p[1],p[2], p[3], p[4]]
  elif(len(p) == 4):
    p[0] = [p[1], p[2], p[3]]
  elif(len(p) == 3):
    p[0] = [p[1], p[2]]
  elif(len(p) == 2):
    p[0] = p[1]
  nodes.append({'left':'Primary','right':p[0]})

def p_Literal(p):
  '''Literal : LITERAL
             | NUMBER'''
  p[0] = p[1]
  nodes.append({'left':'Literal','right':p[0]})

def p_ParExpression(p):
  '''ParExpression : L_BRACE Expression R_BRACE'''
  p[0] = [p[1], p[2], p[3]]
  nodes.append({'left':'ParExpression','right':p[0]})

def p_ExpressionList(p):
  '''ExpressionList : Expression
                    | Expression COMMA ExpressionList   '''
  if(len(p) == 4):
    p[0] = [p[1], p[2], p[3]]
  else:
    p[0] = p[1]
  nodes.append({'left':'ExpressionList','right':p[0]})

def p_Arguments(p):
  '''Arguments :  L_BRACE ExpressionList L_BRACE '''
  p[0] = [p[1], p[2], p[3]]
  nodes.append({'left':'Arguments','right':p[0]})

def p_SuperSuffix(p):
  '''SuperSuffix : Arguments 
                 | DOT IDENTIFIER   Arguments '''
  if(len(p) == 4):
    p[0] = [p[1], p[2], p[3]]
  else:
    p[0] = p[1]
  nodes.append({'left':'SuperSuffix','right':p[0]})

def p_IdentifierSuffix(p):
  '''IdentifierSuffix : L_BRACE  square_brace DOT CLASS R_BRACE
                      | L_BRACE  square_brace DOT Expression R_BRACE
                      | Arguments 
                      | DOT  CLASS    
                      | DOT  THIS  
                      | DOT  SUPER Arguments '''
  if(len(p) == 6):
    p[0] = [p[1], p[2], p[3], p[4], p[5]]
  elif(len(p) == 4):
    p[0] = [p[1], p[2], p[3]]
  elif(len(p) == 3):
    p[0] = [p[1], p[2]]
  else:
    p[0] = p[1]
  nodes.append({'left':'IdentifierSuffix','right':p[0]})


def p_error(p):
    print("Syntax error in input!")

