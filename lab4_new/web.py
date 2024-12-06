class Node:
    def __init__(self, value, parent=None):
        self.value = value
        self.parent = parent
        self.left = None
        self.right = None
        self.height = 1

    def left_height(self):
        # Get the heigth of the left subtree
        return 0 if self.left is None else self.left.height

    def right_height(self):
        # Get the height of the right subtree
        return 0 if self.right is None else self.right.height

    def balance_factor(self):
        # Get the balance factor
        return self.left_height() - self.right_height()

    def update_heigth(self):
        # Update the heigth of this node
        self.height = 1 + max(self.left_height(), self.right_height())

    def set_left(self, node):
        # Set the left child
        self.left = node
        if node is not None:
            node.parent = self
        self.update_heigth()

    def set_right(self, node):
        # Set the right child
        self.right = node
        if node is not None:
            node.parent = self
        self.update_heigth()

    def is_left_child(self):
        # Check whether this node is a left child
        return self.parent is not None and self.parent.left == self

    def is_right_child(self):
        # Check whether this node is a right child
        return self.parent is not None and self.parent.right == self


class Tree:
    def __init__(self):
        self.root = None
        self.size = 0

    # Inside the AVLTree class

    def rotate_left(self, a):
        b = a.right
        # 1. The new right child of A becomes the left child of B
        a.set_right(b.left)
        # 2. The new left child of B becomes A
        b.set_left(a)
        return b  # 3. Return B to replace A with it

    # Inside the AVLTree class


    def rotate_right(self, a):
        b = a.left
        a.set_left(b.right)
        b.set_right(a)
        return b

    def rebalance(self, node):

        if node is None:
            # Empty tree, no rebalancing needed
            return None
        balance = node.balance_factor()
        if abs(balance) <= 1:
            # The node is already balanced, no rebalancing needed
            return node
        if balance == 2:
            # Cases 1 and 2, the tree is leaning to the left
            if node.left.balance_factor() == -1:
                # Case 2, we first do a left rotation
                node.set_left(self.rotate_left(node.left))
            return self.rotate_right(node)
        # Balance must be -2
        # Cases 3 and 4, the tree is leaning to the left
        if node.right.balance_factor() == 1:
            # Case 4, we first do a right rotation
            node.set_right(self.rotate_right(node.right))
        return self.rotate_left(node)


    def add(self, value):
        self.size += 1
        parent = None
        current = self.root
        while current is not None:
            parent = current
            if value < current.value:
                # Value to insert is smaller than node value, go left
                current = current.left
            else:
                # Value to insert is larger than node value, go right
                current = current.right
        # We found the parent, create the new node
        new_node = Node(value, parent)
        # Case 1: The parent is None so the new node is the root
        if parent is None:
            self.root = new_node
        else:
            # Case 2: Set the new node as a child of the parent
            if value < parent.value:
                parent.left = new_node
            else:
                parent.right = new_node
        # After a new node is added, we need to restore balance
        self.restore_balance(new_node)

    # Inside the AVLTree class


    def restore_balance(self, node):
        current = node
        # Go up the tree and rebalance left and right children
        while current is not None:
            current.set_left(self.rebalance(current.left))
            current.set_right(self.rebalance(current.right))
            current.update_heigth()
            current = current.parent
        self.root = self.rebalance(self.root)
        self.root.parent = None

    def find_lower(self, y):


