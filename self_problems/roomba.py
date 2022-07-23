from cgi import print_form
import unittest
import numpy as np

# Problem:
# - roomba  -- TODO: desc.


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
        print(f"adding {self.position} to cleaned_positions")
        print(f"cleaned_positions before add = {self.cleaned_positions}")
        self.cleaned_positions += [tuple(self.position)]
        print(f"cleaned_positions after add = {self.cleaned_positions}")

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
        print(
            f"---------------------------{DFSAlgorithm.clean_node.stack_frame}-----------------------------"
        )
        DFSAlgorithm.clean_node.stack_frame += 1
        print(
            f"position = {self.position}, direction = {DIRECTION.str(direction)}"
        )
        print(f"moving to position {self.position + direction}")
        if not self.go(direction):
            print(f"couldn't go {DIRECTION.str(direction)}")
            return
        print(f"cleaning new position = {self.position}")
        self.clean()
        return_direction = -direction
        print(f"return_direction = {DIRECTION.str(return_direction)}")
        child_directions = [
            d for d in DIRECTION.ALL
            if not np.array_equal(d, return_direction)
            and not tuple(self.position +
                          d) in self.cleaned_positions + self.blocked_positions
        ]
        print(
            f"child_directions = {[DIRECTION.str(c) for c in child_directions]}"
        )
        for c in child_directions:
            print(f"recursing on child direction {DIRECTION.str(c)}")
            self.clean_node(c)
        if not self.go(return_direction):
            print("PANIC!!!")
            exit()

    def clean_room(self):
        self.clean_node(DIRECTION.NONE)


DFSAlgorithm.clean_node.stack_frame = 0


class TestDFSAlgorithm(unittest.TestCase):
    '''
      0 1 2 3 4
     -1 0 1 2 3
      ---------
 0 -1|0 0 1 0 0
 1  0|0 R 0 1 0
 2  1|0 0 1 0 0
 3  2|0 0 0 0 0
 4  3|0 0 0 0 0
    '''
    ROOM = np.array([[0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 1, 0, 0],
                     [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
    START = np.array([1, 1])

    def test_clean_room(self):
        roomba = Roomba(TestDFSAlgorithm.ROOM, TestDFSAlgorithm.START,
                        DIRECTION.UP)
        algorithm = DFSAlgorithm(roomba)
        algorithm.clean_room()
        print(f"ROOM = \n{TestDFSAlgorithm.ROOM}")
        print(f"roomba.path = {roomba.path}")
        print(f"roomba.cleaned = \n{roomba.cleaned}")
        print(f"roomba.position = {roomba.position}")
        print(f"algorithm.path = {algorithm.path}")
        print(f"algorithm.position = {algorithm.position}")


if __name__ == '__main__':
    unittest.main()
