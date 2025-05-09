# main.py

from lexer import Lexer
from parser import Parser
from generator import generate_html

input_text = """
# Título
Este es un texto de prueba
- Elemento 1
- Elemento 2
**Importante**
*Enfatizado*
==Resaltado==
'código'
"""

try:
    lexer = Lexer(input_text)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    html = generate_html(ast)
    print("🔧 HTML Generado:\n")
    print(html)

except Exception as e:
    print(str(e))
