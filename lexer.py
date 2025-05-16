# lexer.py
from error import LexicalError

# Clase que representa un token léxico con tipo, contenido y ubicación
class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"

# Clase Lexer: convierte texto plano en una lista de tokens
class Lexer:
    def __init__(self, text):
        self.text = text          # Texto original
        self.tokens = []          # Lista de tokens resultantes
        self.line = 1             # Número de línea actual
        self.column = 1           # Columna actual
        self.pos = 0              # Posición actual

    # Avanza la posición y columna una o más veces
    def advance(self, steps=1):
        self.pos += steps
        self.column += steps

    # Mira el carácter que viene después sin avanzar
    def peek(self, offset):
        if self.pos + offset < len(self.text):
            return self.text[self.pos + offset]
        return ''

    # Función principal que recorre el texto y genera tokens
    def tokenize(self):
        while self.pos < len(self.text):
            char = self.text[self.pos]

            # Salto de línea incrementa la línea y reinicia la columna
            if char == '\n':
                self.line += 1
                self.column = 1
                self.pos += 1
                continue

            # Aquí se utiliza una serie de elifs para detectar los tokens
            # Esto eventualmente se va a cambiar por una tabla de patrones usando expresiones regulares para hacer el lexer más mantenible
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
                number = char
                self.advance(2)
                self.tokens.append(Token("NUM_LIST", f"<{number}>", self.line, self.column))

            elif char.isspace():
                self.advance()

            else:
                # Captura de texto extendido
                start_col = self.column
                value = ''
                while self.pos < len(self.text):
                    current = self.text[self.pos]
                    if current in ['#', '-', '*', '=', "'", '\n']:
                        break
                    value += current
                    self.advance()

                if value.strip():
                    self.tokens.append(Token("TEXT", value.strip(), self.line, start_col))
                else:
                    raise LexicalError("Caracter no reconocido", self.line, self.column)

        # Devuelve la lista completa de tokens
        return self.tokens
