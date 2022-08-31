numbers = '0123456789'

TT_INT    = "INT"
TT_FLOAT  = "FLOAT"
TT_EXPO   = "EXPO"
TT_DIV    = "DIV"
TT_MUL    = "MUL"
TT_PLUS   = "PLUS"
TT_MINUS  = "MINUS"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"

class Position:
    def __init__(self, idx, col):
        self.idx = idx
        self.col = col

    def advance(self):
        self.idx += 1
        self.col += 1

        return self

class Token:
    def __init__(self, TT_type, value=None):
        self.TT_type = TT_type
        self.value = value
    def __repr__(self):
        if self.value >= 0: return f'{self.TT_type}:{self.value}'
        return f'{self.TT_type}'

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
                tokens.append(TT_EXPO)
                self.advance()
            elif self.current_char == '/':
                tokens.append(TT_DIV)
                self.advance()
            elif self.current_char == '*':
                tokens.append(TT_MUL)
                self.advance()
            elif self.current_char == '+':
                tokens.append(TT_PLUS)
                self.advance()
            elif self.current_char == '-':
                tokens.append(TT_MINUS)
                self.advance()
            elif self.current_char == '(':
                tokens.append(TT_LPAREN)
                self.advance()
            elif self.current_char == ')':
                tokens.append(TT_RPAREN)
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
            return Token(TT_INT, int(n))
        else:
            return Token(TT_FLOAT, float(n))


def main(fn, text):
    lexer = Lexer(fn, text)
    tokens, error = lexer.Tokenizer()

    return tokens, error


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
