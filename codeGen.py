class CodeGen:

	def __init__(self, symTabs, tac, temps):
		self._mipsCode = []
		self._symTabs = symTabs
		self._tac = tac
		self._temps = {}
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

	def getOffset(self, var, func):
		for tab in self._symTabs:
			if tab.getName() == func:
				return tab.getOffset(var)

	def addOffset(self, offset, func):
		for tab in self._symTabs:
			if tab.getName() == func:
				tab.addOffset(offset)
				break

	def getParams(self, func):
		for tab in self._symTabs:
			if tab.getName() == func:
				return tab.getParams()

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


	def pushActRec(self, func):
		space = -(self.getSpaceForLocs(func))
		if space > 0:
			self.addInstr(["addi", "$sp", str(space)])

	def popActRec(self, func):
		space = self.getSpaceForLocs(func)
		if space > 0:
			self.addInstr(["addi", "$sp", str(space)])

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
			offset = -(self.getOffset(value, func))
			return ["lw", reg, str(offset)+"($sp)"]
		elif value in self.getParams(func):
			offset = self.getOffset(value, func)
			return ["lw", reg, str(offset)+"($sp)"]
		else:
			return ["li", reg, value]

	def store(self, reg, addr, func):
		if addr in self.getGlobVars():
			return ["sw", reg, addr]
		elif addr in self.getLocVars(func):
			offset = -(self.getOffset(addr, func))
			return ["sw", reg, str(offset) + "($sp)"]
		elif addr in self.getParams(func):
			offset = self.getOffset(addr, func)
			return ["sw", reg, str(offset) + "($sp)"]




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
		funcParReg = {}
		for instr in self._tac:
			instrNo += 1

			if(instrNo > 0):
				if(self._tac[instrNo-1][0] == "call"):
					self.addInstr(["lw", "$v0", "0($sp)"])
					self.addInstr(["addi", "$sp", "4"])

					argRegs = funcParReg[func]
					for a in reversed(argRegs):
						self.addInstr(["lw", a, "0($sp)"])
						self.addInstr(["addi", "$sp", "4"])
						self.setArgReg(a)

					self.addInstr(["lw", "$ra", "0($sp)"])					
					self.addInstr(["addi", "$sp", "4"])

					self.addInstr(["lw", "$s1", "0($sp)"])					
					self.addInstr(["addi", "$sp", "4"])

					self.addInstr(["lw", "$s0", "0($sp)"])					
					self.addInstr(["addi", "$sp", "4"])

			if(instr[1]==":"):
				if self.isFunc(instr[0]):
					func = instr[0]
					self.addInstr([instr[0], ":"])
					self.pushActRec(instr[0])

					funcParReg[func] = []
				else:
					self.addInstr([instr[0], ":"])
			
			elif(instr[0]=="end"):
				func = ''
				if(instr[1] == "main"):
					self.addInstr(["li", "$v0", "1"])
					self.addInstr(["lw", "$a0", "0($sp)"])
					self.addInstr(["syscall"])

					self.addInstr(["li", "$v0", 10])
					self.addInstr(["syscall"])
				else:
					self.popActRec(instr[1])
					self.addInstr(["jr", "$ra"])
			
			elif(instr[0] == "return"):
				if instr[1] in self._temps:
					self.addInstr(["move", "$v0", self._temps[instr[1]]])
				else:
					self.addInstr(self.load("$v0", instr[1], func))
			
			elif(instr[0]=="param"):
				reg = self.getArgReg()
				if instr[1] in self._temps:
					self.addInstr(["move", reg, self._temps[instr[1]]])
				else:
					self.addInstr(self.load(reg, instr[1], func))

				funcParReg[func].append(reg)
			
			elif(instr[0] == "call"):
				
				self.addInstr(["addi", "$sp", "-4"])
				self.addInstr(["sw", "$s0", "0($sp)"])
				
				self.addInstr(["addi", "$sp", "-4"])
				self.addInstr(["sw", "$s1", "0($sp)"])

				self.addInstr(["addi", "$sp", "-4"])
				self.addInstr(["sw", "$ra", "0($sp)"])


				self.addOffset(12, func)

				argRegs = funcParReg[func]
				for a in argRegs:
					self.addInstr(["addi", "$sp", "-4"])
					self.addInstr(["sw", a, "0($sp)"])
					self.addOffset(4, func)
					self.resetArgReg(a)
				
				self.addInstr(["addi", "$sp", "-4"])
				self.addInstr(["sw", "$v0", "0($sp)"])

				self.addOffset(4, func)

				self.addInstr(["jal", instr[1]])

			elif (instr[0] == "goto"):
				self.addInstr(['j', instr[1]])


			elif(len(instr)==3):
				if(instr[1] == "="):
					if instr[0] in self._temps and instr[2] in self.temps:
						self.addInstr(["move", self._temps[instr[0]], self._temps[instr[2]]])
					elif instr[0] in self._temps:
						if(instr[2]==func):
							self.addInstr(["move", self._temps[instr[0]], "$v0"])
						else:
							self.addInstr(self.load(self._temps[instr[0]], instr[2], func))
					elif instr[2] in self._temps:
						self.addInstr(self.store(self._temps[instr[2]], instr[0], func))
					else:
						if(instr[2]==func):
							self.addInstr(self.store("$v0", instr[0]))
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
					if instr[4] == func:
						lOperand = self._temps[instr[2]]
						rOperand = "$v0"
					else:
						t = self.getTempReg()
						self.addInstr(self.load(t, instr[4], func))
						lOperand = self._temps[instr[2]]
						rOperand = t
						self.resetTempReg(t)

				elif instr[4] in self._temps:
					if instr[2] == func:
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
					

















