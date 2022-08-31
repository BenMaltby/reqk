import math
import reqkMathLexer

numbers = '0123456789'
global_variables = {}  # will store variables

class Interpreter:
	def __init__(self, op_tokens, lex_tokens, show_stages, dev_mode):
		self.op_tokens  = op_tokens
		self.lex_tokens = lex_tokens
		self.show_stages = show_stages
		self.dev_mode = dev_mode
		self.left  = 0
		self.right = 0
		self.tag_printed = 0
	
	def op_TYPECAST(self, type):
		if type == 'INT':
			return int(self.right)
		elif type == 'FLOAT':
			return float(self.right)
		else:
			return reqkMathLexer.error("<stdin>", 0, "Unkown Cast")

	def op_FACT(self):
		return math.factorial(self.left)

	def op_PERC(self):
		return self.left * 0.01

	def op_EXPO(self):
		return self.left ** self.right
	
	def op_MODULO(self):
		return self.left % self.right

	def op_DIV_FLOOR(self):
		return self.left // self.right
	
	def op_DIV(self):
		if self.right == 0:
			return 0
		return self.left / self.right

	def op_MUL(self):
		return self.left * self.right

	def op_OR(self):
		return self.left | self.right

	def op_AND(self):
		return self.left & self.right

	def op_NOT(self):
		return ~self.right

	def op_DUB_EQUALS(self):
		return True if self.left == self.right else False
	
	def op_GT(self):
		return True if self.left > self.right else False

	def op_LT(self):
		return True if self.left < self.right else False

	def op_PLUS(self):
		return self.left + self.right

	def op_MINUS(self):
		return self.left - self.right

	def op_ROUND_NEAR(self):
		return round(self.right)
	
	def op_ROUND_UP(self):
		return math.ceil(self.right)

	def op_ROUND_DOWN(self):
		return math.floor(self.right)

	def operation_index(self, search):

		for i in range(len(self.lex_tokens)):
			if search[1] == self.lex_tokens[i][0].idx:
				return int(i)

		return 'THIS HAS FAILED!!!!'

	def generate(self):
		plus_minus_edge_case = 0
		terms = []
		op_func_table = {
			'self.op_TYPECAST'  : self.op_TYPECAST,
			'self.op_FACT'      : self.op_FACT,
			'self.op_PERC'      : self.op_PERC,
			'self.op_EXPO'      : self.op_EXPO,
			'self.op_MODULO'    : self.op_MODULO,
			'self.op_DIV_FLOOR' : self.op_DIV_FLOOR,
			'self.op_DIV'       : self.op_DIV,
			'self.op_MUL'       : self.op_MUL,
			'self.op_OR'        : self.op_OR,
			'self.op_AND'       : self.op_AND,
			'self.op_NOT'       : self.op_NOT,
			'self.op_DUB_EQUALS': self.op_DUB_EQUALS,
			'self.op_GT'        : self.op_GT,
			'self.op_LT'        : self.op_LT,
			'self.op_PLUS'      : self.op_PLUS,
			'self.op_MINUS'     : self.op_MINUS,
			'self.op_ROUND_NEAR': self.op_ROUND_NEAR,
			'self.op_ROUND_UP'  : self.op_ROUND_UP,
			'self.op_ROUND_DOWN': self.op_ROUND_DOWN
		}

		for idx, operation in enumerate(self.op_tokens):

			if operation[0] in ['FACT', 'PERC']:  # left {op}
				op_index = self.operation_index(operation)
				try:
					self.left  = self.lex_tokens[op_index-1][0].value
				except IndexError:
					return reqkMathLexer.error('<stdin>', 0, "list index out of range")
				op_function = f'self.op_{operation[0]}'

				terms.append([reqkMathLexer.Token('TEMP', op_func_table[op_function](), 1, 1)])

				self.lex_tokens[op_index-1] = terms[len(terms)-1]
				del self.lex_tokens[op_index]

			
			elif operation[0] in ['TYPECAST', 'NOT', 'ROUND_NEAR', 'ROUND_UP', 'ROUND_DOWN']:  # {op} right
				op_index = self.operation_index(operation)
				try:
					self.right = self.lex_tokens[op_index+1][0].value
				except:
					return reqkMathLexer.error('<stdin>', 0, "self.right -> failed to calculate")

				op_function = f'self.op_{operation[0]}'

				if operation[0] == 'TYPECAST':
					terms.append([reqkMathLexer.Token('TEMP', op_func_table[op_function](self.lex_tokens[op_index][0].value), 1, 1)])
				else:
					terms.append([reqkMathLexer.Token('TEMP', op_func_table[op_function](), 1, 1)])
				self.lex_tokens[op_index] = terms[len(terms)-1]
				del self.lex_tokens[op_index+1]


			elif operation[0] in ['PLUS', 'MINUS']:  # special plus minus case
				op_index = self.operation_index(operation)

				if op_index == 0:
					self.left = 0
					plus_minus_edge_case = 1
				elif type(self.lex_tokens[op_index-1][0].value) not in [int, float]:
					self.left = 0
					plus_minus_edge_case = 1
				else:
					try:
						self.left  = self.lex_tokens[op_index-1][0].value
					except IndexError:
						return reqkMathLexer.error('<stdin>', 0, "list index out of range")

				try:
					self.right = self.lex_tokens[op_index+1][0].value
				except IndexError:
					return reqkMathLexer.error('<stdin>', 0, "list index out of range")
				op_function = f'self.op_{operation[0]}'

				terms.append([reqkMathLexer.Token('TEMP', op_func_table[op_function](), 1, 1)])

				if plus_minus_edge_case == 1:
					plus_minus_edge_case = 0
					self.lex_tokens[op_index] = terms[len(terms)-1]
					del self.lex_tokens[op_index+1]

				else:
					self.lex_tokens[op_index-1] = terms[len(terms)-1]
					del self.lex_tokens[op_index:op_index+2]
				
			elif operation[0] == 'TEMP':  # skip over temp
				pass

			else:  # standard left {op} right
				op_index = self.operation_index(operation)
				try:
					self.left  = self.lex_tokens[op_index-1][0].value
					self.right = self.lex_tokens[op_index+1][0].value
				except IndexError:
					return reqkMathLexer.error('<stdin>', 0, "list index out of range")
				op_function = f'self.op_{operation[0]}'

				terms.append([reqkMathLexer.Token('TEMP', op_func_table[op_function](), 1, 1)])

				self.lex_tokens[op_index-1] = terms[len(terms)-1]
				del self.lex_tokens[op_index:op_index+2]

			if self.show_stages == True or self.dev_mode == True:
				if self.tag_printed == 0:
					print('\nCalculations:')
					self.tag_printed = 1
				print(terms[len(terms)-1])

		return self.lex_tokens[0][0].value
