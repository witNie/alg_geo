class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

class BSTTree:
    def __init__(self):
        self.root = None

    def insert(self, node, key):
        if not node:
            return Node(key)

        if key < node.key:
            node.left = self.insert(node.left, key)
        elif key > node.key:
            node.right = self.insert(node.right, key)
        else:
            return node

        return node

    def delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self.delete(node.left, key)
        elif key > node.key:
            node.right = self.delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            temp = self.get_min_value_node(node.right)
            node.key = temp.key
            node.right = self.delete(node.right, temp.key)

        if not node:
            return node

        return node

    def get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def get_predecessor(self, node, key):
        predecessor = None
        while node:
            if key > node.key:
                predecessor = node
                node = node.right
            else:
                node = node.left
        return predecessor.key if predecessor else None

    def get_successor(self, node, key):
        successor = None
        while node:
            if key < node.key:
                successor = node
                node = node.left
            else:
                node = node.right
        return successor.key if successor else None

    def in_order_traversal(self, node):
        if node:
            self.in_order_traversal(node.left)
            print(node.key, end=" ")
            self.in_order_traversal(node.right)

    def insert_key(self, key):
        self.root = self.insert(self.root, key)

    def delete_key(self, key):
        self.root = self.delete(self.root, key)

    def print_tree(self):
        self.in_order_traversal(self.root)
        print()

