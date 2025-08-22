# src/integration/main_system.py

import os
from .api import (
    registrar_proyecto_api, listar_proyectos_api, eliminar_proyecto_api,
    analizar_documentacion_api, comparar_archivos_codigo_api, obtener_probabilidades_de_documento, optimal_bst
)

# --- Menús Principales (Sin cambios) ---

def menu_principal():
    while True:
        print("\n=== Sistema de Gestión y Análisis de Proyectos ===")
        print("1. Gestionar Proyectos")
        print("2. Analizar un Proyecto Existente")
        print("3. Herramientas Individuales")
        print("4. Salir")
        opcion = input("Selecciona una opción: ")
        if opcion == '1':
            menu_gestion_proyectos()
        elif opcion == '2':
            menu_analizar_proyecto()
        elif opcion == '3':
            menu_herramientas_individuales()
        elif opcion == '4':
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

def menu_gestion_proyectos():
    while True:
        print("\n--- Gestión de Proyectos ---")
        print("1. Registrar Proyecto")
        print("2. Listar Proyectos")
        print("3. Eliminar Proyecto")
        print("4. Volver al Menú Principal")
        opcion = input("Selecciona una opción: ")
        if opcion == '1':
            registrar_nuevo_proyecto()
        elif opcion == '2':
            listar_proyectos()
        elif opcion == '3':
            eliminar_proyecto_por_nombre()
        elif opcion == '4':
            break
        else:
            print("Opción no válida.")

# --- Funciones de Gestión (Ligeramente ajustadas para usar la API) ---

def registrar_nuevo_proyecto():
    nombre = input("Nombre del proyecto: ")
    ruta_codigo = input("Ruta de la carpeta de código: ")
    ruta_documento = input("Ruta del archivo de documentación: ")
    response = registrar_proyecto_api(nombre, ruta_codigo, ruta_documento)
    print(response['message'])

def listar_proyectos():
    response = listar_proyectos_api()
    if response['status'] == 'success' and response['proyectos']:
        print("\nProyectos registrados:")
        for p in response['proyectos']:
            print(f"- {p['nombre']} (Código: {p['ruta_codigo']}, Docs: {p['ruta_documento']})")
    else:
        print("No hay proyectos registrados.")

def eliminar_proyecto_por_nombre():
    nombre = input("Nombre del proyecto a eliminar: ")
    response = eliminar_proyecto_api(nombre)
    print(response['message'])

# --- Flujo de Análisis de Proyectos (Reestructurado) ---

def menu_analizar_proyecto():
    response = listar_proyectos_api()
    proyectos = response.get('proyectos', [])
    if not proyectos:
        print("No hay proyectos para analizar. Por favor, registra uno primero.")
        return

    print("\nProyectos disponibles:")
    for idx, p in enumerate(proyectos, 1):
        print(f"[{idx}] {p['nombre']}")
    
    try:
        seleccion = int(input("Selecciona el proyecto a analizar (o 0 para volver): "))
        if seleccion == 0: return
        proyecto_seleccionado = proyectos[seleccion - 1]
        
        print(f"\nAnalizando '{proyecto_seleccionado['nombre']}':")
        print("a. Analizar Documentación (OBST)")
        print("b. Comparar Archivos de Código (LCS)")
        opcion_analisis = input("Elige una opción: ").lower()

        if opcion_analisis == 'a':
            resultado = analizar_documentacion_api(proyecto_seleccionado['nombre'])
            if resultado['status'] == 'success':
                print(f"\nAnálisis OBST completado:")
                print(f"  - Costo óptimo de búsqueda: {resultado['costo_obst']:.4f}")
                print(f"  - {len(resultado['terminos_analizados'])} términos analizados: {', '.join(resultado['terminos_analizados'])}")
            else:
                print(f"Error: {resultado['message']}")
        
        elif opcion_analisis == 'b':
            analizar_codigo_de_proyecto(proyecto_seleccionado)

    except (ValueError, IndexError):
        print("Selección no válida.")

def analizar_codigo_de_proyecto(proyecto):
    """
    Nuevo flujo para seleccionar y comparar archivos de un proyecto.
    """
    ruta_codigo = proyecto['ruta_codigo']
    try:
        archivos_py = [f for f in os.listdir(ruta_codigo) if f.endswith('.py')]
        if not archivos_py:
            print("No se encontraron archivos .py en el directorio del proyecto.")
            return

        print("\nArchivos de código en el proyecto:")
        for idx, f in enumerate(archivos_py, 1):
            print(f"[{idx}] {f}")

        seleccion = int(input("Selecciona el PRIMER archivo para comparar: "))
        archivo1_path = os.path.join(ruta_codigo, archivos_py[seleccion - 1])

        archivo2_path = input("Ingresa la ruta completa del SEGUNDO archivo (puede ser de dentro o fuera del proyecto): ")
        
        resultado = comparar_archivos_codigo_api(archivo1_path, archivo2_path)

        if resultado['status'] == 'success':
            print("\nAnálisis LCS completado:")
            print(f"  - Similitud: {resultado['similitud']:.2%}")
            print(f"  - Secuencia Común Más Larga (LCS): {' '.join(resultado['lcs_sequence'])}")
        else:
            print(f"Error: {resultado['message']}")

    except (ValueError, IndexError, FileNotFoundError):
        print("Error en la selección o ruta de archivo.")

# --- Herramientas Individuales (Completado) ---

def menu_herramientas_individuales():
    """
    Menú completado para usar las herramientas de forma independiente.
    """
    while True:
        print("\n--- Herramientas Individuales ---")
        print("1. Análisis de Documento (OBST)")
        print("2. Comparación de Código (LCS)")
        print("3. Volver al Menú Principal")
        opcion = input("Selecciona una herramienta: ")

        if opcion == '1':
            ruta_doc = input("Ingresa la ruta del archivo de documentación (.pdf): ")
            if not os.path.exists(ruta_doc):
                print("Error: El archivo no existe.")
                continue
            
            # Usamos la misma lógica que la API, pero de forma directa
            terminos, p, q = obtener_probabilidades_de_documento(ruta_doc)
            if not terminos:
                print("No se pudieron extraer términos clave del documento.")
                continue
            
            costo, _ = optimal_bst(terminos, p, q)
            print("\nAnálisis OBST completado:")
            print(f"  - Costo óptimo de búsqueda: {costo:.4f}")
            print(f"  - {len(terminos)} términos analizados: {', '.join(terminos)}")

        elif opcion == '2':
            archivo1 = input("Ruta del primer archivo de código: ")
            archivo2 = input("Ruta del segundo archivo de código: ")
            resultado = comparar_archivos_codigo_api(archivo1, archivo2)

            if resultado['status'] == 'success':
                print("\nAnálisis LCS completado:")
                print(f"  - Similitud: {resultado['similitud']:.2%}")
                print(f"  - Secuencia Común Más Larga (LCS): {' '.join(resultado['lcs_sequence'])}")
            else:
                print(f"Error: {resultado['message']}")

        elif opcion == '3':
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    # Asegúrate de que el directorio de datos exista
    if not os.path.exists('data/individual_datasets'):
        os.makedirs('data/individual_datasets')
    menu_principal()