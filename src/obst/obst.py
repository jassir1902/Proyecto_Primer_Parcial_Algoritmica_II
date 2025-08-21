# src/obst/obst.py
from .tree_utils import Node  # Importamos la clase Node y la función imprimir_arbol

def optimal_bst(keys, p, q):
    """
    Calcula el Árbol de Búsqueda Binaria Óptimo (OBST) utilizando programación dinámica.
    
    :param keys: Lista de claves ordenadas (k_1, ..., k_n).
    :param p: Lista de probabilidades de búsqueda para cada clave (p_1, ..., p_n).
    :param q: Lista de probabilidades de búsqueda fallida (q_0, ..., q_n).
    
    :return: Tupla con el costo mínimo esperado (E[1][n]) y la tabla de raíces.
    """
    n = len(keys)

    # Las tablas usan indexado desde 1 para coincidir con el algoritmo.
    # Por eso se crean de tamaño (n+2)x(n+2) o similar.
    E = [[0] * (n + 2) for _ in range(n + 2)]  # Tabla de costos esperados
    W = [[0] * (n + 2) for _ in range(n + 2)]  # Tabla de pesos (suma de probabilidades)
    ROOT = [[0] * (n + 1) for _ in range(n + 1)] # La tabla de raíces solo necesita hasta n

    # Casos base: subárboles vacíos (longitud 0)
    for i in range(1, n + 2):
        E[i][i - 1] = q[i - 1]
        W[i][i - 1] = q[i - 1]

    # Llenado de las tablas para subárboles de longitud 1 hasta n
    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            
            # La suma de probabilidades W[i][j] se calcula eficientemente
            W[i][j] = W[i][j - 1] + p[j - 1] + q[j]
            
            E[i][j] = float('inf')

            # Se buscan todas las posibles raíces 'r' para el subárbol (i, j)
            for r in range(i, j + 1):
                
                # --- PUNTO CRÍTICO DE LA CORRECCIÓN ---
                # Esta es la fórmula de recurrencia. Un error en los índices aquí
                # (p.ej., E[r][j] en lugar de E[r+1][j]) es la causa más probable del fallo.
                cost = E[i][r - 1] + E[r + 1][j] + W[i][j]
                
                if cost < E[i][j]:
                    E[i][j] = cost
                    ROOT[i - 1][j - 1] = r # Ajustamos índices para la tabla ROOT 0-indexada si fuera el caso
                                           # pero la mantendremos 1-indexada por simplicidad.
                                           # Para ello, ROOT debe ser (n+1)x(n+1)
    
    # El resultado final se encuentra en E[1][n]
    return E[1][n], ROOT

def reconstruir_arbol(ROOT, keys, i, j):
    """
    Reconstruye el árbol óptimo de búsqueda binaria (OBST) a partir de la tabla de raíces.

    :param ROOT: Tabla que contiene las raíces de cada subárbol
    :param keys: Lista de claves ordenadas
    :param i: Índice inicial del subárbol
    :param j: Índice final del subárbol

    :return: Nodo raíz del subárbol reconstruido
    """
    if i > j:
        return None
    
    # Los índices de ROOT y keys deben ser consistentes.
    # Si ROOT es 1-indexado (como en este caso), la raíz es ROOT[i-1][j-1] o ROOT[i][j]
    # dependiendo de cómo se construyó. Asumiendo que se guardó como ROOT[i][j].
    # La clave está en keys[r-1] porque `keys` es 0-indexada.
    
    # Esta es una implementación más segura para la reconstrucción:
    if i == 0 or j == 0 or i > len(ROOT) or j > len(ROOT[0]):
         return None # No hay raíz para este rango
    
    r_index = ROOT[i-1][j-1] # Asumimos que ROOT fue llenada 0-indexada
    if r_index == 0:
        return None

    r = keys[r_index - 1]
    nodo = Node(r)
    
    nodo.left = reconstruir_arbol(ROOT, keys, i, r_index - 1)
    nodo.right = reconstruir_arbol(ROOT, keys, r_index + 1, j)

    return nodo

