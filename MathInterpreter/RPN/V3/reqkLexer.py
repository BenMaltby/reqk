import reqkParser
import reqkInterpreter
import string

numbers = '0123456789'
letters = string.ascii_letters

op_T = {
	'!' :'FACT',
	'^' :'EXPO',
	'/' :'DIV',
	'*' :'MUL',
	'+' :'PLUS',
	'-' :'MINUS',
	'(' :'LPAREN',
	')' :'RPAREN',
	'?' :'TYPECAST',
	'?i':'TYPECAST_INT',
	'?f':'TYPECAST_FLOAT',
	'_' :'ROUND_NEAR'
}
INT        = 'INT'
FLOAT      = 'FLOAT'
STRING     = 'STRING'
NAME       = 'NAME'

global_variables = {}

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

# class unkownError:
# 	def __init__(self, fn, pos, details):
# 		self.fn      = str(fn)
# 		self.pos     = pos
# 		self.details = str(details)

# 	def __repr__(self):
# 		arrow_p = ('   '+' '*self.pos) + '^'
# 		error_string = arrow_p+'\n'+self.fn+' Col:'+str(self.pos)+' -> ! - Unkown Error: '+self.details+" - !"
# 		return error_string

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

class VARIABLE:
	def __init__(self, name, value) -> None:
		self.name  = name
		self.value = value

	def __repr__(self) -> str:
		return f'{self.name} = {self.value}'

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

	def makeBinary(self, starting_pos: int) -> int:
		"""
		Creates binary string from string input

		parameters:
		-----------
		starting_pos: int
			used for error handling
		"""
		n = ''

		if self.text[self.pos] == ' ':
			return error(self.fn, self.pos, "Incorrect Binary Syntax. No spaces between '@' and number")
		if self.text[self.pos] not in ['0', '1']:
			return error(self.fn, self.pos, "Binary numbers can only contain 0's and 1's.")

		while self.text[self.pos] in numbers:
			currChar = self.text[self.pos]

			if currChar not in ['0', '1']:
				return error(self.fn, self.pos, "Binary numbers can only contain 0's and 1's.")

			n += currChar

			if self.pos < len(self.text):
				self.pos += 1
			else:
				break

		return n

	def makeString(self, starting_pos) -> Token:
		word = ''

		while self.text[self.pos] in letters or self.text[self.pos] in numbers:
			currChar = self.text[self.pos]

			if currChar not in numbers and currChar not in letters and currChar != '_':
				return error(self.fn, self.pos, "Impossible string format")

			word += currChar

			if self.pos < len(self.text):
				self.pos += 1
			else:
				break

		return Token(STRING, word, starting_pos, len(word))

	def makeVarName(self, starting_pos):
		word = ''

		if self.text[self.pos] not in letters and self.text[self.pos] != '_':
			return error(self.fn, self.pos, "Impossible Variable Name")

		while self.text[self.pos] in letters or self.text[self.pos] in numbers or self.text[self.pos] == '_':
			currChar = self.text[self.pos]

			word += currChar

			if self.pos < len(self.text):
				self.pos += 1
			else:
				break

		return Token(NAME, word, starting_pos, len(word))

	# def binary2denary(self, n):
	# 	den_num = 0
	# 	for i in range(len(n)): den_num += 2 ** i if n[::-1][i] == '1' else 0
	# 	return den_num

	def lex(self):
		tokens = []
		self.text += ' '
		lbc, rbc, plbp = 0, 0, 0  #plbp = previous last bracket position

		while self.pos < len(self.text):
			currChar = self.text[self.pos]
			#print("TOKENS",tokens)

			if currChar in ' \t':
				self.pos += 1

			elif currChar == '\n':
				return tokens, self.pos

			elif currChar == '@':
				# Number should be in binary.
				self.pos += 1
				bin_num = self.makeBinary(self.TK_IDX)
				if type(bin_num) in [error]:
					return bin_num

				den_num = int(bin_num, 2)
				tokens.append([Token(INT, den_num, self.pos, len(str(den_num)))])
				self.TK_IDX += 1

			elif currChar in letters:
				# make string
				word = self.makeString(self.TK_IDX)
				if type(word) in [error]:
					return word

				if word.value == 'asn':
					var_val = Token('TEMP', 0, 1, 1)
					
					while self.text[self.pos] not in letters:
						if self.text[self.pos] == ';':
							return error(self.fn, self.pos, "No Variable Name")
					
						if self.pos == len(self.text)-1:
							return error(self.fn, self.pos, "Incorrect Variable Assignment Syntax")
						else:
							self.pos += 1

					var_name = self.makeVarName(self.TK_IDX)
					if type(var_name) in [error]:
						return word

					while self.text[self.pos] != ';':
					
						if self.pos == len(self.text)-1:
							return error(self.fn, self.pos, "Incorrect Variable Assignment Syntax")
						else:
							self.pos += 1

					while self.text[self.pos] not in numbers:
					
						if self.pos < len(self.text)-1:
							self.pos += 1
						else:
							break

					if self.pos != len(self.text)-1:
						var_val = self.makeNumber(self.TK_IDX)
						if type(var_val) in [error]:
							return word

					global_variables.update({var_name.value:var_val.value})
					return VARIABLE(var_name.value, var_val.value)

				else:

					if word.value in global_variables:
						if type(global_variables[word.value]) == int:
							tokens.append([Token(INT, global_variables[word.value], self.TK_IDX, len(word.value))])
							self.TK_IDX += 1
						else:
							tokens.append([Token(FLOAT, global_variables[word.value], self.TK_IDX, len(word.value))])
							self.TK_IDX += 1

					else:
						return unkownChar(self.fn, self.pos-len(word.value), currChar)

			elif currChar in numbers:
				if len(tokens) >= 1:
					if str(tokens[self.TK_IDX-1][0].value) not in ['^','/','*','+','-','?','?i','?f','_','(',')']:
						return error(self.fn,tokens[self.TK_IDX-1][0].idx, "This Expression makes no sense.")
				number = self.makeNumber(self.TK_IDX)
				if type(number) == error:
					return number
				else: 
					tokens.append([number])
					self.TK_IDX += 1

			elif currChar in op_T:

				if len(tokens) >= 1:
					if str(tokens[self.TK_IDX-1][0].value) not in ['(',')',' '] and str(tokens[self.TK_IDX-1][0].value)[0] not in numbers and currChar in ['-', '+']:
						return error(self.fn, self.pos, "Multiple operations")
				elif self.pos == 0:
					if currChar not in ['-', '+', '(', ')', '_', '?']:
						return error(self.fn, 0, "Incorrect operation at start of expression")

				if currChar == '?':
					if self.pos == len(self.text)-1:
						return error(self.fn, self.pos, "TypeCast at end of expression")
					else:
						if self.text[self.pos+1].lower() in ['i', 'f']:
							if self.text[self.pos+1].lower() == 'i':
								tokens.append([Token('TYPECAST_INT', INT, self.pos, 2)])
								self.pos += 2
								self.TK_IDX += 1
								continue
							elif self.text[self.pos+1].lower() == 'f':
								tokens.append([Token('TYPECAST_FLOAT', FLOAT, self.pos, 2)])
								self.pos += 2
								self.TK_IDX += 1
								continue
						else:
							return error(self.fn, self.pos, "Unkown cast type")

				if currChar == '(':
					if self.pos != 0:
						if str(tokens[self.TK_IDX-1][0].value)[0] in numbers:
							tokens.insert(self.TK_IDX, [Token('MUL', '*', self.TK_IDX, 1)])
							self.TK_IDX += 1

				if currChar in ['-', '+']:
					if self.pos == 0:
						tokens.insert(0, [Token(INT, 0, self.TK_IDX, 1)])
						self.TK_IDX += 1
					elif self.text[self.pos-1] == '(':
						tokens.insert(self.pos, [Token(INT, 0, self.TK_IDX, 1)])
						self.TK_IDX += 1

				if currChar == '(': 
					lbc += 1
					plbp = self.pos
				if currChar == ')': 
					rbc += 1
					plbp = self.pos

				tokens.append([Token(op_T[currChar], currChar, self.TK_IDX, 1)])
				self.pos += len(currChar)
				self.TK_IDX += 1

			else:
				return unkownChar(self.fn, self.pos, currChar)

		for idx, token in enumerate(tokens):
			if idx < len(tokens)-1:
				if str(token[0].value) in numbers:
					if str(tokens[idx+1][0].value) in numbers or str(tokens[idx+1][0].value) in ['?i', '?f', '_']:
						return error(self.fn, token[0].idx, "Missing Operation between two numbers")

		if lbc == rbc:
			return tokens
		else:
			return error(self.fn, plbp, "Unequal amount of left and right brackets")

