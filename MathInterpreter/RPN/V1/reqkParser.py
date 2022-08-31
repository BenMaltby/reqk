op_T = [  # Token lookup table
	'EXPO',
	'MUL',
	'DIV',
	'MINUS',
	'PLUS',
	'LPAREN',
	'RPAREN',
]

class Parser:
	def __init__(self, tokens_str):
		self.token_str   = tokens_str
		self.pos         = 0

	def infix_postfix(self):
		stack = []
		calc_string = []

		while self.pos < len(self.token_str):
			Token = self.token_str[self.pos][0]
			# print("Current Token:",Token)
			# print("CALC::",calc_string)
			# print("STACK:",stack, '\n')

			if Token.Type_ in ['INT', 'FLOAT']:  # just add the numbers straight to calc_string
				calc_string.append(Token.value)

			elif Token.Type_ in op_T:

				if Token.Type_ == 'RPAREN':  # dump stack until lparen
					lparen_idx = 0
					for idx, op, in enumerate(stack):
						if op == 'LPAREN':
							lparen_idx = idx+1
							break
						elif op != 'RPAREN':
							calc_string.append(op)
					
					del stack[0:lparen_idx]

				elif Token.Type_ == 'LPAREN':  # left bracket resets order of operations
					stack.insert(0, Token.Type_)

				else:
					if len(stack) == 0:
						stack.append(Token.Type_)

					else:
						delete_index = 0
						for idx, op in enumerate(stack):  # check order of operation and dump or add to the stack accordingly
							if op_T.index(op) < op_T.index(Token.Type_):
								calc_string.append(op)
								if idx != len(stack)-1:
									delete_index = idx+1
								if idx == len(stack)-1:
									stack.clear()
									stack.append(Token.Type_)
									delete_index = 0
							elif op_T.index(op) > op_T.index(Token.Type_):
								stack.insert(idx, Token.Type_)
								break
							else:
								calc_string.append(Token.Type_)
								break

						del stack[:delete_index]

			if self.pos == len(self.token_str)-1:  # dump stack if at end of tokens
				if len(stack) > 0:
					calc_string += stack

			self.pos += 1

		return calc_string

	def parse(self):
		final = self.infix_postfix()

		return final
