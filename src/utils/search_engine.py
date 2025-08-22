# src/utils/search_engine.py

def search_tree(root, key):
    """
    Realiza una búsqueda en el árbol, dado un nodo raíz, y devuelve la profundidad.
    
    :param root: Raíz del árbol
    :param key: Clave que estamos buscando
    :return: Tupla (found, depth) donde `found` es True/False si se encuentra el nodo
             y `depth` es la profundidad del nodo encontrado.
    """
    current_node = root
    depth = 0
    while current_node:
        depth += 1
        if key == current_node.key:
            return True, depth  # Nodo encontrado, devolver profundidad
        elif key < current_node.key:
            current_node = current_node.left
        else:
            current_node = current_node.right
    return False, -1  # Nodo no encontrado, devolver profundidad -1
