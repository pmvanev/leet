import unittest

# Problem: implement fifo queue
# Constraint: you may only use stacks


class TwoStackFifoQueue:

    def __init__(self):
        self.head_stack = []
        self.tail_stack = []

    def enqueue(self, item):
        self.head_stack.append(item)

    def dequeue(self):
        if len(self.tail_stack) != 0:
            return self.tail_stack.pop()

        if len(self.head_stack) == 0:
            return None

        while len(self.head_stack) != 0:
            self.tail_stack.append(self.head_stack.pop())

        return self.dequeue()

    def to_list(self):
        return (self.tail_stack[::-1] + self.head_stack)

    def __len__(self):
        return len(self.to_list())

    def __repr__(self):
        return repr(list(self))

    def __str_(self):
        return str(repr(self))

    def __getitem__(self, index):
        return self.to_list()[index]


class TestTwoStackFifoQueue(unittest.TestCase):

    def test_enqueue(self):
        q = TwoStackFifoQueue()
        numbers = [1, 2, 3, 4, 5]
        for num in numbers:
            q.enqueue(num)
        self.assertEqual(list(q), numbers)
        self.assertEqual(q.to_list(), numbers)
        self.assertEqual(len(q), len(numbers))

    def test_enqueue(self):
        q = TwoStackFifoQueue()

        self.assertEqual(q.dequeue(), None)

        numbers = [1, 2, 3, 4, 5]
        for num in numbers:
            q.enqueue(num)

        self.assertEqual(q.dequeue(), 1)
        self.assertEqual(list(q), [2, 3, 4, 5])

        self.assertEqual(q.dequeue(), 2)
        self.assertEqual(list(q), [3, 4, 5])

        self.assertEqual(q.dequeue(), 3)
        self.assertEqual(list(q), [4, 5])

        q.enqueue(6)
        self.assertEqual(list(q), [4, 5, 6])

        q.enqueue(7)
        self.assertEqual(list(q), [4, 5, 6, 7])

        self.assertEqual(q.dequeue(), 4)
        self.assertEqual(list(q), [5, 6, 7])

        self.assertEqual(q.dequeue(), 5)
        self.assertEqual(list(q), [6, 7])

        self.assertEqual(q.dequeue(), 6)
        self.assertEqual(list(q), [7])

        self.assertEqual(q.dequeue(), 7)
        self.assertEqual(list(q), [])

        self.assertEqual(q.dequeue(), None)


if __name__ == '__main__':
    unittest.main()