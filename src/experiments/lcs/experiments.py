import os
import sys
import json

# --- Configuración de Rutas ---
# Añadimos el directorio raíz del proyecto ('Proyecto_Primer_Parcial') al path de Python
# para poder importar módulos de 'src' como si fuera un paquete instalado.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.insert(0, project_root)
# --- Fin de Configuración de Rutas ---

# Importamos la función específica de la API que vamos a probar
from ...integration.api import comparar_archivos_codigo_api

def ejecutar_prueba_lcs_api():
    """
    Ejecuta una prueba de similitud de código entre dos archivos
    utilizando la función expuesta en la API.
    """
    print("="*60)
    print("🔬 Iniciando Prueba de Similitud de Código vía API")
    print("="*60)

    # Rutas a los archivos de código de prueba. Usamos rutas absolutas
    # para asegurar que la API las encuentre sin problemas.
    # ruta_code1 = os.path.abspath(os.path.join(current_dir, 'code1.py'))
    # ruta_code2 = os.path.abspath(os.path.join(current_dir, 'code2.py'))
    ruta_code1 = 'C:/Users/DELL/OneDrive/Escritorio/Algoritmica II/Proyecto_Primer_Parcial/src/experiments/lcs/code1.py'
    ruta_code2 = 'C:/Users/DELL/OneDrive/Escritorio/Algoritmica II/Proyecto_Primer_Parcial/src/experiments/lcs/code2.py'

    print(f"\n[Paso 1/2] Invocando la API con los archivos:")
    print(f"   - Archivo 1: {ruta_code1}")
    print(f"   - Archivo 2: {ruta_code2}")

    try:
        # Llamamos a la función de la API, que encapsula toda la lógica
        resultado = comparar_archivos_codigo_api(ruta_code1, ruta_code2)
        print("   -> La API respondió correctamente.")
    except Exception as e:
        print(f"\n❌ ERROR: Ocurrió un error al llamar a la función de la API.")
        print(f"   Asegúrate de que la función 'comparar_archivos_codigo_api' en 'src/integration/api.py'")
        print(f"   y sus dependencias ('tokenize_code', 'comparar_archivos_codigo_api') estén completas y sin errores.")
        print(f"   Error original: {e}")
        return

    print("\n[Paso 2/2] Presentando resultados obtenidos de la API...")

    # Verificamos si la API devolvió un error
    if resultado.get("status") == "error":
        print(f"\n❌ La API devolvió un error: {resultado.get('message')}")
        return

    # Extraemos los datos del diccionario devuelto por la API
    score = resultado.get("score", 0.0)
    lcs_sequence = resultado.get("lcs_sequence", [])

    print("-" * 40)
    print(f"Score de Similitud Ponderado: {score:.4f}")
    print("-" * 40)
    
    print("\nSecuencia Común Más Larga (LCS) encontrada (Tokens):")
    # Usamos json.dumps para formatear la lista de tokens de forma legible
    lcs_pretty_print = json.dumps(lcs_sequence, indent=4)
    print(lcs_pretty_print)
    
    print("\n" + "="*60)
    print("✅ Prueba Finalizada.")
    print("="*60)

if __name__ == "__main__":
    # Antes de ejecutar, asegúrate de que tu api.py esté completa y funcional.
    # El snippet que me pasaste tenía la función `comparar_archivos_codigo_api` incompleta.
    # He escrito este script asumiendo que la completaste para que devuelva un diccionario como:
    # {"status": "success", "score": score, "lcs": lcs_sequence}
    ejecutar_prueba_lcs_api()