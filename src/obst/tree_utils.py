# src/obst/tree_utils.py
import graphviz
import os

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

def dibujar_arbol(root_node, filename='obst_tree'):
    """
    Dibuja un árbol binario usando Graphviz con alta resolución y lo muestra.
    """
    if not root_node:
        print("El árbol está vacío, no se puede dibujar.")
        return

    output_directory = os.path.join(os.path.dirname(__file__), 'temp_trees')
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    output_path = os.path.join(output_directory, filename)

    # --- MEJORAS DE CALIDAD ---
    dot = graphviz.Digraph(
        comment='Árbol de Búsqueda Binaria Óptimo',
        graph_attr={
            'dpi': '300',  # <-- 1. AUMENTA LA RESOLUCIÓN (DPI)
            'ranksep': '1.0', # <-- 2. AUMENTA LA SEPARACIÓN VERTICAL
            'nodesep': '0.5'  # <-- 3. AUMENTA LA SEPARACIÓN HORIZONTAL
        }
    )

    dot.attr('node', shape='circle', style='filled', fillcolor='lightblue', fontsize='10')
    dot.attr('edge', color='gray')
    dot.attr(rankdir='TB') # Ya no es necesario 'size' al controlar DPI

    def add_nodes_edges(node):
        if node:
            # Para claves muy largas, podemos acortarlas para la visualización
            display_key = (str(node.key)[:10] + '...') if len(str(node.key)) > 10 else str(node.key)
            dot.node(str(id(node)), display_key)
            
            if node.left:
                display_key_left = (str(node.left.key)[:10] + '...') if len(str(node.left.key)) > 10 else str(node.left.key)
                dot.node(str(id(node.left)), display_key_left)
                dot.edge(str(id(node)), str(id(node.left)))
                add_nodes_edges(node.left)
            
            if node.right:
                display_key_right = (str(node.right.key)[:10] + '...') if len(str(node.right.key)) > 10 else str(node.right.key)
                dot.node(str(id(node.right)), display_key_right)
                dot.edge(str(id(node)), str(id(node.right)))
                add_nodes_edges(node.right)

    add_nodes_edges(root_node)
    
    try:
        # Renderiza el gráfico y lo abre. 'cleanup=True' borra los archivos fuente.
        dot.render(output_path, view=True, cleanup=True, format='png')
        print(f"Árbol de alta resolución guardado temporalmente y mostrado.")
    except graphviz.backend.ExecutableNotFound:
        print("\n--- ERROR ---")
        print("Graphviz no encontrado en el PATH del sistema.")
        print("Asegúrate de haber instalado Graphviz y añadido su carpeta 'bin' a las variables de entorno.")
        print("El resultado se mostrará sin el gráfico.")
