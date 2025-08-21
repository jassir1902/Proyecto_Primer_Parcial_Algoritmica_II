# src/obst/tree_utils.py

class Node:
    """
    Clase para representar un nodo en el árbol binario.
    """
    def __init__(self, key):
        self.key = key  # Clave del nodo
        self.left = None  # Subárbol izquierdo
        self.right = None  # Subárbol derecho

def imprimir_arbol(root):
    """
    Imprime el árbol binario en orden (inorden).
    
    :param root: Raíz del árbol
    """
    if root is not None:
        imprimir_arbol(root.left)
        print(root.key)
        imprimir_arbol(root.right)

def obtener_recorrido_inorden(nodo):
    """
    Realiza un recorrido inorden del árbol y devuelve una lista de claves.
    Esta es la forma correcta de verificar la estructura de un BST.
    """
    resultado = []
    if nodo:
        resultado.extend(obtener_recorrido_inorden(nodo.left))
        resultado.append(nodo.key)
        resultado.extend(obtener_recorrido_inorden(nodo.right))
    return resultado        
