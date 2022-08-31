# attempt number 2
# One file cause might fail. seperate if complete. - seperated
# 17/10/2021 @ 3:29am  - lexer went very well :)
# 17/10/2021 @ 17:49pm - It is complete for now. I don't have 
#                        brackets but i do have order of operations :D
# 18/10/2021 @ 20:42pm - Added brackets and negative numbers, way 
#                        way easier than i initially anticipated =D
# 19/10/2021 @ 23:10pm - Added loads of stuff by v3.1

#from os import curdir
import reqkMathParser
import reqkMathInterpreter
import string

numbers = '0123456789'
letters = string.ascii_letters
op_T = {  # Token lookup table
	'!' :'FACT',
	'^' :'EXPO',
	'/' :'DIV',
	'*' :'MUL',
	'+' :'PLUS',
	'-' :'MINUS',
	'(' :'LPAREN',
	')' :'RPAREN',
	'%' :'PERC',
	'?' :'TYPECAST',
	'&' :'AND',
	'|' :'OR',
	'==':'DUB_EQUALS',
	'>' :'GT',
	'<' :'LT',
	'~' :'NOT',
	'_' :'ROUND_NEAR',
	'/%':'MODULO',
	'//':'DIV_FLOOR'
}
CONST_T = {
	'PI':3.141592653589793  # pi 15.
}
INT        = 'INT'
FLOAT      = 'FLOAT'
STRING     = 'STRING'


class error():
	def __init__(self, fn, pos, details):
		self.fn = fn
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


class unkownError:
	def __init__(self, fn, pos, details):
		self.fn = str(fn)
		self.pos = pos
		self.details = str(details)

	def __repr__(self):
		arrow_p = ('   '+' '*self.pos) + '^'
		error_string = arrow_p+'\n'+self.fn+' Col:'+str(self.pos)+' -> ! - Unkown Error: '+self.details+" - !"
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


	def makeString(self, starting_pos):
		s = ''

		while self.text[self.pos] in letters:
			currChar = self.text[self.pos]

			s += currChar
			if self.pos < len(self.text):
				self.pos += 1
			else:
				break

		return Token(STRING, s, starting_pos, len(s))


	def Lex(self):
		tokens = []
		self.text += ' '

		while self.pos < len(self.text):
			currChar = self.text[self.pos]

			if currChar in ' \n\t':
				self.pos += 1

			elif currChar in numbers:
				number = self.makeNumber(self.TK_IDX)
				if type(number) == error:
					return number
				else: 
					tokens.append([number])
					self.TK_IDX += 1

			elif currChar in op_T or currChar in ['=']:

				if currChar == '?':
					if self.pos == len(self.text)-1:
						return error(self.fn, self.pos, "Type-Cast at end of input")
					else:
						if self.text[self.pos+1] == 'i':
							tokens.append([Token(op_T[currChar], INT, self.TK_IDX, 2)])
							self.pos += 2
							self.TK_IDX += 2
						elif self.text[self.pos+1] == 'f':
							tokens.append([Token(op_T[currChar], FLOAT, self.TK_IDX, 2)])
							self.pos += 2
							self.TK_IDX += 2
						else:
							return error(self.fn, self.pos, "Unkown data Type-Cast")

				elif currChar == '_':
					if self.pos == len(self.text)-1:
						return error(self.fn, self.pos, "Round at end of input")
					else:
						if self.text[self.pos+1] == '>':
							tokens.append([Token('ROUND_UP', currChar+'>', self.TK_IDX, 2)])
							self.pos += 2
							self.TK_IDX += 2
						elif self.text[self.pos+1] == '<':
							tokens.append([Token('ROUND_DOWN', currChar+'<', self.TK_IDX, 2)])
							self.pos += 2
							self.TK_IDX += 2
						else:
							tokens.append([Token(op_T[currChar], currChar, self.TK_IDX, 1)])
							self.pos += 1
							self.TK_IDX += 1

				elif currChar == '=':
					if self.pos == len(self.text)-1:
						return unkownError(self.fn, self.pos, "'=' symbol at end of statement'")
					else:
						if self.text[self.pos+1] == '=':  #equal to
							tokens.append([Token(op_T[currChar*2], currChar*2, self.TK_IDX, 2)])
							self.pos += 2
							self.TK_IDX += 2
						else:
							return error(self.fn, self.pos, "Single equals is not possible")

				elif currChar == '/':
					if self.pos == len(self.text)-1:
						return unkownError(self.fn, self.pos, "'/' symbol at end of statement")
					else:
						if self.text[self.pos+1] == '%':  #modulo
							tokens.append([Token(op_T['/%'], '/%', self.TK_IDX, 2)])
							self.pos += 2
							self.TK_IDX += 2
						elif self.text[self.pos+1] == '/':  #DIV_FLOOR
							tokens.append([Token(op_T['//'], '//', self.TK_IDX, 2)])
							self.pos += 2
							self.TK_IDX += 2
						else:
							tokens.append([Token(op_T[currChar], currChar, self.TK_IDX, 1)])
							self.pos += 1
							self.TK_IDX += 1

				else:
					tokens.append([Token(op_T[currChar], currChar, self.TK_IDX, 1)])
					self.pos += 1
					self.TK_IDX += 1

			elif currChar in letters:
				try:
					word = self.makeString(self.TK_IDX)
				except:
					raise

				if word.value == 'PI':
					tokens.append([Token(FLOAT, CONST_T['PI'], self.TK_IDX, len(str(CONST_T['PI'])))])
					self.TK_IDX += 2
				else:
					if word.value[0].lower() == 'p':
						return unkownChar(self.fn, self.pos-len(word.value), currChar), ' - Did you mean "PI"?'
					return unkownChar(self.fn, self.pos-len(word.value), currChar)

			else:
				return unkownChar(self.fn, self.pos, currChar)


		return tokens