def main(fn, text):
	lexer = Lexer(fn, text)
	tokens = lexer.lex()
	if type(tokens) in [error, unkownChar, VARIABLE]:
		return tokens

	#print(tokens)

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

def commands():
	print("\n Commands:")
	#print("  ':tk' - Toggles token visiblity")
	#print("  ':pt' - Toggles parsed token visiblity")
	#print("  ':st' - Toggles Calculation Visibilty")
	print("  ':f'  - Run code from file (:f {file directory}.reqk)")
	print("  ':h'  - Help guide")
	print("  ':q'  - Quits the program\n")

def help():
	print("\n Operations:")
	print("   |\'@\'  - Binary conversion | Most ")
	print("   |\'()\' - Brackets          | ↑")
	print("   |\'?\'  - Type Cast         | | ")
	print("   |\'!\'  - Factorial         | | ")
	#print("   |\'%\'  - Percentage       | | ")
	print("   |\'^\'  - Power             | | ")
	#print("   |\'/%\' - Modulous         | | ")
	#print("   |\'//\' - Floor divide     | | Order of  ")
	print("   |\'/\'  - Divide            | | Operations")
	print("   |\'*\'  - Multiply          | | ")
	print("   |\'+\'  - Add               | | ")
	print("   |\'-\'  - Subtract          | ↓ ")	
	print("   |\'_\'  - Round Near        | Least ")	
	#print("   |\'_>\' - Round Up         | ↓ ")	
	#print("   |\'_<\' - Round Down       | Least ")	
	#print("\n Logic/Bitwise:")
	#print("   |'&'  - And          | |")
	#print("   |'~'  - Not          | |")
	#print("   |'|'  - Or           | |")
	#print("   |'==' - Equals       | |")
	#print("   |'>'  - Greater      | |")
	#print("   |'<'  - Less         | |")
	#print("\n Constants:")
	#print("   |'PI' - π(3.14159...)| |")
	print("\n Data Types:")
	print("  - (INT)")
	print("  - (FLOAT)")
	print("\n Features:")
	print("  - Variables - Syntax: 'asn (name) ; (value)'")
	print("  - Binary Conversion Syntax: '@1010' = 10, '@1101' = 13")
	print("  - Negative Numbers (surrounded with brackets) e.g (-3) + 5 = 2")
	#print("  - If no numbers after decimal point, value is rounded to 0")
	#print("    - e.g. {1. = 1.0}, {69. =  69.0}, {420. = 420.0}")
	print("  - Type Cast Syntax: ?(i/f) ?i() = int-cast, ?f() = float-cast\n")
	#print("  - Logic operators: (7 & 8 = 0), (~3 = -4), (2 == 2 = True)")
	# print("\n Tips:")
	# print("  - If your program isn't working, try type casting to int ('?i()')")
	# print("    - Some operations don't work with floats.\n")
