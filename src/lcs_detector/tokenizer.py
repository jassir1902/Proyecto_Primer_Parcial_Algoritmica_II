# src/lcs_detector/tokenizer.py

def tokenize_code(code):
    """
    Tokeniza el código fuente en una secuencia de tokens clasificados.
    
    :param code: Cadena de texto representando el código fuente
    :return: Lista de tokens clasificados (cada token es una tupla de tipo y valor)
    """
    # Expresiones regulares para identificar tokens en el código
    import re
    keywords = {'def', 'return', 'if', 'else', 'for'}
    operators = {'+', '-', '=', '==', '!=', '*', '/'}
    
    # Eliminar comentarios (simplificación, solo para comentarios en una línea)
    code = re.sub(r'#.*', '', code)
    
    # Dividir el código en tokens (palabras y operadores)
    tokens = re.findall(r'\w+|[^\w\s]', code)  # Dividir en tokens de tipo palabra y operador
    
    tokenized_code = []
    
    # Clasificar los tokens en categorías: palabras clave, operadores, identificadores, etc.
    for token in tokens:
        if token in keywords:
            tokenized_code.append(('keyword', token))
        elif token in operators:
            tokenized_code.append(('operator', token))
        else:
            tokenized_code.append(('identifier', token))
    
    return tokenized_code
