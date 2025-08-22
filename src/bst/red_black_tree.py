# src/bst/red_black_tree.py (Versión Corregida)

class RBNode:
    def __init__(self, key, color="red"):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = color

class RedBlackTree:
    def __init__(self):
        self.TNULL = RBNode(0)
        self.TNULL.color = "black"
        self.root = self.TNULL

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.TNULL: # Ahora esta condición funcionará siempre
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.TNULL: # Y esta también
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def fix_insert(self, k):
        while k.parent.color == "red":
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.rotate_left(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self.rotate_right(k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == "red":
                    u.color = "black"
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.rotate_right(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self.rotate_left(k.parent.parent)
            if k == self.root:
                break
        self.root.color = "black"

    def insert(self, key):
        """
        Inserta un nuevo nodo con la clave dada en el árbol rojo-negro.
        """
        node = RBNode(key)
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = "red" # Los nodos nuevos son rojos

        y = self.TNULL
        x = self.root

        while x != self.TNULL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y == self.TNULL:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        # Si el nuevo nodo es la raíz, simplemente lo coloreamos de negro.
        if node.parent == self.TNULL:
            node.color = "black"
            return

        # Si el abuelo es TNULL, no hay posible violación de la propiedad rojo-rojo.
        if node.parent.parent == self.TNULL:
            return

        # Arregla el árbol si se violan las propiedades.
        self.fix_insert(node)

    def search(self, key):
        node = self.root
        while node != self.TNULL:
            if key == node.key:
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return False