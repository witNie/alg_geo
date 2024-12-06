







class BST:
    def __init__(self,val=None, height=0):
        self.value = val
        self.height = height
        if self.value:
            self.left = BST()
            self.right = BST()
        else:
            self.left = None
            self.right = None

    def insert(self, el):
        q = self
        while q.value != None:
            if el < q.value:
                q = q.left
            else:
                q = q.right
        q.value = el
        q.left = BST()
        q.right = BST()

    def get_height(self):

        def rec(q, cnt):

            if q.left == None and q.right == None:
                return cnt
            elif q.left == None:
                return rec(q.right, cnt+1)
            elif q.right == None:
                return rec(q.left, cnt+1)
            else:
                return max(rec(q.right, cnt+1), rec(q.left, cnt+1))
        return rec(self, 0)

    def check_balance(self):
        get_height()

    # def delete(self, el):
    #     q = self
    #     while q.value != None or q.value == el:
    #         if el > q.value:
    #             q = q.right
    #         else:
    #             q = q.left
    #     if q.value:
    #


def visualize_bst(node, level=0, prefix="Root: "):
    """Visualizes the BST in the terminal."""
    if node is not None and node.value is not None:
        print(" " * (4 * level) + prefix + str(node.value))
        if node.left is not None or node.right is not None:
            # Recursively print the left and right subtrees
            visualize_bst(node.left, level + 1, "L--- ")
            visualize_bst(node.right, level + 1, "R--- ")
    elif node is None or node.value is None:
        # Print placeholders for empty nodes
        print(" " * (4 * level) + prefix + "None")







#creating a node in the tree
bst = BST()
bst.insert(10)
bst.insert(5)
bst.insert(15)
bst.insert(7)
print(bst.get_height())
visualize_bst(bst)
