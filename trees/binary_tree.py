import os
import unittest

serial_file_delimiter = ', '
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

    def _serialize_to(self, serial_file, node):
        if node is None:
            serial_file.write('None' + serial_file_delimiter)
            return
        serial_file.write(str(node.key) + serial_file_delimiter)
        for child_node in node.children():
            self._serialize_to(serial_file, child_node)

    def serialize_to_file(self, filename):
        'serialize to csv file of keys in depth first order'
        with open(filename, 'w') as serial_file:
            self._serialize_to(serial_file, self.root)

    @staticmethod
    def deserialize_to(depth_first_list, node):
        if len(depth_first_list) <= 2: # list ends with two 'None's
            return 
        left_key = depth_first_list.pop(0)
        if left_key != str(None):
            node.left_child = Node(int(left_key))
            BinaryTree.deserialize_to(depth_first_list, node.left_child)
        right_key = depth_first_list.pop(0)
        if right_key != str(None):
            node.right_child = Node(int(right_key))
            BinaryTree.deserialize_to(depth_first_list, node.right_child)

    def deserialize_from_list(self, depth_first_list):
        if len(depth_first_list) == 0 or depth_first_list[0] == str(None):
            return 
        self.root = Node(int(depth_first_list.pop(0)))
        self.deserialize_to(depth_first_list, self.root)
        
        
    @staticmethod
    def deserialize_from_file(serial_filename):
        'deserialize csv file of keys in depth first order'
        with open(serial_filename, 'r') as serial_file:
            depth_first_list = serial_file.readline().split(serial_file_delimiter)[:-1] 
            depth_first_list = depth_first_list[:-1] # cut off trailing space from final delimeter
        binary_tree = BinaryTree([])
        binary_tree.deserialize_from_list(depth_first_list)
        return binary_tree

class TestBinaryTree(unittest.TestCase):
    def test_add_keys(self):
        key_list = [0,1,2,3,4,5,6,7,8,9]
        binary_tree = BinaryTree(key_list)
        self.assertEqual(binary_tree.key_list(), key_list)

    def test_serialize(self):
        key_list = [0,1,2,3,4,5,6,7,8,9]
        expected_serialization = '0, 1, 3, 7, None, None, 8, None, None, 4, 9, None, None, None, 2, 5, None, None, 6, None, None, '
        start_tree = BinaryTree(key_list)
        serial_filename = 'serial.csv'
        start_tree.serialize_to_file(serial_filename)
        with open(serial_filename) as f:
            self.assertEqual(f.readline(), expected_serialization)
        end_tree = BinaryTree.deserialize_from_file(serial_filename)
        self.assertEqual(start_tree.key_list(), end_tree.key_list())
        os.system(f"rm {serial_filename}")


if __name__ == '__main__':
    unittest.main()