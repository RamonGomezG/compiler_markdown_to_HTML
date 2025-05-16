# generator.py

def generate_html(ast):
    html = ""
    in_list = False

    #despues se usará un diccionario de funciones para resolver esto en lugar de elif,. 
    for node in ast:
        if node.type == "HEADER":
            html += f"<h1>{node.value}</h1>\n"
        elif node.type == "PARAGRAPH":
            html += f"<p>{node.value}</p>\n"
        elif node.type == "BULLET_ITEM":
            if not in_list:
                html += "<ul>\n"
                in_list = True
            html += f"<li>{node.value}</li>\n"
        else:
            if in_list:
                html += "</ul>\n"
                in_list = False
            if node.type == "BOLD":
                html += f"<b>{node.value}</b>\n"
            elif node.type == "ITALIC":
                html += f"<i>{node.value}</i>\n"
            elif node.type == "HIGHLIGHT":
                html += f"<mark>{node.value}</mark>\n"
            elif node.type == "CODE":
                html += f"<code>{node.value}</code>\n"

    if in_list:
        html += "</ul>\n"

    return html
