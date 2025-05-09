# parser.py
from error import SyntaxError

class ASTNode:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"ASTNode({self.type}, value={self.value})"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        self.pos += 1

    def expect(self, type_):
        token = self.current()
        if token is None:
            raise SyntaxError(f"Esperando {type_}, pero se llegó al final.", 0, 0)
        if token.type != type_:
            raise SyntaxError(f"Esperando {type_}, pero se encontró {token.type}", token.line, token.column)
        self.advance()
        return token

    def parse(self):
        ast = []
        while self.pos < len(self.tokens):
            token = self.current()
            if token.type == "HEADER":
                ast.append(self.parse_header())
            elif token.type == "BULLET":
                ast.append(self.parse_bullet())
            elif token.type == "BOLD_MARK":
                ast.append(self.parse_format("BOLD", "BOLD_MARK"))
            elif token.type == "ITALIC_MARK":
                ast.append(self.parse_format("ITALIC", "ITALIC_MARK"))
            elif token.type == "HIGHLIGHT_MARK":
                ast.append(self.parse_format("HIGHLIGHT", "HIGHLIGHT_MARK"))
            elif token.type == "CODE_MARK":
                ast.append(self.parse_format("CODE", "CODE_MARK"))
            elif token.type == "TEXT":
                ast.append(self.parse_paragraph())
            else:
                raise SyntaxError("Token inesperado", token.line, token.column)
        return ast

    def parse_header(self):
        self.expect("HEADER")
        text = self.expect("TEXT")
        return ASTNode("HEADER", text.value)

    def parse_bullet(self):
        self.expect("BULLET")
        text = self.expect("TEXT")
        return ASTNode("BULLET_ITEM", text.value)

    def parse_format(self, node_type, mark_token):
        self.expect(mark_token)
        text = self.expect("TEXT")
        self.expect(mark_token)
        return ASTNode(node_type, text.value)

    def parse_paragraph(self):
        parts = []
        while self.current() and self.current().type == "TEXT":
            parts.append(self.current().value)
            self.advance()
        return ASTNode("PARAGRAPH", ' '.join(parts))
