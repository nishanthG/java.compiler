class BinaryExpression:
	def __init__(self, lhs, operator, rhs):
		self.lhs = lhs
		self.rhs = rhs
		self.operator = operator
	def __str__(self):
		return str([self.lhs, self.operator, self.rhs])

class UnaryExpression:
	def __init__(self, sign, operand):
		self.sign = sign
		self.operand = operand
	def __str__(self):
		return str([self.sign, self.operand])

class ConditionalExpression:
	def __init__(self, condition, ifTrue, ifFalse):
		self.condition = condition
		self.ifTrue = ifTrue
		self.ifFalse = ifFalse
	def __str__(self):
		return str([self.condition, self.ifTrue, self.ifFalse])

class Leaf():
	def __init__(self, token, lexeme):
		self.token = token
		self.lexeme = lexeme
	def __str__(self):
		return str([self.token, self.lexeme, self.type])

