import copy
import unittest
import sys


class Dec6:
    posx = 0
    posy = 0
    direction = '>'
    def parse_input(self, input):
        matrix = []
        for line_ in input.strip().splitlines():
            if line_.strip():
                matrix.append(list(line_.strip()))
        return matrix

    def determine_position(self):
        self.turns = []
        self.sizex = len(self.matrix[0])
        self.sizey = len(self.matrix)
        for x in range(self.sizex):
            for y in range(self.sizey):
                if self.matrix[y][x] in ['v', '^', '<', '>']:
                    self.posx = x
                    self.posy = y
                    self.direction = self.matrix[y][x]
                    self.matrix[y][x] = 'X'

    def check_order(self, produce):
        for i, p1 in enumerate(produce):
            for j, p2 in enumerate(produce):
                if i < j and (p2, p1) in self.order:
                    return False
        return True

    def walk_step(self):
        if self.direction == '^':
            newx = self.posx
            newy = self.posy-1
        elif self.direction == '>':
            newx = self.posx+1
            newy = self.posy
        elif self.direction == 'v':
            newx = self.posx
            newy = self.posy + 1
        elif self.direction == '<':
            newx = self.posx-1
            newy = self.posy

        if self.matrix[newy][newx] == '#':
            # rotate direction
            self.direction = {'^': '>', '>': 'v', 'v': '<', '<': '^'}[self.direction]
            self.turns.append((self.posx, self.posy))
        else:
            self.posx, self.posy = newx, newy
            if self.posx < 0 or self.posy < 0:
                raise IndexError('Out of bounds')
            self.matrix[self.posy][self.posx] = 'X'

    def print(self):
        print()
        for row in self.matrix:
            print(''.join(row))

    def walk(self):
        valid = True
        while valid:
            try:
                self.walk_step()
            except IndexError:
                valid = False
        #self.print()
    def walk2(self):
        valid = True
        while valid:
            try:
                self.walk_step()
                # print(self.turns[-16:])
                for cycle_size in range(0, 100, 2):
                    if len(self.turns) >= 2*cycle_size and self.turns[-2*cycle_size:-cycle_size] == self.turns[-cycle_size:]:
                        return True
                if len(self.turns) > 300:
                    print(self.turns)
                    raise ValueError()
            except IndexError:
                valid = False
        return False

    def count_visited(self):
        count = 0
        for x in range(self.sizex):
            for y in range(self.sizey):
                if self.matrix[y][x] == 'X':
                    count += 1
        return count

    def solve1(self, input):
        self.matrix = self.parse_input(input)
        self.determine_position()
        self.walk()
        return self.count_visited()

    def solve2(self, input):
        loops = 0
        self.matrix = self.parse_input(input)
        self.matrix_copy = copy.deepcopy(self.matrix)
        self.determine_position()
        for x in range(self.sizex):
            for y in range(self.sizey):
                self.matrix = copy.deepcopy(self.matrix_copy)
                # self.matrix = self.parse_input(input)
                self.determine_position()
                if self.matrix[y][x] == '.':
                    self.matrix[y][x] = '#'
                    if self.walk2():
                        loops += 1
                print('.', end='')
                sys.stdout.flush()
        return loops



# --------------------

class Test(unittest.TestCase):
    EXAMPLE_INPUT = """
    ....#.....
    .........#
    ..........
    ..#.......
    .......#..
    ..........
    .#..^.....
    ........#.
    #.........
    ......#...
    """
    def setUp(self):
        self.solver = Dec6()

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 41)
        self.solver.print()

    def test_solution1(self):
        with open('dec6.txt', 'r') as f:
            input = f.read()
            output = self.solver.solve1(input)
            # self.solver.print()
            print(output)

    def test_example2(self):
        output = self.solver.solve2(self.EXAMPLE_INPUT)
        self.assertEqual(output, 6)
        # self.solver.print()

    #
    # def test_example2(self):
    #     output = self.solver.solve2(self.EXAMPLE_INPUT)
    #     self.assertEqual(output, 123)
    #
    def _test_solution2(self):
        with open('dec6.txt', 'r') as f:
            input = f.read()
            output = self.solver.solve2(input)
            print(output)


unittest.main()
