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


class Roomba:
    'encapsulate problem api constraint'

    #TODO: implement for grid design
    def __init__(self, grid, position, direction):
        self.grid = grid
        self.position = position
        self.direction = direction
        self.cleaned = np.zeros(grid.shape)
        self.path = [self.position]

    def turn_left(self):
        self.direction = DIRECTION.left_of(self.direction)

    def turn_right(self):
        self.direction = DIRECTION.right_of(self.direction)

    def can_move(self, position):
        # TODO: extract self.grid.in_bounds(postion)
        rows, cols = self.grid.shape
        row_max = rows - 1
        col_max = cols - 1
        row = position[0]
        col = position[1]
        if row < 0 or row > row_max:
            return False
        if col < 0 or col > col_max:
            return False
        # TODO: extract self.grid.is_open(position)
        return self.grid[row][col] == 0
        # TODO: return self.grid.is_space(position) -> grid.in_bounds(p) and grid.is_open(p)

    def move(self):
        new_position = self.position + self.direction
        if not self.can_move(new_position):
            return False
        self.position = new_position
        self.path.append(self.position)
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
        self.path = [self.position]

    def turn_right(self):
        self.roomba.turn_right()
        self.direction = DIRECTION.right_of(self.direction)

    def face(self, direction):
        # TODO: check for left turn
        while not np.array_equal(self.direction, direction):
            self.turn_right()

    def go(self, direction):
        if np.array_equal(direction, DIRECTION.NONE):
            return True
        self.face(direction)
        if not self.roomba.move():
            return False
        self.position += direction
        self.path.append(self.position)

    def already_cleaned(self, position):
      for cleaned_position in self.cleaned_positions:
        if np.array_equal(position, cleaned_position):
          return True
      return False

    def try_go(self, direction):
        if self.already_cleaned(self.position + direction):
            return False
        return self.go(direction)

    def clean(self):
        self.roomba.clean()
        self.cleaned_positions.append(self.position)

    def clean_path(self, direction):
        if not self.try_go(direction):
            return
        self.clean()
        return_direction = -direction
        child_directions = [
            d for d in DIRECTION.ALL
            if not np.array_equal(d, return_direction)
        ]
        for d in child_directions:
            self.clean_path(d)
        self.go(return_direction)

    def clean_room(self):
        self.clean_path(DIRECTION.NONE)


class TestDFSAlgorithm(unittest.TestCase):
    '''
      0 0 1 0 0
      0 X 0 1 0
      0 0 1 0 0
      0 0 0 0 0
      0 0 0 0 0
    '''
    ROOM_1 = np.array([[0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 1, 0, 0],
                       [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])
    START_1 = np.array([1, 1])

    def test_clean_room(self):
        roomba = Roomba(TestDFSAlgorithm.ROOM_1, TestDFSAlgorithm.START_1,
                        DIRECTION.UP)
        algorithm = DFSAlgorithm(roomba)
        algorithm.clean_room()
        print(roomba.path)
        print(roomba.cleaned)
        print(roomba.position)
        print(algorithm.path)


if __name__ == '__main__':
    unittest.main()
