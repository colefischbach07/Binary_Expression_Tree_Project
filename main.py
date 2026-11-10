
from binary_expression_tree import BinaryExpressionTree


def main():
    expressions = [
        "5 3 8 * +",
        "8 2 / 3 -",
        "10 5 +",
        "-4 2.5 *",
        "9 3 /",
        "5 +",
        "2 3 4 +",
        "8 0 /",
        "5 hello +",
        ""
    ]

    for expression in expressions:
        print("-" * 40)
        print("Original Postfix:", repr(expression))

        try:
            tree = BinaryExpressionTree(expression)

            print("Infix:", tree.to_infix())
            print("Generated Postfix:", tree.to_postfix())
            print("Result:", tree.evaluate())

        except (ValueError, ZeroDivisionError) as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
