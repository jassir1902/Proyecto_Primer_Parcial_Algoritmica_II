# src/integration/api.py

import os
from ..projects_management.project_manager import cargar_proyectos
# No necesitamos importar registrar/eliminar aquí, se manejan en su propio módulo.
from ..obst.obst import optimal_bst
from ..lcs_detector.lcs_weighted import lcs_weighted
from ..lcs_detector.tokenizer import tokenize_code
from ..utils.probability_calculator import obtener_probabilidades_de_documento

# --- API de Gestión de Proyectos (Sin cambios, ya era correcta) ---

def registrar_proyecto_api(nombre, ruta_codigo, ruta_documento):
    from ..projects_management.project_manager import registrar_proyecto
    registrar_proyecto(nombre, ruta_codigo, ruta_documento)
    return {"status": "success", "message": f"Proyecto '{nombre}' registrado exitosamente."}

def listar_proyectos_api():
    proyectos = cargar_proyectos()
    proyectos_listados = [{"nombre": p.nombre, "ruta_codigo": p.ruta_codigo, "ruta_documento": p.ruta_documento} for p in proyectos]
    return {"status": "success", "proyectos": proyectos_listados}

def eliminar_proyecto_api(nombre):
    from ..projects_management.project_manager import eliminar_proyecto
    # La función original imprime, la API debe devolver el estado.
    proyectos_antes = len(cargar_proyectos())
    eliminar_proyecto(nombre)
    proyectos_despues = len(cargar_proyectos())
    
    if proyectos_antes == proyectos_despues:
        return {"status": "error", "message": f"El proyecto '{nombre}' no se encontró."}
    return {"status": "success", "message": f"Proyecto '{nombre}' eliminado exitosamente."}

# --- API de Análisis (Modificada y Extendida) ---

def analizar_documentacion_api(proyecto_nombre):
    """
    Analiza la documentación de un proyecto usando OBST con términos dinámicos.
    """
    proyecto = next((p for p in cargar_proyectos() if p.nombre == proyecto_nombre), None)
    if not proyecto:
        return {"status": "error", "message": "Proyecto no encontrado"}

    # --- CORRECCIÓN CLAVE ---
    # Ahora usamos la generación dinámica de términos y probabilidades.
    terminos, p, q = obtener_probabilidades_de_documento(proyecto.ruta_documento)

    if not terminos:
        return {"status": "error", "message": "No se pudieron extraer términos clave del documento."}

    costo, root_table = optimal_bst(terminos, p, q)

    return {
        "status": "success",
        "proyecto": proyecto.nombre,
        "terminos_analizados": terminos,
        "costo_obst": costo
    }

def comparar_archivos_codigo_api(ruta_archivo1, ruta_archivo2):
    """
    Compara dos archivos de código (rutas absolutas) usando LCS ponderada.
    """
    if not os.path.exists(ruta_archivo1) or not os.path.exists(ruta_archivo2):
        return {"status": "error", "message": "Uno o ambos archivos no existen."}

    with open(ruta_archivo1, 'r', encoding='utf-8') as f1, open(ruta_archivo2, 'r', encoding='utf-8') as f2:
        codigo1 = f1.read()
        codigo2 = f2.read()

    tokens1 = tokenize_code(codigo1)
    tokens2 = tokenize_code(codigo2)
    weights = {'keyword': 2.0, 'operator': 1.5, 'identifier': 1.0}
    
    score, lcs_seq, similarity = lcs_weighted(tokens1, tokens2, weights)

    return {
        "status": "success",
        "similitud": similarity,
        "lcs_sequence": lcs_seq,
        "score" : score
    }