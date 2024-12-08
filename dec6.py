import copy
import unittest
import sys


class LoopDetectedException(Exception):
    pass

class Dec6:
    posx = 0
    posy = 0
    direction = '^'
    show_progress = False
    def parse_input(self, input):
        matrix = []
        for line_ in input.strip().splitlines():
            if line_.strip():
                matrix.append(list(line_.strip()))
        return matrix

    ROTATE_DIR = {'^': '>', '>': 'v', 'v': '<', '<': '^'}
    DELTA_POS = {'^': (0,-1), '>': (1,0), 'v':(0,1), '<': (-1,0)}

    def determine_position(self):
        self.turns = set()
        self.sizex = len(self.matrix[0])
        self.sizey = len(self.matrix)
        for x in range(self.sizex):
            for y in range(self.sizey):
                if self.matrix[y][x] in self.ROTATE_DIR:
                    self.posx = x
                    self.posy = y
                    self.direction = self.matrix[y][x]

    def store_orig(self):
        self.orig_posx = self.posx
        self.orig_posy = self.posy
        self.orig_dir = self.direction

    def restore_matrix(self):
        self.turns = set()
        self.posx = self.orig_posx
        self.posy = self.orig_posy
        self.direction = self.orig_dir

    # def walk_step(self):
    #     dx, dy = self.DELTA_POS[self.direction]
    #     newx, newy = self.posx+dx, self.posy+dy
    #
    #     if self.matrix[newy][newx] in '#O':
    #         # rotate direction
    #         self.last_turn = self.posx, self.posy, self.direction
    #         self.direction = self.ROTATE_DIR[self.direction]
    #         # self.last_turns.append(self.last_turn)
    #         if self.last_turn in self.turns:
    #             raise LoopDetectedException()
    #         self.turns.add(self.last_turn)
    #     else:
    #         # No obstructions, move forward
    #         if newx < 0 or newx >= self.sizex or newy < 0 or newy >= self.sizey:
    #             raise IndexError('Out of bounds')
    #         self.posx, self.posy = newx, newy
    #         if self.matrix[self.posy][self.posx] == '.':
    #             self.matrix[self.posy][self.posx] = 'X' #'X' if self.turns else '*'
    #
    # def walk_step_no_trace(self):
    #     dx, dy = self.DELTA_POS[self.direction]
    #     newx, newy = self.posx+dx, self.posy+dy
    #
    #     if self.matrix[newy][newx] in '#O':
    #         # rotate direction
    #         self.direction = self.ROTATE_DIR[self.direction]
    #         self.last_turn = self.posx, self.posy, self.direction
    #         if self.last_turn in self.turns:
    #             raise LoopDetectedException()
    #         self.turns.add(self.last_turn)
    #     else:
    #         if newx < 0 or newx >= self.sizex or newy < 0 or newy >= self.sizey:
    #             raise IndexError('Out of bounds')
    #         self.posx, self.posy = newx, newy

    def calculate_new_position(self):
        dx, dy = self.DELTA_POS[self.direction]
        newx, newy = self.posx+dx, self.posy+dy
        return newx, newy

    def rotate_guard(self):
        self.direction = self.ROTATE_DIR[self.direction]
        last_turn = self.posx, self.posy, self.direction
        if last_turn in self.turns:
            raise LoopDetectedException()
        self.turns.add(last_turn)

    def step_towards(self, newx, newy):
        if newx < 0 or newx >= self.sizex or newy < 0 or newy >= self.sizey:
            raise IndexError('Out of bounds')
        self.posx, self.posy = newx, newy

    def mark_current_as_visited(self):
        if self.matrix[self.posy][self.posx] == '.':
            self.matrix[self.posy][self.posx] = 'X'  # 'X' if self.turns else '*'

    def make_move(self, mark_path):
        newx, newy = self.calculate_new_position()
        if self.matrix[newy][newx] in '#O':
            self.rotate_guard()
        else:
            self.step_towards(newx, newy)
            if mark_path:
                self.mark_current_as_visited()

    def print(self):
        print()
        for row in self.matrix:
            print(''.join(row))
        print()

    def walk(self, mark_path):
        while True:
            try:
                self.make_move(mark_path=mark_path)
            except IndexError:
                return False
            except LoopDetectedException:
                return True

    def count_visited(self):
        count = 0
        for x in range(self.sizex):
            for y in range(self.sizey):
                if self.matrix[y][x] in 'X*v^<>':
                    count += 1
        return count

    def solve1(self, input):
        self.matrix = self.parse_input(input)
        self.determine_position()
        self.walk(mark_path=True)
        return self.count_visited()

    def solve2(self, input, print_output=False):
        # Use the X in solution 1 to get to faster results
        self.matrix = self.parse_input(input)
        obstacle_positions = set()
        self.determine_position()
        self.walk(mark_path=True)
        self.visit_matrix = copy.deepcopy(self.matrix)

        obstacles_that_make_loops = 0
        # count = 0
        self.matrix = self.parse_input(input)
        self.determine_position()
        self.store_orig()
        # total = self.sizex*self.sizey
        # percentage = 0
        # if self.show_progress:
        #     print()
        # prev_pos_x, prev_pos_y = None, None
        for y in range(self.sizey):
            for x in range(self.sizex):
                # if prev_pos_x is not None:
                #     self.matrix[prev_pos_y][prev_pos_x] = 'X'
                if (x, y) not in [(97, 24), (97, 27)]:
                    continue
                if self.visit_matrix[y][x] == 'X':
                    self.restore_matrix()
                    self.matrix[y][x] = 'O'
                    if self.walk(mark_path=False):
                        obstacle_positions.add((x,y))
                        self.print()
                        print()

                        obstacles_that_make_loops += 1
                        # if print_output:
                        #     print()
                        #     self.print()
                        #     print()
                    self.matrix[y][x] = 'X'
                    # prev_pos_x, prev_pos_y = x, y
        #         count += 1
        #         if int(count*100/total) > percentage:
        #             percentage = int(count*100/total)
        #             if self.show_progress:
        #                 print(f'{percentage} %  ', end='\r')
        #                 sys.stdout.flush()
        # if self.show_progress:
        #     print()
        # print(sorted(list(obstacle_positions)))
        # print(len(obstacle_positions))
        # f = open('obstacles_all.txt', 'w')
        # for x, y in sorted(list(obstacle_positions)):
        #     f.write(f'{x} {y}\n')
        # f.close()
        return obstacles_that_make_loops



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

    def print(self, output):
        print(output, end=' ')
        sys.stdout.flush()

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 41)

    def test_solution1(self):
        with open('dec6.txt', 'r') as f:
            output = self.solver.solve1(f.read())
            self.solver.print()
            self.print(output)
            self.assertEqual(output, 4883)

    def test_example2(self):
        output = self.solver.solve2(self.EXAMPLE_INPUT)
        self.assertEqual(output, 6)
        # self.solver.print()

    def test_solution2(self):
        # self.solver.show_progress = True
        with open('dec6.txt', 'r') as f:
            output = self.solver.solve2(f.read())
            self.print(output)
            self.assertLess(output, 1658)      # Wrong answer
            self.assertLess(output, 1657)      # Wrong answer
            self.assertEqual(output, 1655)     # Correct answer
            self.assertNotEqual(output, 1652)  # Wrong answer (4th time)

unittest.main()