def main(fn, text, showtokens=False, showparse=False, dev_mode=False, show_stages=False):
	run = Lexer(fn, text)
	tokens = run.Lex()
	if type(tokens) in [error, unkownChar]:
		return tokens

	elif showtokens == True or dev_mode == True:
		print("\nTokens:")
		for idx, token in enumerate(tokens):
			print(token)

	parser = reqkMathParser.Parser(tokens)
	if dev_mode == False:
		try:
			current_ops = parser.parse()
		except IndexError:
			return error(fn, 0, "Index Out of range - try (type casting) | (check brackets)")
		except:
			return unkownError(fn, 0, "Input not possible")
	elif dev_mode == True:
		current_ops = parser.parse()

	if showparse == True or dev_mode == True:
		print("\nParsed:")
		for idx, parse in enumerate(current_ops):
			print(parse)

	for i in range(len(tokens)):
		for idx, token in enumerate(tokens):
			if token[0].Type_ == 'LPAREN' or token[0].Type_ == 'RPAREN':
				del tokens[idx]

	interpreter = reqkMathInterpreter.Interpreter(current_ops, tokens, show_stages, dev_mode)
	if dev_mode == False:
		try:
			result = interpreter.generate()
		except:
			return unkownError(fn, 0, "Input not possible")
	elif dev_mode == True:
		result = interpreter.generate()

	return result


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


def help():
	print("\n Commands:")
	print("  ':tk' - Toggles token visiblity")
	print("  ':pt' - Toggles parsed token visiblity")
	print("  ':st' - Toggles Calculation Visibilty")
	print("  ':f'  - Run code from file (:f {file directory}.reqk)")
	print("  ':h'  - Help guide")
	print("  ':q'  - Quits the program")
	print("\n Operations:")
	print("   |\'()\' - Brackets     | Most ")
	print("   |\'?\'  - Type Cast    | ↑ ")
	print("   |\'!\'  - Factorial    | | ")
	print("   |\'%\'  - Percentage   | | ")
	print("   |\'^\'  - Power        | | ")
	print("   |\'/%\' - Modulous     | | ")
	print("   |\'//\' - Floor divide | | Order of  ")
	print("   |\'/\'  - Divide       | | Operations")
	print("   |\'*\'  - Multiply     | | ")
	print("   |\'+\'  - Add          | | ")
	print("   |\'-\'  - Subtract     | | ")	
	print("   |\'_\'  - Round Near   | | ")	
	print("   |\'_>\' - Round Up     | ↓ ")	
	print("   |\'_<\' - Round Down   | Least ")	
	print("\n Logic/Bitwise:")
	print("   |'&'  - And          | |")
	print("   |'~'  - Not          | |")
	print("   |'|'  - Or           | |")
	print("   |'==' - Equals       | |")
	print("   |'>'  - Greater      | |")
	print("   |'<'  - Less         | |")
	print("\n Constants:")
	print("   |'PI' - π(3.14159...)| |")
	print("\n Data Types:")
	print("  - (INT)")
	print("  - (FLOAT)")
	print("\n Features:")
	print("  - Negative Numbers (surrounded with brackets) e.g (-3) + 5 = 2")
	print("  - If no numbers after decimal point, value is rounded to 0")
	print("    - e.g. {1. = 1.0}, {69. =  69.0}, {420. = 420.0}")
	print("  - Type Cast Syntax: ?(i/f) ?i() = int-cast, ?f() = float-cast")
	print("  - Logic operators: (7 & 8 = 0), (~3 = -4), (2 == 2 = True)")
	print("\n Tips:")
	print("  - If your program isn't working, try type casting to int ('?i()')")
	print("    - Some operations don't work with floats.\n")

