# src/lcs_detector/comparator.py

from .tokenizer import RegexTokenizer, TOKEN_DEFINITIONS
from .lcs_weighted import lcs_weighted # lcs_weighted.py no necesita cambios

# Sistema de pesos por defecto, ahora mucho más granular
DEFAULT_TOKEN_WEIGHTS = {
    'CONTROL_FLOW':     5.0,
    'DEF_KEYWORD':      4.5,
    'BOOLEAN_OP':       4.0,
    'COMPARISON_OP':    3.5,
    'ARITHMETIC_OP':    3.0,
    'ASSIGN_OP':        2.5,
    'BUILTIN':          2.0,
    'IDENTIFIER':       1.5,
    'DELIMITER':        1.0,
    'NUMBER_LITERAL':   0.5,
    'STRING_LITERAL':   0.5,
    'SPECIAL_LITERAL':  0.5,
    'IMPORT_KEYWORD':   0.2,
    'OTHER_KEYWORD':    0.2,
}

class CodeComparator:
    """
    Una clase de alto nivel y configurable para comparar la similitud
    entre dos fragmentos de código.
    """
    def __init__(self, weights: dict = None, token_rules: list = None):
        """
        Inicializa el comparador.
        
        Args:
            weights (dict, optional): Un diccionario para ponderar los tipos de token.
                                      Si es None, usa los pesos por defecto.
            token_rules (list, optional): Una lista de tuplas (TIPO, REGEX) para el 
                                          tokenizador. Si es None, usa las reglas por defecto.
        """
        self.weights = weights if weights else DEFAULT_TOKEN_WEIGHTS
        self.tokenizer = RegexTokenizer(token_rules if token_rules else TOKEN_DEFINITIONS)

    def compare(self, code1: str, code2: str) -> dict:
        """
        Compara dos fragmentos de código y devuelve un score y la secuencia común.
        """
        tokens1, weights1 = self.tokenizer.tokenize_and_normalize(code1, self.weights)
        tokens2, weights2 = self.tokenizer.tokenize_and_normalize(code2, self.weights)

        if not tokens1 or not tokens2:
            return {"similarity_score": 0.0, "common_sequence": []}

        # La función lcs_weighted no necesita cambios, ya que su interfaz es estable.
        # Aquí es donde se ve el poder de la buena modularización.
        score, lcs_seq = lcs_weighted(tokens1, weights1, tokens2, weights2)

        return {
            "similarity_score": score,
            "common_sequence": lcs_seq
        }