import PyPDF2
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# --- Asegúrate de haber descargado los recursos de NLTK ---
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')

def extraer_texto_pdf(ruta_pdf):
    # (Esta función no cambia)
    with open(ruta_pdf, 'rb') as file:
        lector_pdf = PyPDF2.PdfReader(file)
        texto = ""
        for page in lector_pdf.pages:
            texto += page.extract_text() or ""
    return texto

def generar_terminos_dinamicamente(texto, top_n=20):
    # (Esta función no cambia, pero el resultado será diferente con las stopwords correctas)
    
    # Usar stopwords en español
    stop_words = set(stopwords.words('english'))

    tokens = word_tokenize(texto.lower())
    palabras_limpias = [
        palabra for palabra in tokens 
        if palabra.isalpha() and len(palabra) > 2 and palabra not in stop_words
    ]
    conteo_palabras = Counter(palabras_limpias)
    terminos_comunes = conteo_palabras.most_common(top_n)
    terminos_clave = sorted([termino for termino, freq in terminos_comunes])
    
    return terminos_clave

def obtener_probabilidades_de_documento(ruta_pdf, top_n=20, prob_exito_total=0.85):
    """
    Proceso completo y corregido.
    """
    texto = extraer_texto_pdf(ruta_pdf)
    terminos_clave_ordenados = generar_terminos_dinamicamente(texto, top_n)
    
    if not terminos_clave_ordenados:
        print("Advertencia: No se encontraron términos clave relevantes.")
        return [], [], []

    texto_lower = texto.lower()
    frecuencias = [len(re.findall(r'\b' + re.escape(term) + r'\b', texto_lower)) for term in terminos_clave_ordenados]
    #print(frecuencias)

    total_frecuencia = sum(frecuencias)
    #print(total_frecuencia)

    if total_frecuencia == 0:
        print("Advertencia: Los términos clave no aparecen en el texto.")
        return terminos_clave_ordenados, [], []

    # CORRECCIÓN 2: Lógica de probabilidad revisada
    # 1. Calcular frecuencias relativas (cuya suma es 1)
    frecuencias_relativas = [f / total_frecuencia for f in frecuencias]
    #print(frecuencias_relativas)

    # 2. Escalar estas frecuencias para que sumen `prob_exito_total`
    p = [freq * prob_exito_total for freq in frecuencias_relativas]
    
    # 3. Distribuir la probabilidad restante (1 - prob_exito_total) entre los q's
    prob_fallo_total = 1 - prob_exito_total
    n = len(terminos_clave_ordenados)
    q_val = prob_fallo_total / (n + 1)
    q = [q_val] * (n + 1)
    
    return terminos_clave_ordenados, p, q

# --- Ejemplo de uso ---
# terminos, p, q = obtener_probabilidades_de_documento('C:/Users/DELL/OneDrive/Escritorio/Algoritmica II/Trabajo primer parcial.pdf')

# if terminos:
#     print("✅ Términos Clave Identificados (Corregido):")
#     print(terminos)
#     print("\n✅ Probabilidades de Éxito (p) - Suma:", sum(p))
#     print(p)
#     # print(p) # Descomentar para ver la lista completa
#     print("\n✅ Probabilidades de Fallo (q) - Suma:", sum(q))
#     print(q)
#     # print(q) # Descomentar para ver la lista completa