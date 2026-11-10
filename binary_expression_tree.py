
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



    def build(self, expression):
        """Build an expression tree from postfix input."""
        tokens = expression.split()

        if not tokens:
            raise ValueError("Empty expression")

        stack = Stack()

        for token in tokens:
            if token in self.OPERATORS:
                if stack.size() < 2:
                    raise ValueError("Too few operands")

                right_tree = stack.pop()
                left_tree = stack.pop()

                subtree = BinaryExpressionTree()
                subtree.add_root(token)
                subtree.attach_subtrees(left_tree, right_tree)
                stack.push(subtree)

            else:
                try:
                    value = float(token)
                except ValueError:
                    raise ValueError(
                        f"Unsupported token: {token}"
                    ) from None

                import math
                if not math.isfinite(value):
                    raise ValueError(
                        f"Unsupported token: {token}"
                    )

                subtree = BinaryExpressionTree()
                subtree.add_root(token)
                stack.push(subtree)

        if stack.size() != 1:
            raise ValueError("Extra operands / invalid expression")

        completed = stack.pop()

        # Replace this tree only after successful construction.
        self._root = completed._root
        self._size = completed._size
        completed._root = None
        completed._size = 0



    def evaluate(self):
        """Recursively evaluate the expression tree."""
        if self.is_empty():
            raise ValueError("No expression tree")

        def evaluate_at(p):
            token = p.element()

            if self.is_leaf(p):
                return float(token)

            left_value = evaluate_at(self.left(p))
            right_value = evaluate_at(self.right(p))

            if token == "+":
                return left_value + right_value
            if token == "-":
                return left_value - right_value
            if token == "*":
                return left_value * right_value
            if token == "/":
                if right_value == 0:
                    raise ZeroDivisionError("Division by zero")
                return left_value / right_value

            raise ValueError("Unsupported operator")

        return evaluate_at(self.root())



    def to_infix(self):
        """Return a fully parenthesized infix expression."""
        if self.is_empty():
            raise ValueError("No expression tree")

        def infix_at(p):
            if self.is_leaf(p):
                return str(p.element())

            left_text = infix_at(self.left(p))
            right_text = infix_at(self.right(p))

            return (
                f"({left_text} {p.element()} {right_text})"
            )

        return infix_at(self.root())



    def to_postfix(self):
        """Return the expression in postfix order."""
        if self.is_empty():
            raise ValueError("No expression tree")

        return " ".join(
            str(p.element()) for p in self.postorder()
        )



    def preorder(self):
        """Visit root, left, right."""
        if not self.is_empty():
            yield from self._preorder(self.root())

    def _preorder(self, p):
        yield p

        left = self.left(p)
        right = self.right(p)

        if left is not None:
            yield from self._preorder(left)

        if right is not None:
            yield from self._preorder(right)



    def inorder(self):
        """Visit left, root, right (without parentheses)."""
        if not self.is_empty():
            yield from self._inorder(self.root())

    def _inorder(self, p):
        left = self.left(p)
        right = self.right(p)

        if left is not None:
            yield from self._inorder(left)

        yield p

        if right is not None:
            yield from self._inorder(right)



    def postorder(self):
        """Visit left, right, root."""
        if not self.is_empty():
            yield from self._postorder(self.root())

    def _postorder(self, p):
        left = self.left(p)
        right = self.right(p)

        if left is not None:
            yield from self._postorder(left)

        if right is not None:
            yield from self._postorder(right)

        yield p
