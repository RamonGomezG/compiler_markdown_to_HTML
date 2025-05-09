# error.py

class CompilerError(Exception):
    pass

class LexicalError(CompilerError):
    def __init__(self, message, line, column):
        super().__init__(f"[Lexical Error] {message} at line {line}, column {column}")

class SyntaxError(CompilerError):
    def __init__(self, message, line, column):
        super().__init__(f"[Syntax Error] {message} at line {line}, column {column}")
