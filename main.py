
from lexer import Lexer
from parser import Parser
from generator import generate_html
import webbrowser
import os

# Archivos de entrada y salida
input_filename = "prueba.txt"
output_filename = "salida.html"

try:
    # 1. Leer contenido del archivo de entrada
    with open(input_filename, "r", encoding="utf-8") as file:
        input_text = file.read()

    # 2. Compilar: Lexer → Parser → Generator
    lexer = Lexer(input_text)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    ast = parser.parse()

    html = generate_html(ast)

    # 3. Guardar el HTML generado en archivo
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write("<!DOCTYPE html>\n<html>\n<head><meta charset='utf-8'></head>\n<body>\n")
        file.write(html)
        file.write("</body>\n</html>")

    print(f"HTML generado exitosamente")

    # 4. Abrir el HTML en el navegador predeterminado
    abs_path = os.path.abspath(output_filename)
    webbrowser.open(f"file://{abs_path}")

except Exception as e:
    print(f"Error durante la compilación:\n{str(e)}")
