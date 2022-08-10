from lib2to3.pytree import Node
import unittest

class Node:
    def __init__(self, key=None, left_child=None, right_child=None):
        self.left_child = left_child
        self.right_child = right_child
        self.key = key

    def children(self):
        return [self.left_child, self.right_child]

class BinaryTree:
    ''' Binary tree, indexed in breadth first order:

                            0
                    1               2
                3      4        5       6
               7 8    9 10    11 12   13 14
                ...etc.
    '''
    def __init__(self, keys):
        self.root = None 
        for key in keys:
            self.add_key(key)

    def key_list(self):
        keys = []
        nodes_to_visit = [self.root]

        while len(nodes_to_visit) != 0:
            current_node = nodes_to_visit.pop(0)
            if current_node is None:
                continue
            keys.append(current_node.key)
            nodes_to_visit += current_node.children()

        return keys

    def __len__(self):
        return len(list(self))

    def __repr__(self):
        return repr(list(self))

    def __str_(self):
        return str(repr(self))

    def __getitem__(self, index):
        return self.key_list()[index]

    def add_key(self, key):
        if self.root == None:
            self.root = Node(key)
            return
        nodes_to_visit = [self.root]
        while len(nodes_to_visit) != 0:
            current_node = nodes_to_visit.pop(0)
            if not current_node.left_child:
                current_node.left_child = Node(key)
                return
            elif not current_node.right_child:
                current_node.right_child = Node(key)
                return
            else:
                nodes_to_visit += current_node.children()

    def add_keys(self, keys):
        # TODO: more efficient add of multiple keys
        pass

class TestBinaryTree(unittest.TestCase):
    def test_add_keys(self):
        key_list = [0,1,2,3,4,5,6,7,8,9,10]
        binary_tree = BinaryTree(key_list)
        self.assertEqual(binary_tree.key_list(), key_list)



if __name__ == '__main__':
    unittest.main()