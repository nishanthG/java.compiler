from threeAddressCode import ThreeAddressCode
tac = ThreeAddressCode()

class Program:
	def __init__(self, classDecl, next):
		self._classDecl = classDecl
		self._next = next
	def __repr__(self):
		if(self._next):
			return str(self._classDecl) + "\n" + str(next)
		else:
			return str(self._classDecl) 
	def genTac(self):
		if(self._next):
			self._classDecl.genTac()
			self._next.genTac()
		else:
			self._classDecl.genTac()
		return tac

class ClassDeclaration:
	def __init__(self, className, classBody):
		self._className = className
		self._classBody = classBody
	def __repr__(self):
		return self._className + "{ " + str(self._classBody) + " }"
	def genTac(self):
		self._classBody.genTac()

class ClassBody:
	def __init__(self, classBodyDecl, next):
		self._classBodyDecl = classBodyDecl
		self._next = next
	def __repr__(self):
		if(self._next):
			return str(self._classBodyDecl) + "\n"  + str(self._next)
		else:
			return str(self._classBodyDecl)
	def genTac(self):
		if(self._next):
			self._classBodyDecl.genTac()
			self._next.genTac()
		else:
			self._classBodyDecl.genTac()


class VariableDeclaration:
	def __init__(self, varName, varValue, next):
		self._varName = varName
		self._varValue = varValue
		self._next = next
	def __repr__(self):
		if(self._next):
			return self._varName + " = " + str(self._varValue) + ", " + str(self._next)
		else:
			return self._varName + " = " + str(self._varValue)
	def setNext(self, next):
		self._next = next
	def genTac(self):
		if(self._next):
			self._next.genTac()
			if(self._varValue):
				varValue = str(self._varValue.genTac())
				
				tac.addInstr([self._varName, '=', varValue])
		else:
			if(self._varValue):
				varValue = str(self._varValue.genTac())
				tac.addInstr([self._varName, '=', varValue])


class MethodDeclaration:
	def __init__(self, methodName, methodBody):
		self._methodName = methodName
		self._methodBody = methodBody
	def __repr__(self):
		return self._methodName + str(self._methodBody)
	def genTac(self):
		tac.addInstr([self._methodName, ":"])
		self._methodBody.genTac()
		tac.addInstr(["end", self._methodName])

class MethodBody:
	def __init__(self, parameters, block):
		self._parameters = parameters
		self._block = block
	def __repr__(self):
		return "(" + str(self._parameters) + ")" + str(self._block)
	def genTac(self):
		self._block.genTac()


class Parameters:
	def __init__(self, parName, next):
		self._parName = parName
		self._next = next
	def __repr__(self):
		if(self._next):
			return self._parName + ", " + str(self._next)
		else:
			return self._parName
		
	def getParName(self):
		return self._parName
	def getNextPar(self):
		return self._next

class MethodCall:
	def __init__(self, methodName, arguments, returnType):
		self._methodName = methodName
		self._arguments = arguments
		self._returnType = returnType

	def genTac(self):
		self._arguments.genTac()
		name = self._methodName.genTac()
		argCount = self._arguments.getCount()

		if(self._returnType == "void"):
			tac.addInstr(["call", name, str(argCount)])
		else:
			tac.addInstr(["call", name, str(argCount+1)])
			return name


class Arguments:
	def __init__(self, argument, next):
		self._argument = argument
		self._next = next

	def getCount(self):
		count = 1
		temp = self._next
		while(temp):
			count += 1
			temp = temp._next
		return count
	
	def genTac(self):
		if(self._next):
			temp = str(self._argument.genTac())
			tac.addInstr(["param", temp])
			self._next.genTac()
		else:
			temp = str(self._argument.genTac())
			tac.addInstr(["param", temp])



class Block:
	def __init__(self, statements):
		self._statements = statements
	def __repr__(self):
		return "{" + str(self._statements) + "}"
	def genTac(self):
		self._statements.genTac()

class BlockStatements:
	def __init__(self, statement, next):
		self._statement = statement
		self._next = next
	def __repr__(self):
		if(self._next):
			return str(self._statement) + "\n" + str(self._next)
		else:
			return str(self._statement)
	def genTac(self):
		if(self._next):
			self._statement.genTac()
			self._next.genTac()
		else:
			self._statement.genTac()

