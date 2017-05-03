class CodeGen:

	def __init__(self, symTabs, tac, temps):
		self._mipsCode = []
		self._symTabs = symTabs
		self._tac = tac
		self._temps = {}
		self._baseOffset = 0
		self._preOff = 0
		for i in range(0, len(temps)):
			self._temps[temps[i]] = "$s" + str(i)
		self._regs = []
		self._tempRegs = {
						"$t0": True,
						"$t1": True,
						"$t2": True,
						"$t3": True,
						"$t4": True,
						"$t5": True,
						"$t6": True,
						"$t7": True,
						"$t8": True,
						"$s3": True,
						"$s4": True

					}
		self._argRegs = {
						"$a0": True,
						"$a1": True,
						"$a2": True,
						"$a3": True
					}

		self.retRegs = {
						"$v0" : True,
						"&v1" : True
					}

	def getMipsCode(self):
		return self._mipsCode

	def getMipsFile(self, filename):
		file = open(filename,"a")
		for instr in self.getMipsCode():
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
						file.write(str(a) + " ")
				else:
					file.write(str(a) + " ")
			file.write("\n")

	def addInstr(self, instr):
		self._mipsCode.append(instr)

	def getMethods(self):
		methods = []
		for tab in self._symTabs:
			methods.append(tab.getName())
		methods.remove("Global")
		return methods

	def getLocVars(self, func):
		locvars = []
		for tab in self._symTabs:
			if tab.getName() == func :
				locvars = tab.getLocVars()
				break
		return locvars

	def getGlobVars(self):
		globVars = []
		for tab in self._symTabs:
			if tab.getName() == "Global" :
				globVars = tab.getGlobVars()
				for m in self.getMethods():
					globVars.remove(m)
		return globVars


	def getVarSize(self, var, func):
		for tab in self._symTabs:
			if tab.getName() == func:
				return tab.getVarSize(var)

	def getOffsetLoc(self, var, func):
		for tab in self._symTabs:
			if tab.getName() == func:
				return tab.getOffsetLoc(var)

	def getOffsetParam(self, var, func):
		for tab in self._symTabs:
			if tab.getName() == func:
				return tab.getOffsetParam(var)

	def addOffsetLocs(self, offset, func):
		for tab in self._symTabs:
			if tab.getName() == func:
				tab.addOffsetLocs(offset)
				break

	def addOffsetParams(self, offset, func):
		for tab in self._symTabs:
			if tab.getName() == func:
				tab.addOffsetParams(offset)
				break



	def getParams(self, func):
		for tab in self._symTabs:
			if tab.getName() == func:
				return tab.getParams()

	def addOffsetParams(self, offset, func):
		for tab in self._symTabs:
			if tab.getName() == func:
				tab.addOffsetParams(offset)

	def getTempReg(self):
		for r in self._tempRegs:
			if self._tempRegs[r]:
				self._tempRegs[r] = False
				return r

	def resetTempReg(self, r):
		self._tempRegs[r] = True

	def getArgReg(self):
		for r in self._argRegs:
			if self._argRegs[r]:
				self._argRegs[r] = False
				return r

	def setArgReg(self, a):
		self._argRegs[a] = False

	def resetArgReg(self, a):
		self._argRegs[a] = True

	def resetAllArgReg(self):
		self._argRegs["$a0"] = True
		self._argRegs["$a1"] = True
		self._argRegs["$a2"] = True
		self._argRegs["$a3"] = True



	def getRetReg(self):
		for r in self._retRegs:
			if self._retRegs[r]:
				self._retRegs[r] = False
				return r

	def resetRetReg(self, r):
		self._retRegs[r] = True

	def getSpaceForLocs(self, func):
		for tab in self._symTabs:
			if tab.getName() == func:
				return tab.getSpaceForLocs()

	def setInitialOffsetLocs(self, func):
		for tab in self._symTabs:
			if tab.getName() == func:
				tab.setInitialOffsetLocs()

	def setInitialOffsetParams(self, func):
		for tab in self._symTabs:
			if tab.getName() == func:
				tab.setInitialOffsetParams()


	def pushActRec(self, func):
		self.setInitialOffsetLocs(func)
		self.setInitialOffsetParams(func)
		space = -(self.getSpaceForLocs(func))
		self._preOff = self._baseOffset
		self._baseOffset = -space
		if space < 0:
			self.addInstr(["addi", "$sp", str(space)])

	def popActRec(self, func):
		if self._baseOffset > 0:
			self.addInstr(["addi", "$sp", str(self._baseOffset)])
		self._baseOffset = self._preOff

	def getMainFirst(self):
		for i in range(0, len(self._tac)):
			if self._tac[i][0] == "main":
				m = self._tac[i:len(self._tac)]
				for j in range(0, len(m)):
					self._tac.pop()
				self._tac = m + self._tac
				break

	def isFunc(self, label):
		for tab in self._symTabs:
			if tab.getName() == label:
				return True

	def load(self, reg, value, func):
		if value in self.getGlobVars():
			return ["lw", reg, value]
		elif value in self.getLocVars(func):
			offset = -(self.getOffsetLoc(value, func))
			return ["lw", reg, str(offset)+"($sp)"]
		elif value in self.getParams(func):
			offset = self.getOffsetParam(value, func) + self._baseOffset + 16
			return ["lw", reg, str(offset)+"($sp)"]
		else:
			return ["li", reg, value]

	def store(self, reg, addr, func):
		if addr in self.getGlobVars():
			return ["sw", reg, addr]
		elif addr in self.getLocVars(func):
			offset = -(self.getOffsetLoc(addr, func))
			return ["sw", reg, str(offset) + "($sp)"]
		elif addr in self.getParams(func):
			offset = self.getOffsetParam(addr, func) + self._baseOffset + 16
			return ["sw", reg, str(offset) + "($sp)"]
		elif addr in self.getMethods():
			return ["sw", reg, "$v0"]
		elif type(addr) is str:
			return ["sw", reg, addr]






	def genMipsCode(self):
		self.addInstr([".data"])

		globs = self.getGlobVars()
		for g in globs:
			size = self.getVarSize(g, "Global")
			self.addInstr([g, ".space", size])

		self.addInstr([".text"])

		self.getMainFirst()

		func = ''
		instrNo = -1
		for instr in self._tac:
			instrNo += 1

			if(instrNo > 0):
				if(self._tac[instrNo-1][0] == "call"):
					self.addInstr(["lw", "$v0", "0($sp)"])
					#self.addInstr(["addi", "$sp", "4"])
					#self.addOffsetLocs(-4, func)
					#self._baseOffset -= 4

					
					self.addInstr(["lw", "$ra", "-4($sp)"])					
					#self.addInstr(["addi", "$sp", "4"])
					#self.addOffsetLocs(-4, func)
					#self._baseOffset -= 4
					
					self.addInstr(["lw", "$s1", "-8($sp)"])					
					#self.addInstr(["addi", "$sp", "4"])
					#self.addOffsetLocs(-4, func)
					#self._baseOffset -= 4

					self.addInstr(["lw", "$s0", "-12($sp)"])					
					#self.addInstr(["addi", "$sp", "4"])
					#self.addOffsetLocs(-4, func)
					#self._baseOffset -= 4


			if(instr[1]==":"):
				self.addInstr([instr[0], ":"])
				if(instr[0]=="main"):
					func = "main"
					self.pushActRec(func)
				elif self.isFunc(instr[0]):
					func = instr[0]
					self.pushActRec(func)
			
			elif(instr[0]=="end"):
				if(instr[1] == "main"):
					self.addInstr(["li", "$v0", "1"])
					self.addInstr(["lw", "$a0", "0($sp)"])
					self.addInstr(["syscall"])

					self.addInstr(["li", "$v0", 10])
					self.addInstr(["syscall"])
				else:
					self.popActRec(instr[1])
					self.addInstr(["jr", "$ra"])
				func = ''
			
			elif(instr[0] == "return"):
				if instr[1] in self._temps:
					self.addInstr(["sw", self._temps[instr[1]], str(self._baseOffset) + "($sp)"])
					#self.addInstr(["move", "$v0", self._temps[instr[1]]])
				else:
					t = self.getTempReg()
					self.addInstr(self.load(t, instr[1], func))
					self.addInstr(["sw", t, str(self._baseOffset) + "($sp)"])
					#self.addInstr(["move", "$v0", t])

			
			elif(instr[0]=="param"):
				if instr[1] in self._temps:
					self.addInstr(["addi", "$sp", "-4"])
					self.addInstr(self.store(self._temps[instr[1]], "0($sp)", func))
					self.addOffsetLocs(4, func)
					self._baseOffset += 4
				else:	
					t = self.getTempReg()
					self.addInstr(self.load(t, instr[1], func))
					self.addInstr(["addi", "$sp", "-4"])
					self.addInstr(self.store(t, "0($sp)", func))
					self.resetTempReg(t)
					self.addOffsetLocs(4, func)
					self._baseOffset += 4
			
			elif(instr[0] == "call"):
				

				self.addInstr(["addi", "$sp", "-4"])
				self.addInstr(["sw", "$s0", "0($sp)"])
				self.addOffsetLocs(4, func)
				self._baseOffset += 4

				self.addInstr(["addi", "$sp", "-4"])
				self.addInstr(["sw", "$s1", "0($sp)"])
				self.addOffsetLocs(4, func)
				self._baseOffset += 4

				self.addInstr(["addi", "$sp", "-4"])
				self.addInstr(["sw", "$ra", "0($sp)"])
				self.addOffsetLocs(4, func)
				self._baseOffset += 4
				
				self.addInstr(["addi", "$sp", "-4"])
				self.addInstr(["sw", "$v0", "0($sp)"])
				self.addOffsetLocs(4, func)
				self._baseOffset += 4

				self.addInstr(["jal", instr[1]])


			elif (instr[0] == "goto"):
				self.addInstr(['j', instr[1]])


			elif(len(instr)==3):
				if(instr[1] == "="):
					if instr[0] in self._temps and instr[2] in self.temps:
						self.addInstr(["move", self._temps[instr[0]], self._temps[instr[2]]])
					elif instr[0] in self._temps:
						if(self.isFunc(instr[2])):
							self.addInstr(["move", self._temps[instr[0]], "$v0"])
						else:
							self.addInstr(self.load(self._temps[instr[0]], instr[2], func))
					elif instr[2] in self._temps:
						self.addInstr(self.store(self._temps[instr[2]], instr[0], func))
					else:
						if(self.isFunc(instr[2])):
							self.addInstr(self.store("$v0", instr[0], func))
						else:
							t = self.getTempReg()
							self.addInstr(self.load(t, instr[2], func))
							self.addInstr(self.store(t, instr[0], func))
							self.resetTempReg(t)

			
			elif(instr[0] == "if"):

				op = instr[2]
				if instr[1] in self._temps and instr[3] in self._temps:
					lOperand = self._temps[instr[1]]
					rOperand = self._temps[instr[3]]
				elif instr[1] in self._temps:
					r = self.getTempReg()
					self.addInstr(self.load(r, instr[3], func))
					lOperand = self._temps[instr[1]]
					rOperand = r
					self.resetTempReg(r)

				elif instr[3] in self._temps:
					r = self.getTempReg()
					self.addInstr(self.load(r, instr[1], func))
					lOperand = r
					rOperand = self._temps[instr[3]]
					self.resetTempReg(r)
				else:
					r1 = self.getTempReg()
					r2 = self.getTempReg()
					self.addInstr(self.load(r1, instr[1], func))
					self.addInstr(self.load(r2, instr[3], func))
					lOperand = r1
					rOperand = r2


				if (op == '<'):
					self.addInstr(['blt', lOperand, rOperand, instr[5]])
					
				elif (op == '>'):
					self.addInstr(['bgt', lOperand,rOperand, instr[5]])

				elif (op == '<='):
					self.addInstr(['ble', lOperand,rOperand, instr[5]])

				elif (op == '>='):
					self.addInstr(['bge', lOperand,rOperand, instr[5]])

				elif (op == '=='):
					self.addInstr(['beq', lOperand,rOperand, instr[5]])

				elif (op == '!='):
					self.addInstr(['bne', lOperand,rOperand, instr[5]])

			elif(len(instr)==5):

				op = instr[3]
				if instr[2] in self._temps and instr[4] in self._temps:
					lOperand = self._temps[instr[2]]
					rOperand = self._temps[instr[4]]
				elif instr[2] in self._temps:
					if self.isFunc(instr[4]):
						lOperand = self._temps[instr[2]]
						rOperand = "$v0"
					else:
						t = self.getTempReg()
						self.addInstr(self.load(t, instr[4], func))
						lOperand = self._temps[instr[2]]
						rOperand = t
						self.resetTempReg(t)

				elif instr[4] in self._temps:
					if self.isFunc(instr[2]):
						lOperand = "$v0"
						rOperand = self._temps[instr[4]]
					else:
						t = self.getTempReg()
						self.addInstr(self.load(t, instr[2], func))
						lOperand = t
						rOperand = self._temps[instr[4]]
						self.resetTempReg(t)

				else:
					if self.isFunc(instr[2]) and self.isFunc(instr[4]):
						t1 = self.getTempReg()
						t2 = self.getTempReg()

						self.addInstr(["move", t1, "$v0"])
						self.addInstr(["move", t2, "$v0"])

						lOperand = t1
						rOperand = t2
						self.resetTempReg(t1)
						self.resetTempReg(t2)
					elif self.isFunc(instr[2]):
						t1 = self.getTempReg()
						t2 = self.getTempReg()

						self.addInstr(["move", t1, "$v0"])
						self.addInstr(self.load(t2, instr[4], func))

						lOperand = t1
						rOperand = t2
						self.resetTempReg(t1)
						self.resetTempReg(t2)
					elif self.isFunc(instr[4]):
						t1 = self.getTempReg()
						t2 = self.getTempReg()

						self.addInstr(self.load(t1, instr[2], func))
						self.addInstr(["move", t2, "$v0"])

						lOperand = t1
						rOperand = t2
						self.resetTempReg(t1)
						self.resetTempReg(t2)
					else:
						t1 = self.getTempReg()
						t2 = self.getTempReg()
						self.addInstr(self.load(t1, instr[2], func))
						self.addInstr(self.load(t2, instr[4], func))

						lOperand = t1
						rOperand = t2

						self.resetTempReg(t1)
						self.resetTempReg(t2)

				if (op == '+'):
					self.addInstr(["add", lOperand, lOperand, rOperand])

				elif (op == '-'):
					self.addInstr(["sub", lOperand, lOperand, rOperand])

				elif (op == '*'):
					self.addInstr(["mult", lOperand, rOperand])
					self.addInstr(["mflo", lOperand])

				elif (op == '/'):
					self.addInstr(["div", lOperand, rOperand])
					self.addInstr(["mflo", lOperand])

				if instr[0] in self._temps:
					if lOperand in self._temps:
						self.addInstr(["move", self._temps[instr[0]], self._temps[lOperand]])
					else:
						self.addInstr(["move", self._temps[instr[0]], lOperand])
				else:
					if lOperand in self._temps:
						self.addInstr(self.store(self._temps[lOperand], instr[0]))
					else:
						self.addInstr(self.store(lOperand, instr[0]))

			elif(len(instr)==4):
				pass
					

