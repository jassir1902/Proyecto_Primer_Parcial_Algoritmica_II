# tests/project_manager_test.py

import pytest
import os
import json
from src.projects_management.project_manager import (
    registrar_proyecto,
    cargar_proyectos,
    eliminar_proyecto,
    listar_proyectos,
    Proyecto
)

# --- Fixture de Pytest para un Entorno de Pruebas Limpio ---

@pytest.fixture
def setup_test_environment(tmp_path, monkeypatch):
    """
    Este fixture es la clave para probar código que interactúa con archivos.
    1. `tmp_path`: Crea un directorio temporal único para esta ejecución de prueba.
    2. `monkeypatch`: Nos permite modificar de forma segura variables globales,
       como la ruta al archivo JSON, para que apunte a nuestro directorio temporal.
    """
    # Crear una ruta de archivo temporal dentro del directorio temporal
    temp_proj_file = tmp_path / "proyectos_test.json"
    
    # Usar monkeypatch para que el project_manager use nuestro archivo temporal
    # en lugar del real.
    monkeypatch.setattr('src.projects_management.project_manager.PROJ_FILE_PATH', str(temp_proj_file))
    
    # Devolvemos la ruta para que los tests puedan usarla si es necesario
    return str(temp_proj_file)


# --- Conjunto de Pruebas ---

def test_registrar_y_cargar_proyectos(setup_test_environment):
    """
    TEST DE FUNCIONALIDAD BÁSICA:
    Verifica que se puedan registrar proyectos y que se carguen correctamente.
    """
    # Registrar dos proyectos
    registrar_proyecto("Proyecto Alpha", "/path/code/a", "/path/doc/a.md")
    registrar_proyecto("Proyecto Beta", "/path/code/b", "/path/doc/b.md")
    
    # Cargar los proyectos desde el archivo
    proyectos = cargar_proyectos()
    
    # Verificaciones
    assert len(proyectos) == 2
    assert proyectos[0].nombre == "Proyecto Alpha"
    assert proyectos[1].ruta_codigo == "/path/code/b"

def test_eliminar_proyecto_existente(setup_test_environment):
    """
    TEST DE ELIMINACIÓN:
    Verifica que un proyecto existente pueda ser eliminado.
    """
    # Estado inicial
    registrar_proyecto("Proyecto 1", "ruta1", "doc1")
    registrar_proyecto("Proyecto 2", "ruta2", "doc2")
    
    # Eliminar uno de los proyectos
    eliminar_proyecto("Proyecto 1")
    
    # Cargar y verificar
    proyectos = cargar_proyectos()
    assert len(proyectos) == 1
    assert proyectos[0].nombre == "Proyecto 2"

def test_eliminar_proyecto_inexistente(setup_test_environment, capsys):
    """
    TEST DE CASO DE ERROR CONTROLADO:
    Verifica que el sistema maneje correctamente el intento de eliminar
    un proyecto que no existe.
    `capsys` es un fixture de pytest que captura la salida de print().
    """
    registrar_proyecto("Proyecto Original", "ruta_og", "doc_og")
    
    # Intentar eliminar un proyecto que no está en la lista
    eliminar_proyecto("Proyecto Fantasma")
    
    # Verificar que la lista de proyectos no haya cambiado
    proyectos = cargar_proyectos()
    assert len(proyectos) == 1
    
    # Verificar que se imprimió el mensaje de error correcto
    captured = capsys.readouterr()
    assert "no se encontró" in captured.out

def test_cargar_proyectos_sin_archivo(setup_test_environment):
    """
    TEST DE CASO LÍMITE:
    Verifica que `cargar_proyectos` devuelva una lista vacía si el archivo JSON no existe.
    """
    # En este punto, setup_test_environment ha preparado la ruta, pero el archivo
    # aún no ha sido creado porque no hemos guardado nada.
    proyectos = cargar_proyectos()
    assert proyectos == []

def test_listar_proyectos(setup_test_environment, capsys):
    """
    TEST DE SALIDA DE USUARIO:
    Verifica que la función `listar_proyectos` imprima la lista correctamente.
    """
    registrar_proyecto("Proyecto de Lista", "/code/list", "/doc/list.md")
    
    listar_proyectos()
    
    captured = capsys.readouterr()
    # Verificamos que la salida contenga la información clave
    assert "Proyectos registrados:" in captured.out
    assert "Proyecto de Lista" in captured.out
    assert "/code/list" in captured.out

def test_listar_proyectos_vacio(setup_test_environment, capsys):
    """
    TEST DE SALIDA DE USUARIO (CASO LÍMITE):
    Verifica que se muestre el mensaje correcto cuando no hay proyectos.
    """
    listar_proyectos()
    
    captured = capsys.readouterr()
    assert "No hay proyectos registrados" in captured.out