import reqkParser
import reqkInterpreter

numbers = '0123456789'

op_T = {
	'^':'EXPO',
	'/':'DIV',
	'*':'MUL',
	'+':'PLUS',
	'-':'MINUS',
	'(' :'LPAREN',
	')' :'RPAREN',
}
INT        = 'INT'
FLOAT      = 'FLOAT'

class error():
	def __init__(self, fn, pos, details):
		self.fn      = fn
		self.pos     = pos
		self.details = details

	def __repr__(self):
		error_string = ('   '+' '*self.pos) + '^\n' + self.fn +' Col:'+str(self.pos)+' -> Error: ' + self.details
		return error_string

class unkownChar:
	def __init__(self, fn, pos, char):
		self.fn   = fn
		self.pos  = pos
		self.char = char

	def __repr__(self):
		arrow_p = ('   '+' '*self.pos) + '^'
		error_string = arrow_p+'\n'+self.fn+' Col:'+str(self.pos)+' -> Error: Unknown Character - \''+self.char+'\''
		return error_string

class Token():
	def __init__(self, Type_, Value, idx, length):
		self.Type_   = Type_
		self.value   = Value
		self.idx     = idx
		self.length  = length

	def __getitem__(self, parameter):
		return parameter

	def __repr__(self):
		if type(self.value) == int | float and self.value >= 0: return f'{self.Type_}, {self.value}, {self.length}, {self.idx}'
		else: return f'({self.Type_}, {self.value}, {self.length}, {self.idx})'

class Lexer():
	def __init__(self, fn, text):
		self.fn     = fn
		self.text   = text
		self.pos    = 0
		self.TK_IDX = 0
	
	def makeNumber(self, starting_pos):
		n = ''
		dots = 0
		negative = 0
		while self.text[self.pos] in numbers + '.':
			currChar = self.text[self.pos]
			if currChar == '.':
				dots += 1
				if dots > 1:
					return error(self.fn, self.pos, "Multiple Decimal Points")

			n += currChar

			if self.pos < len(self.text):
				self.pos += 1
			else:
				break

		if n[len(n)-1] == '.':
			n += '0'
		
		if dots == 1: return Token(FLOAT, float(n), starting_pos, len(n))
		return Token(INT, int(n), starting_pos, len(n))

	def lex(self):
		tokens = []
		self.text += ' '
		lbc, rbc, plbp = 0, 0, 0  #plbp = previous last bracket position

		while self.pos < len(self.text):
			currChar = self.text[self.pos]

			if currChar in ' \t':
				self.pos += 1

			elif currChar == '\n':
				return tokens, self.pos

			elif currChar in numbers:
				number = self.makeNumber(self.TK_IDX)
				if type(number) == error:
					return number
				else: 
					tokens.append([number])
					self.TK_IDX += 1

			elif currChar in op_T:
				if self.pos != 0:
					if self.text[self.pos-1] not in ['(',')',' '] and self.text[self.pos-1] not in numbers and currChar in ['-', '+']:
						return error(self.fn, self.pos, "Multiple operations")
				elif self.pos == 0:
					if currChar not in ['-', '+', '(', ')']:
						return error(self.fn, 0, "Incorrect operation at start of expression")

				if currChar in ['-', '+']:
					if self.pos == 0:
						tokens.insert(0, [Token(INT, 0, self.TK_IDX, 1)])
						self.TK_IDX += 1
					elif self.text[self.pos-1] == '(':
						tokens.insert(self.pos, [Token(INT, 0, self.TK_IDX, 1)])
						self.TK_IDX += 1

				elif currChar == '(': 
					lbc += 1
					plbp = self.pos
				elif currChar == ')': rbc += 1

				tokens.append([Token(op_T[currChar], currChar, self.TK_IDX, 1)])
				self.pos += len(currChar)
				self.TK_IDX += 1

			else:
				return unkownChar(self.fn, self.pos, currChar)

		if lbc == rbc:
			return tokens
		else:
			return error(self.fn, plbp, "Unequal amount of left and right brackets")

def main(fn, text):
	lexer = Lexer(fn, text)
	tokens = lexer.lex()
	if type(tokens) in [error, unkownChar]:
		return tokens

	parser = reqkParser.Parser(tokens)
	calc_string = parser.parse()
	#print("CALC_STRING:",calc_string)

	lexer = reqkInterpreter.Interpreter(calc_string)
	final = lexer.generate()

	return final

def file_opener(text):
	fn, expected_fe = '<stdin>', '.reqk'  # file extension
	text = text.strip()
	fe = text[len(text)-len(expected_fe):]
	if fe != expected_fe: 
		return(error(fn, len(text)-1, "Exptected file extension '.reqk'")), 1

	fn = text[3:]
	try:
		f = open(fn, "r")
		text = f.read()
	except FileNotFoundError:
		return(error(fn, 3, "No such file or directory")), 1

	return text, 0
