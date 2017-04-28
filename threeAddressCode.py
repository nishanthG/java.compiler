class ThreeAddressCode:
	def __init__(self):
		self._temp_no = -1
		self._label_no = -1
		self._file = open('3ac.text',"w+")
		self._file.close
	def gen(self, code):
		self._file = open('3ac.text',"a")
		self._file.write(code+'\n')
	def newTemp(self):
		self._temp_no += 1
		return 't'+str(self._temp_no)
	def newLabel(self):
		self._label_no += 1
		return 'L'+str(self._label_no)

