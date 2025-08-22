# src/projects_management/project_manager.py
import os
import json

# Ruta del archivo donde se almacenarán los proyectos
PROJ_FILE_PATH = 'data/proyectos.json'

class Proyecto:
    def __init__(self, nombre, ruta_codigo, ruta_documento):
        self.nombre = nombre  # Nombre del proyecto
        self.ruta_codigo = ruta_codigo  # Ruta a la carpeta de código
        self.ruta_documento = ruta_documento  # Ruta al archivo de documentación

    def to_dict(self):
        """
        Convierte el proyecto a un diccionario para facilitar la serialización a JSON.
        """
        return {
            'nombre': self.nombre,
            'ruta_codigo': self.ruta_codigo,
            'ruta_documento': self.ruta_documento
        }

def cargar_proyectos():
    """
    Carga la lista de proyectos desde el archivo JSON.
    
    :return: Lista de objetos Proyecto
    """
    if os.path.exists(PROJ_FILE_PATH):
        with open(PROJ_FILE_PATH, 'r') as file:
            proyectos_data = json.load(file)
            return [Proyecto(**data) for data in proyectos_data]
    return []

def guardar_proyectos(proyectos):
    """
    Guarda la lista de proyectos en el archivo JSON.
    
    :param proyectos: Lista de objetos Proyecto
    """
    with open(PROJ_FILE_PATH, 'w') as file:
        json.dump([proyecto.to_dict() for proyecto in proyectos], file, indent=4)

def registrar_proyecto(nombre, ruta_codigo, ruta_documento):
    """
    Registra un nuevo proyecto en el sistema.
    
    :param nombre: Nombre del proyecto
    :param ruta_codigo: Ruta a la carpeta que contiene los archivos de código fuente
    :param ruta_documento: Ruta al archivo de documentación asociado
    """
    proyectos = cargar_proyectos()  # Cargar proyectos existentes
    nuevo_proyecto = Proyecto(nombre, ruta_codigo, ruta_documento)
    proyectos.append(nuevo_proyecto)
    guardar_proyectos(proyectos)  # Guardar la lista actualizada de proyectos
    print(f"Proyecto '{nombre}' registrado exitosamente.")

def listar_proyectos():
    """
    Muestra todos los proyectos registrados en el sistema.
    """
    proyectos = cargar_proyectos()
    if proyectos:
        print("Proyectos registrados:")
        for idx, proyecto in enumerate(proyectos, 1):
            print(f"[{idx}] {proyecto.nombre} (Código: {proyecto.ruta_codigo}, Docs: {proyecto.ruta_documento})")
    else:
        print("No hay proyectos registrados.")

def eliminar_proyecto(nombre):
    """
    Elimina un proyecto registrado del sistema.
    
    :param nombre: Nombre del proyecto a eliminar
    """
    proyectos = cargar_proyectos()
    proyectos_filtrados = [proyecto for proyecto in proyectos if proyecto.nombre != nombre]
    
    if len(proyectos) == len(proyectos_filtrados):
        print(f"El proyecto '{nombre}' no se encontró.")
    else:
        guardar_proyectos(proyectos_filtrados)
        print(f"Proyecto '{nombre}' eliminado exitosamente.")
