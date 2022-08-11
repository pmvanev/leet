import unittest

class Node:
    def __init__(self, key=None, left_child=None, right_child=None):
        self.left_child = left_child
        self.right_child = right_child
        self.key = key

    def children(self):
        return [self.left_child, self.right_child]

    def add_child(self, node):
        if not self.left_child:
            self.left_child = node
        elif not self.right_child:
            self.right_child = node
        else:
            raise RuntimeError("node already full, can't add child")

    def has_vacancy(self):
        return None in self.children()

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
        if self.root is None:
            self.root = Node(key)
            return
        nodes_to_visit = []
        current_node = self.root
        while not current_node.has_vacancy():
            nodes_to_visit += current_node.children()
            current_node = nodes_to_visit.pop(0)
        current_node.add_child(Node(key))
        
class TestBinaryTree(unittest.TestCase):
    def test_add_keys(self):
        key_list = [0,1,2,3,4,5,6,7,8,9,10]
        binary_tree = BinaryTree(key_list)
        self.assertEqual(binary_tree.key_list(), key_list)



if __name__ == '__main__':
    unittest.main()