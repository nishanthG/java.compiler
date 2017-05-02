
class ThreeAddressCode:
	
	def __init__(self):
		self._tac = []
		self._temps = []
		self._LastUse = {}
		self._temp_no = -1
		self._label_no = -1

	
	def newTemp(self):
		self._temp_no += 1
		return 't'+str(self._temp_no)
	
	def newLabel(self):
		self._label_no += 1
		return 'L'+str(self._label_no)
	
	def addInstr(self, instr):
		self._tac.append(instr)
	
	def getTac(self):
		return self._tac

	def getTacFile(self, filename):
		file = open(filename,"a")
		for instr in self.getTac():
			if(len(instr)==2):
				if(instr[1] != ":"):
					file.write("	")
			else:
				file.write("	")
			for a in instr:
				if(len(instr)==2):
					if(instr[1]==":"):
						file.write(a)
					else:
						file.write(a + " ")
				else:
					file.write(str(a) + " ")
			file.write("\n")

	def addTemp(self, temp):
		self._temps.append(temp)

	def getFreeTemp(self, instrNo):
		for i in range(0, instrNo+1):
			instr = self.getTac()[i]
			if instr[0] in self.getTemps():
				if(self.getLastUse(instr[0])<=instrNo):
					return instr[0]

	def deleteTemp(self, temp):
		self._temps.remove(temp)
	
	def getTemps(self):
		return self._temps

	def addLastUse(self, temp, instrNo):
		self._LastUse[temp] = instrNo

	def getLastUse(self, temp):
		return self._LastUse[temp]

	def deleteLastUse(self, temp):
		del self._LastUse[temp]

	def calcLastUse(self):
		instrNo = 0
		for instr in self.getTac():
			for i in range(0, len(instr)):
				if instr[i] in self.getTemps():
					self.addLastUse(instr[i], instrNo)
			instrNo += 1

	def replaceTempInCode(self, oldTemp, newTemp):
		for i in range(0, len(self.getTac())):
			instr = self.getTac()[i]
			for j in range(0, len(instr)):
				if instr[j] == oldTemp:
					instr[j] = newTemp


	def optimizeTac(self):
		self.calcLastUse()
		instrNo = 0
		for instr in self.getTac():
			flag = True
			if instr[0] in self.getTemps():
				for j in range(1, len(instr)):
					if instr[j] in self.getTemps():
						if self.getLastUse(instr[j]) <= instrNo:
							flag = False
							self.deleteTemp(instr[0])
							self.deleteLastUse(instr[0])
							self.replaceTempInCode(instr[0], instr[j])
							self.calcLastUse()
							break
				if(flag):
					temp = self.getFreeTemp(instrNo)
					if(temp):
						self.deleteTemp(instr[0])
						self.deleteLastUse(instr[0])
						self.replaceTempInCode(instr[0], temp)
						self.calcLastUse()
			instrNo += 1
		return self.getTac()



