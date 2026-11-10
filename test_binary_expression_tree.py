
import unittest
from binary_expression_tree import BinaryExpressionTree





class TestBinaryExpressionTree(unittest.TestCase):
    def test_basic_addition(self):
        tree = BinaryExpressionTree("5 3 +")
        self.assertAlmostEqual(tree.evaluate(), 8.0)

    def test_nested_operators(self):
        tree = BinaryExpressionTree("5 3 8 * +")
        self.assertAlmostEqual(tree.evaluate(), 29.0)
        self.assertEqual(tree.to_infix(), "(5 + (3 * 8))")

    def test_operand_order(self):
        tree = BinaryExpressionTree("8 2 / 3 -")
        self.assertAlmostEqual(tree.evaluate(), 1.0)

    def test_negative_decimal(self):
        tree = BinaryExpressionTree("-4 2.5 *")
        self.assertAlmostEqual(tree.evaluate(), -10.0)


    def test_too_few_operands(self):
        with self.assertRaises(ValueError):
            BinaryExpressionTree("5 +")

    def test_extra_operands(self):
        with self.assertRaises(ValueError):
            BinaryExpressionTree("2 3 4 +")


    def test_division_by_zero(self):
        tree = BinaryExpressionTree("8 0 /")
        with self.assertRaises(ZeroDivisionError):
            tree.evaluate()

    def test_empty_expression(self):
        with self.assertRaises(ValueError):
            BinaryExpressionTree("")


    def test_unsupported_token(self):
        with self.assertRaises(ValueError):
            BinaryExpressionTree("5 hello +")

    def test_postfix_output(self):
        expression = "5 3 8 * +"
        tree = BinaryExpressionTree(expression)
        self.assertEqual(
            tree.to_postfix().split(),
            expression.split()
        )

    def test_traversals(self):
        tree = BinaryExpressionTree("5 3 8 * +")

        preorder = [p.element() for p in tree.preorder()]
        inorder = [p.element() for p in tree.inorder()]
        postorder = [p.element() for p in tree.postorder()]

        self.assertEqual(preorder, ["+", "5", "*", "3", "8"])
        self.assertEqual(inorder, ["5", "+", "3", "*", "8"])
        self.assertEqual(postorder, ["5", "3", "8", "*", "+"])


    def test_parent_links(self):
        tree = BinaryExpressionTree("5 3 +")
        root = tree.root()

        self.assertEqual(tree.left(root).element(), "5")
        self.assertEqual(tree.right(root).element(), "3")
        self.assertEqual(tree.parent(tree.left(root)), root)




if __name__ == "__main__":
    unittest.main()
