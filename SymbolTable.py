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
			if "Param" not in sym:
				locVars.append(sym["Name"])
		return locVars

	def getGlobVars(self):
		globVars = []
		for sym in self.table:
			globVars.append(sym["Name"])
		return globVars

	def getParams(self):
		params = {}
		for sym in self.table:
			if "Param" in sym:
				params[sym["Name"]] = sym["Type"]
		return params

	def setInitialOffsetParams(self):
		size = 0
		for sym in self.table:
			if "Param" in sym:
				sym["Offset"] = size
				if sym["Type"] == "int":
					size += 4
				elif sym["Type"] == "float":
					size += 8

	def setInitialOffsetLocs(self):
		size = 0
		for sym in self.table:
			if "Param" not in sym:
				sym["Offset"] = size
				if sym["Type"] == "int":
					size += 4
				elif sym["Type"] == "float":
					size += 8

	def getSpaceForLocs(self):
		size = 0
		for sym in self.table:
			if "Param" not in sym:
				if sym["Type"] == "int":
					size += 4
				elif sym["Type"] == "float":
					size += 8
		return size

	def addOffsetLocs(self, offset):
		for sym in self.table:
			if "Params" not in sym:
				sym["Offset"] += offset

	def addOffsetParams(self, offset):
		for sym in self.table:
			if "Param" in sym:
				sym["Offset"] += offset

	def getOffsetParam(self, par):
		for sym in self.table:
			if "Param" in sym:
				if sym["Name"] == par:
					return sym["Offset"]

	def getOffsetLoc(self, var):
		for sym in self.table:
			if "Param" not in sym:
				if sym["Name"] == var:
					return sym["Offset"]

	def getVarSize(self, var):
		for sym in self.table:
			if sym["Name"] == var:
				if sym["Type"]=="int":
					return 4
				elif sym["Type"]=="float":
					return 8







		
