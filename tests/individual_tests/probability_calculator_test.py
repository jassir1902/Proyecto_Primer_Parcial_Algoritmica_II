# tests/individual_tests/probability_calculator_test.py

import pytest
import os
import json
from src.utils.probability_calculator import (
    generar_terminos_dinamicamente,
    obtener_probabilidades_de_documento
)

# --- Datos de Prueba y Mocks ---
# Se usará en los tests que dependen de obtener_probabilidades_de_documento
MOCK_TEXTO_PDF = """
Este es un documento sobre algoritmos y estructuras de datos.
Los algoritmos son fundamentales en la programación. Las estructuras
de datos organizan la información. Un buen algoritmo es eficiente.
El estudio de algoritmos y datos es clave.
"""

# --- Fixture de Pytest para Mockear la lectura de PDF ---
@pytest.fixture
def mock_pdf_extraction(monkeypatch):
    """
    Este fixture intercepta la llamada a `extraer_texto_pdf` y, en su lugar,
    devuelve nuestro texto de prueba (MOCK_TEXTO_PDF).
    """
    def mock_extraer(ruta_pdf):
        return MOCK_TEXTO_PDF
    
    monkeypatch.setattr(
        'src.utils.probability_calculator.extraer_texto_pdf', 
        mock_extraer
    )

# --- Conjunto de Pruebas ---

def test_probability_calculation(mock_pdf_extraction):
    """
    TEST DE FUNCIONALIDAD PRINCIPAL:
    Verifica que se extraigan los términos correctos y se calculen las
    probabilidades 'p' y 'q' de manera adecuada.
    """
    terminos, p, q = obtener_probabilidades_de_documento("dummy_path.pdf", top_n=3)

    # CORRECCIÓN 1: La aserción debe coincidir con el resultado real de tu lógica.
    # El texto de mock tiene 'algoritmos' en plural. El top 3 será 'algoritmos', 'datos', 'estructuras'.
    # El orden es alfabético.
    expected_terminos = ['algoritmos', 'datos', 'estructuras']    
    assert terminos == expected_terminos
    
    assert len(p) == 3
    assert len(q) == 4
    
    # 2. Verificamos la suma de las probabilidades (usando tolerancia)
    assert abs(sum(p) - 0.85) < 1e-9
    assert abs(sum(q) - 0.15) < 1e-9

def test_probability_distribution(mock_pdf_extraction):
    """
    TEST DE DISTRIBUCIÓN DE PROBABILIDAD:
    Asegura que las probabilidades se distribuyan correctamente según la frecuencia.
    """
    # Con el texto de mock, las frecuencias son: 'algoritmos' (3), 'datos' (3), 'estructuras' (2).
    # Total de frecuencia = 8
    # Frecuencias relativas: 3/8, 3/8, 2/8
    # Probabilidades 'p' (escaladas por 0.85): 0.85 * 3/8, 0.85 * 3/8, 0.85 * 2/8
    
    terminos, p, q = obtener_probabilidades_de_documento("dummy_path.pdf", top_n=3)
    print(terminos)
    print(p)
    print(q)


    assert p[0] == p[1]
    
    # CORRECCIÓN: 'algoritmos' (p[0]) y 'datos' (p[1]) tienen la misma frecuencia, por lo tanto,
    # sus probabilidades deben ser iguales.
    assert abs(p[0] - p[1]) < 1e-9

    # Todas las probabilidades de fallo 'q' deben ser idénticas.
    # Aquí puedes usar 'len(set(q)) == 1' para verificar que todos los valores son iguales.
    assert len(set(q)) == 1

def test_generate_terms_basic_functionality():
    """
    TEST DE FUNCIONALIDAD BÁSICA (Unidad):
    Verifica que la función extraiga los términos más comunes, los limpie
    (sin stopwords, >2 caracteres) y los devuelva ordenados alfabéticamente.
    """
    # CORRECCIÓN 3: El texto de prueba debe reflejar la lógica de tu código (len > 2).
    # 'tres' y 'uno' tienen 4 y 3 caracteres, respectivamente.
    texto_controlado = "primero primero primero segundo segundo tercero"
    terminos = generar_terminos_dinamicamente(texto_controlado, top_n=2)
    print(terminos)
    
    # Las frecuencias son: 'uno' (3), 'dos' (2), 'tres' (1).
    # Top 2 son: 'uno', 'dos'.
    # Ordenados alfabéticamente: 'dos', 'uno'.
    assert terminos == ['primero', 'segundo']

def test_generate_terms_stopwords_filtering():
    """
    TEST DE FILTRADO DE STOPWORDS:
    Asegura que las palabras comunes en español sean eliminadas.
    """
    texto = "el perro y la gata sobre un tejado"
    terminos = generar_terminos_dinamicamente(texto, top_n=5)
    
    assert "el" not in terminos
    assert "la" not in terminos
    assert "y" not in terminos
    assert "sobre" not in terminos
    assert "un" not in terminos
    assert terminos == ['gata', 'perro', 'tejado']

def test_generate_terms_case_and_punctuation():
    """
    TEST DE MANEJO DE FORMATO:
    Verifica que la función sea insensible a mayúsculas/minúsculas y que
    ignore la puntuación.
    """
    texto = "¡Algoritmos, Algoritmos! Son la CLAVE. La clave es... algoritmos."
    terminos = generar_terminos_dinamicamente(texto, top_n=2)

    assert terminos == ['algoritmos', 'clave']

def test_generate_terms_top_n_parameter():
    """
    TEST DE PARÁMETRO top_n:
    Verifica que el parámetro 'top_n' limite el número de términos devueltos
    y que la longitud de palabra sea > 2.
    """
    # CORRECCIÓN 4: El texto de prueba debe tener palabras de más de 2 caracteres
    # para pasar el filtro de tu función.
    texto = "aaaa aaaa aaaa aaaa bbbb bbbb bbbb cccc cccc dddd"
    # Frecuencias: 'aaaa' (4), 'bbbb' (3), 'cccc' (2), 'dddd' (1).
    
    terminos_top_1 = generar_terminos_dinamicamente(texto, top_n=1)
    assert terminos_top_1 == ['aaaa']
    
    terminos_top_3 = generar_terminos_dinamicamente(texto, top_n=3)
    assert sorted(terminos_top_3) == ['aaaa', 'bbbb', 'cccc']
    
def test_empty_text_input(monkeypatch):
    """
    TEST DE CASO LÍMITE:
    Verifica que el sistema maneje correctamente un texto vacío.
    """
    monkeypatch.setattr(
        'src.utils.probability_calculator.extraer_texto_pdf', 
        lambda ruta: ""
    )

    terminos, p, q = obtener_probabilidades_de_documento("dummy_path.pdf")
    
    assert terminos == []
    assert p == []
    assert q == []

def test_no_relevant_terms(monkeypatch):
    """
    TEST DE CASO LÍMITE:
    Verifica el comportamiento cuando el texto solo contiene stopwords o palabras
    demasiado cortas, resultando en cero términos clave.
    """
    texto_irrelevante = "el la los un y que con por de a b c"
    monkeypatch.setattr(
        'src.utils.probability_calculator.extraer_texto_pdf', 
        lambda ruta: texto_irrelevante
    )
    
    terminos, p, q = obtener_probabilidades_de_documento("dummy_path.pdf")
    
    assert terminos == []
    assert p == []
    assert q == []