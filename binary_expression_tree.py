
from stack import Stack


class BinaryExpressionTree:
    """A linked positional binary expression tree."""

    OPERATORS = {"+", "-", "*", "/"}

    class _Node:
        def __init__(self, element, parent=None, left=None, right=None):
            self.element = element
            self.parent = parent
            self.left = left
            self.right = right

    class Position:
        """Public position representing a tree node."""

        def __init__(self, tree, node):
            self._tree = tree
            self._node = node

        def element(self):
            return self._node.element

        def __eq__(self, other):
            return (
                isinstance(other, BinaryExpressionTree.Position)
                and self._tree is other._tree
                and self._node is other._node
            )



    def __init__(self, expression=None):
        self._root = None
        self._size = 0

        if expression is not None:
            self.build(expression)

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._root is None

    def _make_position(self, node):
        if node is None:
            return None
        return self.Position(self, node)

    def _validate(self, p):
        if not isinstance(p, self.Position):
            raise TypeError("Expected a Position")



        if p._tree is not self:
            raise ValueError("Position belongs to another tree")
        

        node = p._node

        # Check that this node still belongs to this tree.
        current = node
        seen = set()

        while current.parent is not None:
            if id(current) in seen:
                raise ValueError("Invalid tree structure")
            seen.add(id(current))
            current = current.parent

        if current is not self._root:
            raise ValueError("Position is no longer valid")

        return node

    def root(self):
        return self._make_position(self._root)

    def parent(self, p):
        node = self._validate(p)
        return self._make_position(node.parent)

    def left(self, p):
        node = self._validate(p)
        return self._make_position(node.left)

    def right(self, p):
        node = self._validate(p)
        return self._make_position(node.right)

    def is_leaf(self, p):
        return self.left(p) is None and self.right(p) is None

    def add_root(self, element):
        if not self.is_empty():
            raise ValueError("Root already exists")

        self._root = self._Node(element)
        self._size = 1
        return self.root()


    def attach_subtrees(self, left_tree, right_tree):
        """Transfer two existing subtrees under this root."""
        if self.is_empty() or not self.is_leaf(self.root()):
            raise ValueError("Root must exist and have no children")

        if (
            not isinstance(left_tree, BinaryExpressionTree)
            or not isinstance(right_tree, BinaryExpressionTree)
        ):
            raise TypeError("Both arguments must be trees")


        if (
            left_tree is self
            or right_tree is self
            or left_tree is right_tree
        ):
            
            raise ValueError("Trees must be distinct")

        if left_tree.is_empty() or right_tree.is_empty():
            raise ValueError("Cannot attach empty subtrees")




        self._root.left = left_tree._root
        self._root.right = right_tree._root

        self._root.left.parent = self._root
        self._root.right.parent = self._root

        self._size += len(left_tree) + len(right_tree)

        # Transfer ownership instead of copying nodes.
        left_tree._root = None
        left_tree._size = 0
        right_tree._root = None
        right_tree._size = 0
