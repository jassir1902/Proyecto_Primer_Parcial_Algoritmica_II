# src/integration/api.py

import os
from ..projects_management.project_manager import cargar_proyectos
from ..obst.obst import optimal_bst, reconstruir_arbol
from ..lcs_detector.lcs_weighted import lcs_weighted
from ..lcs_detector.comparator import CodeComparator 
from ..utils.probability_calculator import obtener_probabilidades_de_documento
from ..obst.tree_utils import dibujar_arbol

# --- API de Gestión de Proyectos ---

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

    # Ahora usamos la generación dinámica de términos y probabilidades.
    terminos, p, q = obtener_probabilidades_de_documento(proyecto.ruta_documento)

    if not terminos:
        return {"status": "error", "message": "No se pudieron extraer términos clave del documento."}

    costo, root_table = optimal_bst(terminos, p, q)

    # 2. Reconstruir el árbol a partir de la tabla de raíces
    print("Reconstruyendo el árbol para visualización...")
    n = len(terminos)
    arbol_reconstruido_root = reconstruir_arbol(root_table, terminos, 1, n)

    # 3. Dibujar el árbol reconstruido
    if arbol_reconstruido_root:
        print("Iniciando la visualización del árbol...")
        # El nombre del archivo puede ser dinámico para no sobreescribir
        nombre_archivo_arbol = f"obst_{proyecto_nombre}" 
        dibujar_arbol(arbol_reconstruido_root, filename=nombre_archivo_arbol)
    else:
        print("No se pudo reconstruir el árbol para dibujarlo.")

    return {
        "status": "success",
        "proyecto": proyecto.nombre,
        "terminos_analizados": terminos,
        "costo_obst": costo
    }



def comparar_archivos_codigo_api(ruta_archivo1: str, ruta_archivo2: str, custom_weights: dict = None):
    """
    Compara dos archivos de código usando la nueva arquitectura `CodeComparator`.

    Args:
        ruta_archivo1 (str): Ruta absoluta al primer archivo.
        ruta_archivo2 (str): Ruta absoluta al segundo archivo.
        custom_weights (dict, optional): Un diccionario de pesos personalizado para
                                          sobrescribir los pesos por defecto en esta
                                          comparación específica.
    """
    if not os.path.exists(ruta_archivo1) or not os.path.exists(ruta_archivo2):
        return {"status": "error", "message": "Uno o ambos archivos no existen."}

    try:
        with open(ruta_archivo1, 'r', encoding='utf-8') as f1, open(ruta_archivo2, 'r', encoding='utf-8') as f2:
            codigo1 = f1.read()
            codigo2 = f2.read()
    except Exception as e:
        return {"status": "error", "message": f"Error al leer los archivos: {e}"}

    # 1. Instanciamos el comparador. Si se pasan pesos personalizados, los usamos.
    comparator = CodeComparator(weights=custom_weights)
    
    # 2. Llamamos al método `compare` que encapsula toda la lógica.
    resultado = comparator.compare(codigo1, codigo2)
    
    # 3. Devolvemos una respuesta unificada.
    return {
        "status": "success",
        "score": resultado["similarity_score"],
        "lcs_normalized": resultado["common_sequence"] # La secuencia de tokens normalizados
    }