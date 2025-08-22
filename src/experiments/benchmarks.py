# src/experiments/benchmarks.py

import time
import random
from ..bst.avl_tree import AVLTree
from ..bst.red_black_tree import RedBlackTree
from ..utils.search_engine import search_tree
from ..obst.obst import optimal_bst
from ..utils.probability_calculator import obtener_probabilidades_de_documento

# --- CONFIGURACIÓN DEL BENCHMARK ---
# 1. Cambia esta ruta al archivo PDF que quieras analizar.
#    Usa rutas absolutas para evitar problemas, ej: "C:/Users/TuUsuario/documentos/mi_libro.pdf"
#RUTA_PDF = 'C:/Users/DELL/OneDrive/Escritorio/Algoritmica II/Trabajo primer parcial.pdf' 
#RUTA_PDF = 'C:/Users/DELL/OneDrive/Escritorio/Algoritmica II/Cormen, Thomas H._ Leiserson, Charles E._ Rivest, Ronald L._ Ste - Introduction to Algorithms (202.pdf' 
#RUTA_PDF = 'C:/Users/DELL/OneDrive/Escritorio/Algoritmica II/Proyecto_Primer_Parcial/docs/reporte_final.pdf' 
RUTA_PDF = 'C:/Users/DELL/OneDrive/Escritorio/Algoritmica II/Proyecto_Primer_Parcial/data/general_datasets/07-ABB.pdf' 

# 2. Define cuántos de los términos más comunes del PDF quieres usar en el benchmark.
TOP_N_TERMINOS = 5000

# 3. Define qué porcentaje de la probabilidad total corresponde a búsquedas exitosas.
#    Por ejemplo, 0.90 significa que el 90% de las búsquedas encontrarán una clave.
PROBABILIDAD_EXITO_TOTAL = 0.90
# --- FIN DE LA CONFIGURACIÓN ---


def ejecutar_benchmark_con_datos_reales():
    """
    Ejecuta el benchmark completo usando datos extraídos de un documento PDF.
    """
    print("="*60)
    print(f"🚀 Iniciando Benchmark con datos reales del PDF:")
    print(f"   - Documento: {RUTA_PDF}")
    print(f"   - Usando los {TOP_N_TERMINOS} términos más comunes.")
    print("="*60)

    # --- 1. Generación de Datos ---
    print("\n[Paso 1/3] Extrayendo y procesando datos del PDF...")
    try:
        claves, p, q = obtener_probabilidades_de_documento(
            RUTA_PDF, 
            top_n=TOP_N_TERMINOS, 
            prob_exito_total=PROBABILIDAD_EXITO_TOTAL
        )
    except FileNotFoundError:
        print(f"\n❌ ERROR CRÍTICO: No se pudo encontrar el archivo PDF en la ruta especificada.")
        print(f"   Por favor, verifica que la ruta '{RUTA_PDF}' sea correcta.")
        return # Detiene la ejecución si el archivo no existe.

    if not claves:
        print("\n❌ ERROR CRÍTICO: No se pudieron extraer claves del documento.")
        print("   Asegúrate de que el PDF contenga texto seleccionable y que NLTK esté bien configurado.")
        return

    print(f"   -> Se han extraído {len(claves)} claves únicas para el benchmark.")
    print(f"   -> Suma de probabilidades 'p' (éxito): {sum(p):.4f}")
    print(f"   -> Suma de probabilidades 'q' (fallo): {sum(q):.4f}")

    # --- 2. Tiempos de Construcción ---
    print("\n[Paso 2/3] Midiendo tiempos de construcción de los árboles...")
    
    # OBST (Cálculo)
    start_time = time.time()
    costo_obst_teorico, _ = optimal_bst(claves, p, q)
    tiempo_obst = time.time() - start_time
    print(f"   - OBST (Cálculo):      {tiempo_obst:.6f}s")
    
    # Crear una copia aleatoria de las claves para una inserción más realista
    claves_aleatorias = list(claves)
    random.shuffle(claves_aleatorias)

    # AVL (Inserción)
    avl_tree = AVLTree()
    start_time = time.time()
    for clave in claves_aleatorias:
        avl_tree.insert(clave)
    tiempo_avl = time.time() - start_time
    print(f"   - AVL (Inserción):       {tiempo_avl:.6f}s")
    
    # Red-Black (Inserción)
    rb_tree = RedBlackTree()
    start_time = time.time()
    for clave in claves_aleatorias:
        rb_tree.insert(clave)
    tiempo_rb = time.time() - start_time
    print(f"   - Red-Black (Inserción): {tiempo_rb:.6f}s")

    # --- 3. Costos de Búsqueda ---
    print("\n[Paso 3/3] Calculando costos de búsqueda esperados...")
    
    # Costo teórico del OBST (el óptimo)
    print(f"   - OBST Costo Teórico:      {costo_obst_teorico:.6f}")
    
    # Costo real del AVL
    costo_avl_real = 0
    for i, clave in enumerate(claves):
        found, depth = search_tree(avl_tree.root, clave)
        if found:
            costo_avl_real += depth * p[i]
    print(f"   - AVL Costo Real:          {costo_avl_real:.6f}")
    
    # Costo real del Red-Black
    costo_rb_real = 0
    for i, clave in enumerate(claves):
        found, depth = search_tree(rb_tree.root, clave)
        if found:
            costo_rb_real += depth * p[i]
    print(f"   - Red-Black Costo Real:    {costo_rb_real:.6f}")
    print("\n" + "="*60)
    print("✅ Benchmark Finalizado.")
    print("="*60)


if __name__ == "__main__":
    ejecutar_benchmark_con_datos_reales()