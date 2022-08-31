from operator import itemgetter

op_T = [  # Token lookup table
	'FACT',
	'PERC',
	'EXPO',
	'DIV',
	'MUL',
	'PLUS',
	'MINUS'
]

class Parser:
	def __init__(self, tokens_str):
		self.token_str   = tokens_str
		self.pos = 0
		self.bracket_ops = []

	def operation_sort(self, op_string):
		op_order = ['LPAREN', 'RPAREN', 'FACT', 'PERC', 'EXPO', 'DIV', 'MUL', 'PLUS', 'MINUS']
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

			else:
				self.pos += 1

		current_ops = self.operation_sort(current_ops)
		self.bracket_ops.append(current_ops)

		final = []
		for idx, operation in enumerate(self.bracket_ops):
			for i in range(len(operation)):
				final.append(operation[i])

		return final

