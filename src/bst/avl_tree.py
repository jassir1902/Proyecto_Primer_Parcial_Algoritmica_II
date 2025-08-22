# src/bst/avl_tree.py

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1  # Altura del nodo

class AVLTree:
    def __init__(self):
        self.root = None

    def _height(self, node):
        return node.height if node else 0

    def _balance_factor(self, node):
        return self._height(node.left) - self._height(node.right)

    def _update_height(self, node):
        node.height = 1 + max(self._height(node.left), self._height(node.right))

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self._update_height(y)
        self._update_height(x)
        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self._update_height(x)
        self._update_height(y)
        return y

    def _rebalance(self, node):
        balance = self._balance_factor(node)
        if balance > 1:  # Left heavy
            if self._balance_factor(node.left) < 0:  # Left-Right case
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1:  # Right heavy
            if self._balance_factor(node.right) > 0:  # Right-Left case
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node  # No balancing needed

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)
        self._update_height(node)
        return self._rebalance(node)

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def search(self, key):
        node = self.root
        while node:
            if key == node.key:
                return True
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return False
