import unittest


class BinaryTree:
    ''' Binary tree, indexed in breadth first order:

                            0
                    1               2
                3      4        5       6
               7 8    9 10    11 12   13 14
                ...etc.
    '''

    class Node:

        def __init__(self,
                     key=None,
                     parent=None,
                     left_child=None,
                     right_child=None):
            self.parent = parent
            self.left_child = left_child
            self.right_child = right_child
            self.key = key

    def __init__(self):
        self.root = None

    def key_list(self):
        if self.root is None:
            return []

        keys = [self.root.key]

        return keys

    def __len__(self):
        return len(list(self))

    def __repr__(self):
        return repr(list(self))

    def __str_(self):
        return str(repr(self))

    def __getitem__(self, index):
        return self.key_list()[index]


class TestBinaryTree(unittest.TestCase):

    def test_insert(self):

        pass


if __name__ == '__main__':
    unittest.main()