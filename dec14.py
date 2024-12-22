import unittest
import sys


class Dec14:
    matrix = [[]]
    sizex = 101
    sizey = 103

    def __init__(self, sizex=101, sizey=103):
        self.sizex = sizex
        self.sizey = sizey
        self.create_empty_matrix()

    def parse_coordinate(self, text):
        x, y = text.strip().split('=')[1].split(',')
        return int(x), int(y)

    def parse_input(self, inp):
        self.robots = []
        for line_ in inp.strip().splitlines():
            if line_.strip():
                position, velocity = line_.split()
                position = self.parse_coordinate(position)
                velocity = self.parse_coordinate(velocity)
                self.robots.append((position, velocity))

    def create_empty_matrix(self):
        self.matrix = []
        for i in range(self.sizey):
            self.matrix.append([0]*self.sizex)

    def place_robots(self, steps=100):
        for position, velocity in self.robots:
            endx = (position[0] + velocity[0] * steps) % self.sizex
            endy = (position[1] + velocity[1] * steps) % self.sizey
            self.matrix[endy][endx] += 1

    def count_quadrant(self, posx, posy, sizex, sizey):
        total = 0
        for x in range(posx, sizex):
            for y in range(posy, sizey):
                total += self.matrix[y][x]
        return total

    def row_to_string(self, row):
        return ''.join([(str(c) if c > 0 else '.') for c in row])

    def print_matrix(self):
        for row in self.matrix:
            print(self.row_to_string(row))

    def count_quadrants(self):
        quadrant_counts = [0, 0, 0, 0]
        quadrant_counts[0] = self.count_quadrant(0, 0, int((self.sizex-1)/2), int((self.sizey-1)/2))
        quadrant_counts[1] = self.count_quadrant(int((self.sizex+1)/2), 0, self.sizex, int((self.sizey-1)/2))
        quadrant_counts[2] = self.count_quadrant(0, int((self.sizey+1)/2), int((self.sizex-1)/2), self.sizey)
        quadrant_counts[3] = self.count_quadrant(int((self.sizex+1)/2), int((self.sizey+1)/2), self.sizex, self.sizey)
        return quadrant_counts

    def solve1(self, inp):
        self.parse_input(inp)
        self.place_robots()
        # self.print_matrix()
        q1, q2, q3, q4 = self.count_quadrants()
        return q1 * q2 * q3 * q4

    def check_all_lines_symmetric(self):
        for row in self.matrix:
            if row[:int((self.sizex-1)/2)] != reversed(row[int((self.sizex-1)/2):]):
                return False
        return True

    def detect_easteregg(self):
        for row in self.matrix:
            if '11111111' in self.row_to_string(row):
                return True
        return False

    def solve2(self, inp):
        self.parse_input(inp)
        for steps in range(18000):
            self.create_empty_matrix()
            self.place_robots(steps=steps)
            if self.detect_easteregg():
                print(steps)
                print(f'After {steps}:')
                self.print_matrix()
                print(f'Above was after {steps}')
                print()
                solution = steps
        return solution


# ****************************************************************************
# Unittests
# ****************************************************************************

class TestDec14(unittest.TestCase):
    EXAMPLE_INPUT = """
    p=0,4 v=3,-3
    p=6,3 v=-1,-3
    p=10,3 v=-1,2
    p=2,0 v=2,-1
    p=0,0 v=1,3
    p=3,0 v=-2,-2
    p=7,6 v=-1,-3
    p=3,0 v=-1,-2
    p=9,3 v=2,3
    p=7,3 v=-1,2
    p=2,4 v=2,-3
    p=9,5 v=-3,-3
    """

    def setUp(self):
        self.solver = Dec14()

    def print(self, output):
        if '-v' in sys.argv:
            print(output, end=' ')
            sys.stdout.flush()
        else:
            print(f'{self.id()} = {output}')

    @staticmethod
    def get_input():
        with open('dec14.txt', 'r') as f:
            return f.read()

    def test_example1(self):
        self.solver = Dec14(sizex=11, sizey=7)
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 12)

    def test_solution1(self):
        output = self.solver.solve1(self.get_input())
        self.print(output)

    def test_solution2(self):
        output = self.solver.solve2(self.get_input())
        self.print(output)


if __name__ == '__main__':
    unittest.main()
