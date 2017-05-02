class SymbolTable:
	def __init__(self, name, parent):
		self._name = name
		self.parent = parent
		self.table = []

	def getName(self):
		return self._name

	def getTable(self):
		return self._table

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

	def getLocVars(self):
		locVars = []
		for sym in self.table:
			if "Params" not in sym:
				locVars.append(sym["Name"])
		return locVars

	def getGlobVars(self):
		globVars = []
		for sym in self.table:
			globVars.append(sym["Name"])
		return globVars

	def getParams(self):
		params = {}
		size = 0
		for sym in self.table:
			sym["Offset"] = size
			if "Param" in sym:
				params[sym["Name"]] = sym["Type"]
				sym["Offset"] = size
				if sym["Type"] == "int":
					size += 4
				elif sym["Type"] == "float":
					size += 8
		return params


	def getSpaceForLocs(self):
		size = 0
		for sym in self.table:
			if "Param" not in sym:
				sym["Offset"] = size
				if sym["Type"] == "int":
					size += 4
				elif sym["Type"] == "float":
					size += 8
		return size

	def addOffset(self, offset):
		for sym in self.table:
			if "Params" not in sym:
				sym["Offset"] += offset

	def getOffset(self, var):
		self.getParams()
		self.getSpaceForLocs()
		for sym in self.table:
			if sym["Name"] == var:
				return sym["Offset"]

	def getVarSize(self, var):
		for sym in self.table:
			if sym["Name"] == var:
				if sym["Type"]=="int":
					return 4
				elif sym["Type"]=="float":
					return 8







		

