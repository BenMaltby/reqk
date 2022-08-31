import math
import reqkMathLexer

class Interpreter:
	def __init__(self, op_tokens, lex_tokens):
		self.op_tokens  = op_tokens
		self.lex_tokens = lex_tokens
		self.left  = 0
		self.right = 0

	def op_FACT(self):
		return math.factorial(self.left)

	def op_EXPO(self):
		return self.left ** self.right
	
	def op_DIV(self):
		if self.right == 0:
			return 0
		return self.left / self.right

	def op_MUL(self):
		if type(self.left) | type(self.right) == float:
			return float(self.left * self.right)
		return int(self.left * self.right)

	def op_PLUS(self):
		return self.left + self.right

	def op_MINUS(self):
		return self.left - self.right

	def operation_index(self, search):

		for i in range(len(self.lex_tokens)):
			if search[1] == self.lex_tokens[i][0].idx:
				return i

		return 'THIS HAS FAILED!!!!'

	def generate(self):
		terms = []
		op_func_table = {
			'self.op_FACT' : self.op_FACT,
			'self.op_EXPO' : self.op_EXPO,
			'self.op_DIV'  :  self.op_DIV,
			'self.op_MUL'  :  self.op_MUL,
			'self.op_PLUS' : self.op_PLUS,
			'self.op_MINUS':self.op_MINUS,
		}

		for idx, operation in enumerate(self.op_tokens):

			if operation[0] == 'FACT':
				op_index = self.operation_index(operation)
				try:
					self.left  = self.lex_tokens[op_index-1][0].value
				except IndexError:
					return reqkMathLexer.error('<stdin>', 0, "list index out of range")
				op_function = f'self.op_{operation[0]}'

				terms.append([reqkMathLexer.Token('NUM', op_func_table[op_function](), 1, 1)])

				self.lex_tokens[op_index-1] = terms[len(terms)-1]
				del self.lex_tokens[op_index]


			elif operation[0] in ['LPAREN', 'RPAREN']:
				continue

			else:
				op_index = self.operation_index(operation)
				try:
					self.left  = self.lex_tokens[op_index-1][0].value
					self.right = self.lex_tokens[op_index+1][0].value
				except IndexError:
					return reqkMathLexer.error('<stdin>', 0, "list index out of range")
				op_function = f'self.op_{operation[0]}'

				terms.append([reqkMathLexer.Token('NUM', op_func_table[op_function](), 1, 1)])

				self.lex_tokens[op_index-1] = terms[len(terms)-1]
				del self.lex_tokens[op_index:op_index+2]

		return self.lex_tokens[0][0].value
