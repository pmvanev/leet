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

    def check_lg(self, x, y):
        self.assertEqual(lg(x), y)
        self.assertEqual(lg(x + 1), y)
        self.assertEqual(lg(2 * x - 1), y)

    def test_lg(self):
        self.assertEqual(lg(1), 0)

        self.check_lg(2, 1)
        self.check_lg(4, 2)
        self.check_lg(8, 3)
        self.check_lg(16, 4)
        self.check_lg(32, 5)
        self.check_lg(64, 6)
        self.check_lg(128, 7)
        self.check_lg(256, 8)
        self.check_lg(512, 9)
        self.check_lg(1024, 10)
        self.check_lg(2048, 11)
        self.check_lg(4096, 12)
        self.check_lg(1024 * 1024, 20)
        self.check_lg(1024 * 1024 * 1024, 30)
        self.check_lg(1024 * 1024 * 1024 * 1024, 40)
        self.check_lg(1024 * 1024 * 1024 * 1024 * 1024, 50)


if __name__ == '__main__':
    unittest.main()
