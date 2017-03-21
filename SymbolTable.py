class SymbolTable:
	def __init__(self):
		self.table = []
	def insert(self, symbol):
		self.table.append(symbol)
	def lookup(self, name, scopes):
		found = False
		for i in range(len(scopes)-1, -1, -1):
			for symbol in self.table:
				if((symbol['Name'] == name) and (symbol['Scope'] == scopes[i])):
					found = True
					matchedSymbol = symbol
					break
			if(found):
				break
		if(found):
			return matchedSymbol
	def lookupCurrentScope(self, name, scope):
		found = False
		for symbol in self.table:
			if((symbol['Name'] == name) and (symbol['Scope'] == scope)):
				found = True
				matchedSymbol = symbol
				break
		if(found):
			return matchedSymbol
			

		

