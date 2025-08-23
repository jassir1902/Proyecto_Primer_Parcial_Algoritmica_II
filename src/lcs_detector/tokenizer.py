# src/lcs_detector/tokenizer.py

import io
import re
import tokenize
from typing import List, Tuple, Dict, Any

# --- Definiciones de Tokens Específicos con Regex ---
# Ordenados por precedencia: el primero que coincida, gana.
TOKEN_DEFINITIONS = [
    # Palabras clave de control de flujo
    ('CONTROL_FLOW', r'\b(if|else|elif|for|while|break|continue|return|yield|try|except|finally|with|pass)\b'),
    # Palabras clave de importación
    ('IMPORT_KEYWORD', r'\b(import|from|as)\b'),
    # Palabras clave de definición y estructura
    ('DEF_KEYWORD', r'\b(def|class|lambda)\b'),
    # Operadores booleanos y de pertenencia
    ('BOOLEAN_OP', r'\b(and|or|not|in|is)\b'),
    # Palabras clave de aserción y eliminación
    ('OTHER_KEYWORD', r'\b(assert|del|global|nonlocal|raise)\b'),
    # Literales especiales
    ('SPECIAL_LITERAL', r'\b(True|False|None)\b'),
    # Funciones y tipos built-in comunes
    ('BUILTIN', r'\b(print|len|range|int|str|list|dict|set|tuple|open|sum|min|max)\b'),
    # Identificadores (nombres de variables, funciones, etc.)
    ('IDENTIFIER', r'[a-zA-Z_]\w*'),
    # Literales numéricos (enteros y flotantes)
    ('NUMBER_LITERAL', r'\d+(\.\d*)?'),
    # Operadores aritméticos y de bits
    ('ARITHMETIC_OP', r'\+|-|\*|/|%|//|\*\*|&|\||\^|<<|>>'),
    # Operadores de comparación
    ('COMPARISON_OP', r'==|!=|<=|>=|>|<'),
    # Operadores de asignación
    ('ASSIGN_OP', r'=|\+=|-=|\*=|/=|%=|//='),
    # Puntuación y delimitadores
    ('DELIMITER', r'\(|\)|\[|\]|\{|\}|,|\.|:|;'),
    # Literales de tipo string (el contenido no se valida con regex aquí, solo el token)
    ('STRING_LITERAL', r'.*') 
]

class RegexTokenizer:
    """
    Un tokenizador avanzado que usa el módulo `tokenize` de Python para la
    segmentación y un sistema de regex para una clasificación detallada.
    """
    def __init__(self, token_rules: List[Tuple[str, str]]):
        # Compilamos las regex para mayor eficiencia
        self.token_regex = [(token_type, re.compile(pattern)) for token_type, pattern in token_rules]

    def _classify(self, token_value: str) -> str:
        """Clasifica un valor de token según las reglas regex."""
        for token_type, pattern in self.token_regex:
            if pattern.fullmatch(token_value):
                return token_type
        return 'UNKNOWN' # Categoría por defecto si nada coincide

    def tokenize_and_normalize(self, code: str, weights: Dict[str, float]) -> Tuple[List[str], List[float]]:
        """
        Tokeniza, clasifica detalladamente y normaliza el código fuente.
        """
        classified_tokens = []
        identifier_map = {}
        literal_map = {}

        try:
            code_stream = io.StringIO(code)
            token_generator = tokenize.generate_tokens(code_stream.readline)

            for tok in token_generator:
                category = None
                value = tok.string
                normalized_value = value

                if tok.type == tokenize.NAME:
                    category = self._classify(value)
                    if category == 'IDENTIFIER':
                        # Normalizar solo si es un identificador genérico
                        if value not in identifier_map:
                            identifier_map[value] = f"ID_{len(identifier_map)}"
                        normalized_value = identifier_map[value]
                
                elif tok.type == tokenize.OP:
                    category = self._classify(value)

                elif tok.type == tokenize.NUMBER:
                    category = 'NUMBER_LITERAL'
                    if value not in literal_map:
                        literal_map[value] = f"LIT_N_{len(literal_map)}"
                    normalized_value = literal_map[value]

                elif tok.type == tokenize.STRING:
                    category = 'STRING_LITERAL'
                    # Normalizamos el string completo para evitar falsos negativos
                    if value not in literal_map:
                        literal_map[value] = f"LIT_S_{len(literal_map)}"
                    normalized_value = literal_map[value]
                
                # Ignoramos tokens no relevantes
                elif tok.type in [tokenize.COMMENT, tokenize.ENCODING, tokenize.NL, 
                                    tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT, tokenize.ENDMARKER]:
                    continue

                if category:
                    classified_tokens.append({'category': category, 'value': normalized_value})

        except (tokenize.TokenError, IndentationError):
            return [], []

        token_values = [token['value'] for token in classified_tokens]
        token_weights = [weights.get(token['category'], 1.0) for token in classified_tokens]

        return token_values, token_weights