class ColonStatement:
	def __init__(self, identifier, statement):
		self._identifier = identifier
		self._statement = statement
	def __init__(self):
		return self._identifier + " : " + str(self._statement)

class IfStatement:
	def __init__(self, expression, statement):
		self._expression = expression
		self._statement = statement
	def __repr__(self):
		return "if(" + str(self._expression) + ")" + str(self._statement)
	
	def genTac(self):
		ltrue = tac.newLabel()
		lfalse = tac.newLabel()
		lOperand = str(self._expression._lhs.genTac())
		rOperand = str(self._expression._rhs.genTac())
		op = self._expression._operator
		
		tac.addInstr(['if', lOperand, op, rOperand, 'goto', ltrue])
		tac.addInstr(['goto', lfalse])
		tac.addInstr([ltrue, ":"])
		self._statement.genTac()
		tac.addInstr([lfalse, ":"])

class IfElseStatement:
	def __init__(self, expression, ifStatement, elseStatement):
		self._expression = expression
		self._ifStatement = ifStatement
		self._elseStatement = elseStatement
	def __repr__(self):
		return "if(" + str(self._expression) + ")" + str(self._ifStatement) + " else" + str(self._elseStatement)
	
	def genTac(self):
		ltrue = tac.newLabel()
		lfalse = tac.newLabel()
		lafter = tac.newLabel()
		lOperand =str(self._expression._lhs.genTac())
		rOperand = str(self._expression._rhs.genTac())
		op = self._expression._operator
		
		tac.addInstr(['if', lOperand, op, rOperand, 'goto', ltrue])
		tac.addInstr(["goto", lfalse])
		tac.addInstr([ltrue, ":"])
		self._ifStatement.genTac()
		tac.addInstr(["goto", lafter])
		tac.addInstr([lfalse, ":"])
		self._elseStatement.genTac()
		tac.addInstr([lafter, ":"])

class WhileLoopStatement:
	def __init__(self, expression, statement):
		self._expression = expression
		self._statement = statement
	def __repr__(self):
		return "while(" + str(self._expression) + ")" + str(self._statement)
	
	def genTac(self):
		ltrue = tac.newLabel()
		lafter = tac.newLabel()
		lbegin = tac.newLabel()
		lOperand = str(self._expression._lhs.genTac())
		rOperand = str(self._expression._rhs.genTac())
		op = self._expression._operator

		tac.addInstr([lbegin, ":"])
		tac.addInstr(['if', lOperand, op, rOperand, "goto", ltrue])
		tac.addInstr(["goto", lafter])
		tac.addInstr([ltrue, ":"])
		self._statement.genTac()
		tac.addInstr(["goto", lbegin])
		tac.addInstr([lafter, ":"])

class DoWhileLoopStatement:
	def __init__(self, statement, expression):
		self._statement = statement
		self._expression = expression


	def __repr__(self):
		return  "do " + str(self._statement) + "while(" + str(self._expression) + ")"
	def genTac(self):
		lafter = tac.newLabel()
		lbegin = tac.newLabel()
		lOperand = str(self._expression._lhs.genTac())
		rOperand = str(self._expression._rhs.genTac())
		op = self._expression._operator

		tac.addInstr([lbegin, ":"])
		self._statement.genTac()		
		tac.addInstr(['if', lOperand, op, rOperand, "goto", lbegin])
		tac.addInstr(["goto", lafter])
		tac.addInstr([lafter, ":"])
		

class ReturnStatement:
	def __init__(self, expression):
		self._expression = expression
	def __repr(self):
		return "return " + str(self._expression)

	def genTac(self):
		ret = self._expression.genTac()
		tac.addInstr(["return", ret])

class SwitchStatement:
	def __init__(self, expression, switchBlockStatementGroup):
		self._expression = expression
		self._switchBlockStatementGroup = switchBlockStatementGroup
	def __repr__(self):
		return "switch(" + str(self._expression) + "){" + str(self._switchBlockStatementGroup) + "}"

class SwitchBlockStatementGroup:
	def __init__(self, switchLabel, statement, next):
		self._switchLabel = switchLabel
		self._statement = statement
		self._next = next
	def __repr__(self):
		if(self._next):
			return "case " + str(self._switchLabel) + " : " + str(self._statement) + ", " + str(self._next)
		else:
			return "case " + str(self._switchLabel) + " : " + str(self._statement)

