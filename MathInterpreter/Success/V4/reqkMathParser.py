from operator import itemgetter
from reqkMathInterpreter import global_variables
import reqkMathLexer

op_T = [  # Token lookup table
	'TYPECAST',
	'FACT',
	'PERC',
	'EXPO',
	'DIV',
	'MUL',
	'AND',
	'PLUS',
	'MINUS',
	'OR',
	'DUB_EQUALS',
	'GT',
	'LT',
	'NOT',
	'ROUND_NEAR',
	'ROUND_UP',
	'ROUND_DOWN',
	'MODULO',
	'DIV_FLOOR'
]

class Parser:
	def __init__(self, tokens_str):
		self.token_str   = tokens_str
		self.pos = 0
		self.bracket_ops = []

	def operation_sort(self, op_string):
		op_order = ['LPAREN', 'RPAREN', 'TYPECAST', 
					'FACT', 'PERC', 'EXPO', 'MODULO',
					'DIV_FLOOR', 'DIV', 'MUL', 'OR', 
					'AND', 'NOT', 'DUB_EQUALS', 
					'GT', 'LT', 'PLUS', 
					'MINUS', 'ROUND_NEAR', 'ROUND_UP',
					'ROUND_DOWN']
		op_string_numbered = []

		for i in range(len(op_string)):
			for j in range(len(op_order)):
				if op_string[i][0] == op_order[j]:
					op_string_numbered.append([j, op_string[i][1]])

		op_string_numbered = sorted(op_string_numbered, key=itemgetter(0))

		for i in range(len(op_string_numbered)):
			op_string[i] = [op_order[op_string_numbered[i][0]], op_string_numbered[i][1]]

		return op_string

	def make_bracket(self):
		current_ops = []

		while self.token_str[self.pos][0].Type_ != 'RPAREN':
			Token = self.token_str[self.pos][0]

			if Token.Type_ == 'LPAREN':
				self.pos+=1
				self.bracket_ops.append(self.make_bracket())

			elif Token.Type_ in op_T:
				current_ops.append([Token.Type_, Token.idx])
				self.pos += 1

			else:
				self.pos += 1

		if self.token_str[self.pos][0].Type_ == 'RPAREN':
			self.pos += 1
			
		current_ops = self.operation_sort(current_ops)
		return current_ops

	def parse(self):
		current_ops = []

		while self.pos < len(self.token_str):
			Token = self.token_str[self.pos][0]
 
			if Token.Type_ in ['LPAREN']:
				self.pos+=1
				self.bracket_ops.append(self.make_bracket())

			elif Token.Type_ in op_T:
				current_ops.append([Token.Type_, Token.idx])
				self.pos += 1

			elif Token.Type_ == 'ASN':  # variable parse
				self.pos += 1
				if self.token_str[self.pos][0].Type_ == 'NAME' and len(self.token_str[self.pos][0].value) > 0:
					name, key = self.token_str[self.pos][0].value, self.token_str[self.pos+2][0].value
					global_variables.update({name:key})
					return f'{name} = {global_variables[name]}'
				else:
					return reqkMathLexer.syntaxError('<stdin>', 3, 'Variable missing name')

			else:
				self.pos += 1

		current_ops = self.operation_sort(current_ops)
		self.bracket_ops.append(current_ops)

		final = []
		for idx, operation in enumerate(self.bracket_ops):
			for i in range(len(operation)):
				final.append(operation[i])

		return final

