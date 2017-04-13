class SymbolTable:
	def __init__(self, parent):
		self.parent = parent
		self.table = []

	def insert(self, symbol):
		self.table.append(symbol)
		
	def lookup(self, name):
		if(self.lookupScope(name)):
			return self.lookupScope(name)
		elif(self.parent):
			return self.parent.lookup(name)

	def lookupScope(self, name):
		for symbol in self.table:
			if(symbol['Name'] == name):
				return symbol


		