class ForLoopStatement:
	def __init__(self, forControl, statement):
		self._forControl = forControl
		self._statement = statement
	def __repr__(self):
		return "for(" + str(self._forControl) + ")" + str(self._statement)

	def genTac(self):
		ltrue = tac.newLabel()
		lafter = tac.newLabel()
		lbegin = tac.newLabel()
		lOperand = str(self._forControl._forCondition._lhs.genTac())
		rOperand = str(self._forControl._forCondition._rhs.genTac())
		op = self._forControl._forCondition._operator

		self._forControl._forInit.genTac()

		tac.addInstr([lbegin, ":"])
		tac.addInstr(['if', lOperand, op, rOperand, "goto", ltrue])
		tac.addInstr(["goto", lafter])
		tac.addInstr([ltrue, ":"])
		self._statement.genTac()
		self._forControl._forUpdate.genTac()
		tac.addInstr(["goto", lbegin])
		tac.addInstr([lafter, ":"])

class ForControl:
	def __init__(self, forInit, forCondition, forUpdate):
		self._forInit = forInit
		self._forCondition = forCondition
		self._forUpdate = forUpdate
	def __repr__(self):
		return str(self._forInit) + "; " + str(self._forCondition) + "; " + str(self._forUpdate)

	def setForInit(self, forInit):
		self._forInit = forInit




class ForControlColon:
	def __init__(self, forInit, expression):
		self._forInit = forInit
		self._expression = expression
	def __repr(self):
		return str(self._forInit) + " : " + str(self._expression)

class ForUpdate:
	def __init__(self, statement, next):
		self._statement = statement
		self._next = next
	def __repr__(self):
		if(self._next):
			return str(self._statement) + ", " + str(self._next)
		else:
			return str(self._statement)
	def genTac(self):
		if(self._next):
			self._statement.genTac()
			self._next.genTac()
		else:
			self._statement.genTac()

class AssignmentExpression:
	def __init__(self, rhs, operator, lhs):
		self._lhs = lhs
		self._rhs = rhs
		self._operator = operator
	def __repr__(self):
		return str(self._lhs) + self._operator + str(self._rhs)
	
	def genTac(self):
		lhs = str(self._lhs.genTac())
		rhs = str(self._rhs.genTac())
		op = self._operator 

		tac.addInstr([lhs, op, rhs])

class BinaryExpression:
	def __init__(self, rhs, operator, lhs):
		self._lhs = lhs
		self._rhs = rhs
		self._operator = operator
	def __repr__(self):
		return str(self._lhs) + self._operator + str(self._rhs)
	
	def genTac(self):
		temp = tac.newTemp()
		tac.addTemp(temp)
		lOperand = str(self._lhs.genTac())
		rOperand = str(self._rhs.genTac())
		op = self._operator

		tac.addInstr([temp, "=", lOperand, op, rOperand])		
		return temp

class UnaryExpression:
	def __init__(self, sign, operand):
		self._sign = sign
		self._operand = operand
	def __repr__(self):
		return self._sign[0] + str(self._operand)
	def genTac(self):
		temp = tac.newTemp()
		tac.addTemp(temp)
		operand = self._operand.genTac()
		sign = self._sign[0]

		tac.addInstr([temp, "=", sign, operand])
		return temp

class ConditionalExpression:
	def __init__(self, condition, ifTrue, ifFalse):
		self._condition = condition
		self._ifTrue = ifTrue
		self._ifFalse = ifFalse
	def __repr__(self):
		return str(self._condition) + "?" + str(ifTrue) + " : " + str(ifFalse) 

class Array:
	def __init__(self, name, index):
		self._name = name
		self._index = index
	def __repr__(self):
		return str(self._name) + "[" + str(self._index) + "]"
	def genTac(self):
		t = tac.newTemp()
		tac.addTemp(t)
		index = str(self._index.genTac())

		tac.addInstr([t, "=", index, "*", str(4)])
		return str(self._name._lexeme) + "[" + t + "]"

class ArrayInitializer:
	def __init__(self, item, next):
		self._item = item
		self._next = next


class Leaf():
	def __init__(self, token, lexeme):
		self._token = token
		self._lexeme = lexeme
	def __repr__(self):
		return str(self._lexeme)
	def getLexeme(self):
		return self._lexeme

	def genTac(self):		
		return self._lexeme



