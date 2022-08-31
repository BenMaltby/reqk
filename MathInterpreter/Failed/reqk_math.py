numbers = '0123456789'

_INT    = "INT"
_FLOAT  = "FLOAT"
_EXPO   = "EXPO"
_DIV    = "DIV"
_MUL    = "MUL"
_PLUS   = "PLUS"
_MINUS  = "MINUS"
_LPAREN = "LPAREN"
_RPAREN = "RPAREN"

class Position:
    def __init__(self, idx, col):
        self.idx = idx
        self.col = col

    def advance(self):
        self.idx += 1
        self.col += 1

        return self

class Token:
    def __init__(self, _type, value=None):
        self._type = _type
        self.value = value
    def __repr__(self):
        if self.value >= 0: return f'{self._type}:{self.value}'
        return f'{self._type}'

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, -1)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance()
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def Tokenizer(self):  # make tokens
        tokens = []

        while self.current_char != None:
            if self.current_char in ' ':
                self.advance()
            elif self.current_char in numbers:
                tokens.append(self.process_number())
            elif self.current_char == '^':
                tokens.append(_EXPO)
                self.advance()
            elif self.current_char == '/':
                tokens.append(_DIV)
                self.advance()
            elif self.current_char == '*':
                tokens.append(_MUL)
                self.advance()
            elif self.current_char == '+':
                tokens.append(_PLUS)
                self.advance()
            elif self.current_char == '-':
                tokens.append(_MINUS)
                self.advance()
            elif self.current_char == '(':
                tokens.append(_LPAREN)
                self.advance()
            elif self.current_char == ')':
                tokens.append(_RPAREN)
                self.advance()
            else:
                return [], ('ILLEGAL CHARACTER', self.current_char)

        return tokens, None

    def process_number(self):
        n = ''
        dot = 0

        while self.current_char != None and self.current_char in numbers + '.':
            if self.current_char == '.':
                if dot == 1: break
                dot += 1
                n += '.'
            else:
                n += self.current_char
            self.advance()

        if dot == 0:
            return Token(_INT, int(n))
        else:
            return Token(_FLOAT, float(n))

class Parse:
    def __init__(self, TOKENS):
        self.TOKENS = TOKENS
        self.TKPOS = Position(-1, -1)
        self.current_TOK = None
        self.advance()

    def advance(self):
        self.TKPOS.advance()
        self.current_TOK = self.TOKENS[self.TKPOS.idx] if self.TKPOS.idx < len(self.TOKENS) else None

    def Organise(self):
        organised_tokens = []

        while self.current_TOK != None:
            if self.current_TOK == _LPAREN:
                organised_tokens.append(self.make_brackets())
            else:
                organised_tokens.append(self.current_TOK)
                self.advance()

        return organised_tokens

    def make_brackets(self):
        brackets = [_LPAREN]

        while self.current_TOK != _RPAREN or self.current_TOK != None:
            if self.TOKENS[self.TKPOS.idx][3:]:
                brackets.append(self.TOKENS[self.TKPOS.idx][3:])
            else:
                brackets.append(self.current_TOK)
            self.advance()

        if self.current_TOK == None:
            return f'{self.TOKENS[self.TKPOS.idx]._type - 1} requires bracket'

        return brackets

def main(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.Tokenizer()

    #print(tokens)

    parse = Parse(tokens)
    brackets = parse.Organise()

    # return tokens, error
    return brackets, error


if __name__ == "__main__":
    running = True

    while running:
        raw = input(">> ")
        if raw == 'q':
            running = False
        else:
            result, error = main('<stdin>', raw)
            if error:
                print(error)
            else:
                print(result)
