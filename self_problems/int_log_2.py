import unittest

# Problem: Write algorithm to compute a Log to the base 2 of a number (integral
# results no need for floating point). Solution should not assume a particular
# size of integer.


def lg(x):
    'integer lower bound for log base 2 of input'
    if x <= 0: return None
    prod = 1
    exp = 0
    while prod <= x:
        prod *= 2
        exp += 1
    return exp - 1


class TestLog2(unittest.TestCase):

    def test_lg_undefined(self):
        self.assertEqual(lg(0), None)
        self.assertEqual(lg(-1), None)

    def test_lg_powers_of_2(self):
        self.assertEqual(lg(1), 0)
        self.assertEqual(lg(2), 1)
        self.assertEqual(lg(4), 2)
        self.assertEqual(lg(8), 3)
        self.assertEqual(lg(16), 4)
        self.assertEqual(lg(32), 5)
        self.assertEqual(lg(64), 6)
        self.assertEqual(lg(128), 7)
        self.assertEqual(lg(256), 8)
        self.assertEqual(lg(512), 9)
        self.assertEqual(lg(1024), 10)
        self.assertEqual(lg(2048), 11)
        self.assertEqual(lg(1024 * 1024), 20)
        self.assertEqual(lg(1024 * 1024 * 1024), 30)
        self.assertEqual(lg(1024 * 1024 * 1024 * 1024), 40)
        self.assertEqual(lg(1024 * 1024 * 1024 * 1024 * 1024), 50)


if __name__ == '__main__':
    unittest.main()
