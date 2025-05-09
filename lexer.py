# lexer.py
from error import LexicalError

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.line = 1
        self.column = 1
        self.pos = 0

    def advance(self, steps=1):
        self.pos += steps
        self.column += steps

    def peek(self, offset):
        if self.pos + offset < len(self.text):
            return self.text[self.pos + offset]
        return ''

    def tokenize(self):
        while self.pos < len(self.text):
            char = self.text[self.pos]

            if char == '\n':
                self.line += 1
                self.column = 1
                self.pos += 1
                continue

            if char == '#':
                self.tokens.append(Token("HEADER", "#", self.line, self.column))
                self.advance()

            elif char == '-' and (self.pos == 0 or self.text[self.pos - 1] in ['\n', ' ']):
                self.tokens.append(Token("BULLET", "-", self.line, self.column))
                self.advance()

            elif char == '*' and self.peek(1) == '*':
                self.tokens.append(Token("BOLD_MARK", "**", self.line, self.column))
                self.advance(2)

            elif char == '*':
                self.tokens.append(Token("ITALIC_MARK", "*", self.line, self.column))
                self.advance()

            elif char == '=' and self.peek(1) == '=':
                self.tokens.append(Token("HIGHLIGHT_MARK", "==", self.line, self.column))
                self.advance(2)

            elif char == "'":
                self.tokens.append(Token("CODE_MARK", "'", self.line, self.column))
                self.advance()

            elif char.isdigit() and self.peek(1) == '.':
                num = char
                self.advance(2)
                self.tokens.append(Token("NUM_LIST", f"<{num}>", self.line, self.column))

            elif char.isspace():
                self.advance()

            else:
                # Captura de texto
                start_col = self.column
                value = ''
                while self.pos < len(self.text) and self.text[self.pos] not in ['\n', '#', '-', '*', '=', "'", ' ', '.']:
                    value += self.text[self.pos]
                    self.advance()
                if value:
                    self.tokens.append(Token("TEXT", value, self.line, start_col))
                else:
                    raise LexicalError("Caracter no reconocido", self.line, self.column)

        return self.tokens
