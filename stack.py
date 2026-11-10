"""This module creates a Stack using a Python list."""


class Stack:
    """A stack that follows Last In, First Out (LIFO)."""

    def __init__(self):
        self._items = []

    def push(self, item):
        """Add an item to the stack."""
        self._items.append(item)

    def pop(self):
        """Remove and return the top item."""
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self._items.pop()

    def peek(self):
        """Return the top item without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack")
        return self._items[-1]

    def is_empty(self):
        """Check if the stack is empty."""
        return len(self._items) == 0

    def size(self):
        """Return the number of items in the stack."""
        return len(self._items)


if __name__ == "__main__":
    stack = Stack()

    # Test an empty stack
    assert stack.is_empty()
    assert stack.size() == 0

    # Test adding items
    stack.push(10)
    stack.push(20)
    stack.push(30)

    assert stack.size() == 3
    assert stack.peek() == 30
    assert stack.size() == 3

    # Test removing items in LIFO order
    assert stack.pop() == 30
    assert stack.pop() == 20
    assert stack.pop() == 10
    assert stack.is_empty()

    # Test popping from an empty stack
    try:
        stack.pop()
    except IndexError:
        print("Empty pop error handled correctly")
    else:
        raise AssertionError("Expected IndexError from pop")

    # Test peeking at an empty stack
    try:
        stack.peek()
    except IndexError:
        print("Empty peek error handled correctly")
    else:
        raise AssertionError("Expected IndexError from peek")

    print("All Stack tests passed!")