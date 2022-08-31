import math
import numpy
import reqkParser
import reqkLexer

numbers = '0123456789'

class Interpreter:
	def __init__(self, postfix_expression):
		self.p_expr = postfix_expression
		self.left  = 0
		self.right = 0

	def op_TYPECAST_FLOAT(self):
		return float(self.right)

	def op_TYPECAST_INT(self):	
		return int(self.right)

	def op_FACT(self):
		return math.factorial(self.left)

	def op_EXPO(self):
		return self.left ** self.right

	def op_DIV(self):
		if self.right == 0:
			return 0
		return self.left / self.right

	def op_MUL(self):
		return self.left * self.right

	def op_PLUS(self):
		return self.left + self.right

	def op_MINUS(self):
		return self.left - self.right

	def op_ROUND_NEAR(self):
		return numpy.rint(self.right)

	def generate(self):
		stack = []
		op_func_table = {
			'TYPECAST_FLOAT':self.op_TYPECAST_FLOAT,
			'TYPECAST_INT': self.op_TYPECAST_INT,
			'FACT'       : self.op_FACT,
			'EXPO'       : self.op_EXPO,
			'DIV'        : self.op_DIV,
			'MUL'        : self.op_MUL,
			'PLUS'       : self.op_PLUS,
			'MINUS'      : self.op_MINUS,
			'ROUND_NEAR' : self.op_ROUND_NEAR
		}

		for idx, term in enumerate(self.p_expr):
			#print("IDX:",idx,"STACK:",stack)	
			if type(term) in [int, float]:
				stack.append(term)

			elif term in reqkParser.op_T:
				if term in ['FACT']:
					self.left = stack[len(stack)-1]
					stack[len(stack)-1] = op_func_table[term]()

				elif term in ['TYPECAST_INT', 'TYPECAST_FLOAT', 'ROUND_NEAR']:
					self.right = stack[len(stack)-1]
					stack[len(stack)-1] = op_func_table[term]()

				else:
					self.left  = stack[len(stack)-2]
					self.right = stack[len(stack)-1]
					#print("LEFT:",self.left,"RIGHT:",self.right)
					stack[len(stack)-2] = op_func_table[term]()
					del stack[len(stack)-1:]
		
		try:
			return stack[0]
		except:
			return reqkLexer.error("<stdin>", 0, "Couldn't complete the calculation\nTry adding brackets around terms.")
