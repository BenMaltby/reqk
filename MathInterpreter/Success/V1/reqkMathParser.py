from operator import itemgetter

op_T = [  # Token lookup table
	'FACT',
	'EXPO',
	'DIV',
	'MUL',
	'PLUS',
	'MINUS',
	'LPAREN',
	'RPAREN'
]

class Parser:
	def __init__(self, tokens_str):
		self.token_str   = tokens_str

	def operation_sort(self, op_string):
		op_order = ['LPAREN', 'RPAREN', 'FACT', 'EXPO', 'DIV', 'MUL', 'PLUS', 'MINUS']
		op_string_numbered = []

		for i in range(len(op_string)):
			for j in range(len(op_order)):
				if op_string[i][0] == op_order[j]:
					op_string_numbered.append([j, op_string[i][1]])

		op_string_numbered = sorted(op_string_numbered, key=itemgetter(0))

		for i in range(len(op_string_numbered)):
			op_string[i] = [op_order[op_string_numbered[i][0]], op_string_numbered[i][1]]

		return op_string


	def parse(self):
		current_ops = []
		
		for idx, Token in enumerate(self.token_str):
			if Token[0].Type_ in op_T:
				current_ops.append([Token[0].Type_, Token[0].idx])

		current_ops = self.operation_sort(current_ops)

		return current_ops

