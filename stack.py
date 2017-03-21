class Stack:
	def __init__(self):
		self.S = []

	def isEmpty(self):
		return self.S == []
	def isNotEmpty(self):
		return self.S != []

	def push(self, a):
		self.S.append(a)

	def pop(self):
		if (self.S != []):
			return self.S.pop()
		else:
			print 'Stack is empty'

	def top(self):
		if (self.S != []):
			return self.S[len(self.S)-1]
		else:
			print 'Stack is empty'
	def empty(self):
		while(len(self.S)>0):
			self.S.pop()
	def nthFromTop(self, n):
		if (self.S != []):
			return self.S[len(self.S)-n]
		else:
			print 'Stack is empty'

