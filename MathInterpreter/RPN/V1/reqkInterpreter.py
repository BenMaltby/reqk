import math
import reqkLexer
import reqkParser

numbers = '0123456789'

class Interpreter:
	def __init__(self, postfix_expression):
		self.p_expr = postfix_expression
		self.left  = 0
		self.right = 0

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

	def generate(self):
		stack = []
		op_func_table = {
			'EXPO'      : self.op_EXPO,
			'DIV'       : self.op_DIV,
			'MUL'       : self.op_MUL,
			'PLUS'      : self.op_PLUS,
			'MINUS'     : self.op_MINUS
		}

		for idx, term in enumerate(self.p_expr):
			#print("IDX:",idx,"STACK:",stack)	
			if type(term) in [int, float]:
				stack.append(term)

			elif term in reqkParser.op_T:
				self.left  = stack[len(stack)-2]
				self.right = stack[len(stack)-1]
				#print("LEFT:",self.left,"RIGHT:",self.right)
				stack[len(stack)-2] = op_func_table[term]()
				del stack[len(stack)-1:]

		return stack[0]
