# tests/test_obst_suite.py
import pytest
from src.obst.obst import optimal_bst, reconstruir_arbol
from src.obst.tree_utils import obtener_recorrido_inorden, Node
# --- Fixture de Pytest para Datos Estándar ---

@pytest.fixture
def clrs_example_data():
    """
    Proporciona los datos del ejemplo clásico del libro "Introduction to Algorithms" (CLRS).
    Este es un caso de prueba estándar y bien conocido para el algoritmo OBST.
    
    Retorna:
        dict: Un diccionario con claves, probabilidades p y q, y el costo óptimo esperado.
    """
    return {
        "keys": ['k1', 'k2', 'k3', 'k4', 'k5'],
        "p": [0.15, 0.10, 0.05, 0.10, 0.20],
        "q": [0.05, 0.10, 0.05, 0.05, 0.05, 0.10],
        "expected_cost": 2.75,
        "expected_root_key": 'k2' # La raíz del árbol óptimo para este caso es k2
    }

# --- Conjunto de Pruebas Rigurosas ---

def test_correctitud_con_ejemplo_clrs(clrs_example_data):
    """
    TEST DE CORRECTITUD:
    Verifica que el algoritmo calcula el costo mínimo y la estructura de árbol correctos
    para un ejemplo estándar de la literatura.
    """
    keys = clrs_example_data["keys"]
    p = clrs_example_data["p"]
    q = clrs_example_data["q"]
    expected_cost = clrs_example_data["expected_cost"]
    expected_root_key = clrs_example_data["expected_root_key"]

    cost, root_table = optimal_bst(keys, p, q)

    # 1. Verificar el costo óptimo
    assert abs(cost - expected_cost) < 1e-9, f"El costo calculado {cost} no coincide con el esperado {expected_cost}"

    # 2. Reconstruir el árbol y verificar la raíz principal
    n = len(keys)
    root_node = reconstruir_arbol(root_table, keys, 1, n)
    assert root_node is not None, "El árbol no debería ser nulo"
    assert root_node.key == expected_root_key, f"La raíz esperada era '{expected_root_key}', pero se obtuvo '{root_node.key}'"

    # 3. Verificar la propiedad fundamental de un BST con la función de ayuda
    inorden_list = obtener_recorrido_inorden(root_node)
    assert inorden_list == keys, "El recorrido inorden del árbol reconstruido no coincide con las claves ordenadas"

def test_caso_limite_arbol_vacio():
    """
    TEST DE CASO LÍMITE:
    Verifica el comportamiento del algoritmo cuando no hay claves de entrada.
    El costo debería ser simplemente la probabilidad de búsqueda fallida q[0].
    """
    keys, p = [], []
    q = [0.25]
    
    cost, root_table = optimal_bst(keys, p, q)
    
    # El costo de un árbol sin nodos es la probabilidad del único "hueco"
    assert abs(cost - q[0]) < 1e-9
    
    # La reconstrucción debe devolver un árbol nulo
    arbol = reconstruir_arbol(root_table, keys, 1, len(keys))
    assert arbol is None

def test_caso_limite_un_solo_nodo():
    """
    TEST DE CASO LÍMITE:
    Verifica el algoritmo con una sola clave.
    """
    keys = ['única_clave']
    p = [0.7]
    q = [0.1, 0.2]

    # --- CORRECCIÓN AQUÍ ---
    # El costo esperado es 1*p[0] + 2*q[0] + 2*q[1] = 1.3
    expected_cost = 1.3

    cost, root_table = optimal_bst(keys, p, q)
    arbol = reconstruir_arbol(root_table, keys, 1, len(keys))

    assert abs(cost - expected_cost) < 1e-9
    assert arbol.key == 'única_clave'
    assert arbol.left is None
    assert arbol.right is None

def test_comportamiento_con_probabilidades_sesgadas():
    """
    TEST DE COMPORTAMIENTO INTUITIVO:
    Si una clave tiene una probabilidad de búsqueda abrumadoramente alta,
    debería ser la raíz del árbol óptimo para minimizar el costo promedio.
    """
    keys = ['Bajo_1', 'MUY_PROBABLE', 'Bajo_2']
    p = [0.05, 0.9, 0.05] # La clave central es la más probable
    q = [0.0, 0.0, 0.0, 0.0] # Probabilidades de fallo insignificantes
    
    cost, root_table = optimal_bst(keys, p, q)
    arbol = reconstruir_arbol(root_table, keys, 1, len(keys))
    
    # La raíz del árbol completo (subárbol de 1 a n) debe ser la clave más probable
    assert arbol.key == 'MUY_PROBABLE', "La clave con mayor probabilidad debería ser la raíz."