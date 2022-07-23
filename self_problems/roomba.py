import unittest
import numpy as np

# Problem:
# - roomba  -- TODO: desc.
# TODO: logger


class DIRECTION:
    'direction in (row,col)'
    UP = np.array([-1, 0])
    DOWN = np.array([1, 0])
    LEFT = np.array([0, -1])
    RIGHT = np.array([0, 1])
    ALL = [UP, RIGHT, DOWN, LEFT]
    NONE = np.array([0, 0])

    def right_of(direction):
        if np.array_equal(direction, DIRECTION.UP):
            return DIRECTION.RIGHT
        elif np.array_equal(direction, DIRECTION.RIGHT):
            return DIRECTION.DOWN
        elif np.array_equal(direction, DIRECTION.DOWN):
            return DIRECTION.LEFT
        elif np.array_equal(direction, DIRECTION.LEFT):
            return DIRECTION.UP

    def left_of(direction):
        if np.array_equal(direction, DIRECTION.UP):
            return DIRECTION.LEFT
        elif np.array_equal(direction, DIRECTION.RIGHT):
            return DIRECTION.UP
        elif np.array_equal(direction, DIRECTION.DOWN):
            return DIRECTION.RIGHT
        elif np.array_equal(direction, DIRECTION.LEFT):
            return DIRECTION.DOWN

    def str(direction):
        if np.array_equal(direction, DIRECTION.UP):
            return "UP"
        elif np.array_equal(direction, DIRECTION.RIGHT):
            return "RIGHT"
        elif np.array_equal(direction, DIRECTION.DOWN):
            return "DOWN"
        elif np.array_equal(direction, DIRECTION.LEFT):
            return "LEFT"
        elif np.array_equal(direction, DIRECTION.NONE):
            return "NONE"
        else:
            return f"UNDEFINED {direction}"


class Roomba:
    'encapsulate problem api constraint'

    def __init__(self, grid, position, direction):
        self.grid = grid
        self.position = position
        self.direction = direction
        self.cleaned = np.zeros(grid.shape)
        self.path = [tuple(self.position)]

    def turn_left(self):
        self.direction = DIRECTION.left_of(self.direction)

    def turn_right(self):
        self.direction = DIRECTION.right_of(self.direction)

    def can_move(self, position):
        rows, cols = self.grid.shape
        row_max = rows - 1
        col_max = cols - 1
        row = position[0]
        col = position[1]
        if row < 0 or row > row_max:
            return False
        if col < 0 or col > col_max:
            return False
        return self.grid[row][col] == 0

    def move(self):
        new_position = self.position + self.direction
        if not self.can_move(new_position):
            return False
        self.position = new_position
        self.path.append(tuple(self.position))
        return True

    def clean(self):
        row = self.position[0]
        col = self.position[1]
        self.cleaned[row][col] = 1


class DFSAlgorithm:
    def __init__(self, roomba):
        self.roomba = roomba
        self.direction = roomba.direction
        self.position = np.array([0, 0])
        self.cleaned_positions = []
        self.blocked_positions = []
        self.path = [tuple(self.position)]

    def turn_right(self):
        self.roomba.turn_right()
        self.direction = DIRECTION.right_of(self.direction)

    def face(self, direction):
        while not np.array_equal(self.direction, direction):
            self.turn_right()

    def clean(self):
        self.roomba.clean()
        self.cleaned_positions += [tuple(self.position)]

    def go(self, direction):
        if np.array_equal(direction, DIRECTION.NONE):
            return True
        self.face(direction)
        if not self.roomba.move():
            self.blocked_positions.append(tuple(self.position + direction))
            return False
        self.position += self.direction
        self.path.append(tuple(self.position))
        return True

    def clean_node(self, direction):
        if not self.go(direction):
            return
        self.clean()
        return_direction = -direction
        child_directions = [
            d for d in DIRECTION.ALL
            if not np.array_equal(d, return_direction)
            and not tuple(self.position +
                          d) in self.cleaned_positions + self.blocked_positions
        ]
        for c in child_directions:
            self.clean_node(c)
        if not self.go(return_direction):
            raise RuntimeError(
                "Unable to return to previous tile. This shouldn't happen!!!")

    def clean_room_recursive(self):
        self.clean_node(DIRECTION.NONE)

    def clean_room_iterative(self):
        all_directions = [tuple(d) for d in DIRECTION.ALL]
        # so we get the same path as the recursive version
        all_directions.reverse()
        stack = all_directions
        while len(stack) != 0:
            if tuple(self.position) not in self.cleaned_positions:
                self.clean()
            direction = np.array(stack.pop())
            if not self.go(direction):
                continue
            return_direction = -direction
            # definitely returning to previous node
            stack.append(tuple(return_direction))
            child_directions = [
                d for d in all_directions
                if d != tuple(return_direction) and not tuple(
                    self.position + np.array(d)) in self.cleaned_positions +
                self.blocked_positions
            ]
            stack += child_directions


