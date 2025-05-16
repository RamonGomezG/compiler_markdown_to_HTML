# parser.py
# Este módulo toma una lista de tokens generados por el lexer y construye un árbol de sintaxis abstracta (AST),
# que representa la estructura lógica del documento (encabezados, listas, texto en formato, etc.)

from error import SyntaxError  # Importa la clase personalizada para errores de sintaxis


# Clase ASTNode es un nodo del árbol sintáctico
class ASTNode:
    def __init__(self, type_, value=None):
        self.type = type_   
        self.value = value  

    def __repr__(self):
        return f"ASTNode({self.type}, value={self.value})"
# Clase Parser genera una lista de nodos AST
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # Lista de tokens del lexer
        self.pos = 0          # Posición actual dentro de la lista

    def current(self):
        # Devuelve el token actual, o None si llegamos al final
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        # Avanza al siguiente token
        self.pos += 1

    def expect(self, type_):
        # Verifica que el token actual sea del tipo esperado, si no, lanza un error de sintaxis.
        token = self.current()
        if token is None:
            raise SyntaxError(f"Esperando {type_}, pero se llegó al final.", 0, 0)
        if token.type != type_:
            raise SyntaxError(f"Esperando {type_}, pero se encontró {token.type}", token.line, token.column)
        self.advance()
        return token

    def parse(self):
        # Método principal que recorre todos los tokens y genera una lista de nodos AST
        ast = []
        while self.pos < len(self.tokens):
            token = self.current()

            # Elegimos la función de parsing según el tipo de token actual
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
        # Reconoce un encabezado del tipo: # Título
        self.expect("HEADER")         # Espera el token "#"
        text = self.expect("TEXT")    # Luego espera el texto
        return ASTNode("HEADER", text.value)

    def parse_bullet(self):
        # Reconoce un elemento de lista con viñeta: - Elemento
        self.expect("BULLET")         # Espera el token "-"
        text = self.expect("TEXT")    # Luego espera el texto
        return ASTNode("BULLET_ITEM", text.value)

    def parse_format(self, node_type, mark_token):
        # Reconoce formatos simétricos como **negrita**, *cursiva*, ==resaltado==, 'código'
        self.expect(mark_token)       # Marca de apertura
        text = self.expect("TEXT")    # Texto contenido
        self.expect(mark_token)       # Marca de cierre
        return ASTNode(node_type, text.value)

    def parse_paragraph(self):
        # Agrupa múltiples tokens TEXT consecutivos como un párrafo
        parts = []
        while self.current() and self.current().type == "TEXT":
            parts.append(self.current().value)
            self.advance()
        return ASTNode("PARAGRAPH", ' '.join(parts))