class TestDFSAlgorithm(unittest.TestCase):
    '''
             0 1 2 3 4  roomba coord frame
            -1 0 1 2 3  alg coord frame
            ---------
        0 -1|0 0 1 0 0
        1  0|0 R 0 1 0
        2  1|0 0 1 0 0
        3  2|0 0 0 0 0
        4  3|0 0 0 0 0

        R: roomba start position
        0: empty tile
        1: blocked tile
    '''
    ROOM = np.array([[0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
    START = np.array([1, 1])

    def test_clean_room_recursive(self):
        roomba = Roomba(TestDFSAlgorithm.ROOM, TestDFSAlgorithm.START,
                        DIRECTION.UP)
        algorithm = DFSAlgorithm(roomba)
        algorithm.clean_room_recursive()

        # should have cleaned everywhere that's not blocked
        blocked = TestDFSAlgorithm.ROOM == 1
        self.assertTrue(np.array_equal(roomba.cleaned, ~(blocked)))

        # should have finished where we started
        self.assertTrue(np.array_equal(roomba.position,
                                       TestDFSAlgorithm.START))
        self.assertEqual(roomba.path[0], (1, 1))
        self.assertTrue(np.array_equal(algorithm.position, np.array([0, 0])))
        self.assertEqual(algorithm.path[0], (0, 0))

        self.assertEqual(len(algorithm.path), len(roomba.path))
        for i in range(len(algorithm.path)):
            alg_pos = np.array(algorithm.path[i])
            rmb_pos = np.array(roomba.path[i])
            self.assertTrue(
                np.array_equal(alg_pos, rmb_pos - TestDFSAlgorithm.START))
        # print(f"algorithm.path = {algorithm.path}")
        # print(f"roomba.path = {roomba.path}")

    def test_clean_room_iterative(self):
        roomba = Roomba(TestDFSAlgorithm.ROOM, TestDFSAlgorithm.START,
                        DIRECTION.UP)
        algorithm = DFSAlgorithm(roomba)
        algorithm.clean_room_iterative()

        # should have cleaned everywhere that's not blocked
        blocked = TestDFSAlgorithm.ROOM == 1
        self.assertTrue(np.array_equal(roomba.cleaned, ~(blocked)))

        # should have finished where we started
        self.assertTrue(np.array_equal(roomba.position,
                                       TestDFSAlgorithm.START))
        self.assertEqual(roomba.path[0], (1, 1))
        self.assertTrue(np.array_equal(algorithm.position, np.array([0, 0])))
        self.assertEqual(algorithm.path[0], (0, 0))

        self.assertEqual(len(algorithm.path), len(roomba.path))
        for i in range(len(algorithm.path)):
            alg_pos = np.array(algorithm.path[i])
            rmb_pos = np.array(roomba.path[i])
            self.assertTrue(
                np.array_equal(alg_pos, rmb_pos - TestDFSAlgorithm.START))
        # print(f"algorithm.path = {algorithm.path}")
        # print(f"roomba.path = {roomba.path}")


if __name__ == '__main__':
    unittest.main()
