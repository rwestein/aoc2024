import unittest
import sys


class Dec10:
    trailheads = []
    sizex = 0
    sizey = 0
    def parse_input(self, inp):
        self.map = []
        for line_ in inp.strip().splitlines():
            if line_.strip():
                self.map.append([int(n) for n in line_.strip()])
        self.sizex = len(self.map[0])
        self.sizey = len(self.map)

    def find_trailheads(self):
        self.trailheads = []
        for x in range(self.sizex):
            for y in range(self.sizey):
                if self.map[y][x] == 0:
                    self.trailheads.append((x, y))

    def has_height(self, x, y, height):
        if 0 <= x < self.sizex and 0 <= y < self.sizey:
            return self.map[y][x] == height
        else:
            return False

    def find_next(self, x, y):
        next_paths = set()
        height = self.map[y][x]
        # print(f'{x}, {y} == {height}')
        if self.has_height(x-1, y, height+1):
            next_paths.add((x-1, y))
        if self.has_height(x+1, y, height+1):
            next_paths.add((x+1, y))
        if self.has_height(x, y-1, height+1):
            next_paths.add((x, y-1))
        if self.has_height(x, y+1, height+1):
            next_paths.add((x, y+1))
        # print(next_paths)
        return next_paths

    def find_paths(self, x, y):
        heads = set()
        height = self.map[y][x]
        if height == 9:
            heads.add((x, y))
        else:
            for posx, posy in self.find_next(x, y):
                new_heads = self.find_paths(posx, posy)
                heads.update(new_heads)
        return heads

    def find_paths2(self, path):
        paths = set()
        x, y = path[-1]
        height = self.map[y][x]
        if height == 9:
            paths.add(path)
        else:
            for posx, posy in self.find_next(x, y):
                new_paths = self.find_paths2(path+((posx, posy),))
                paths.update(new_paths)
                # for new_head in new_heads:
                #     paths.add(path+(new_head,))
        # print(f'find_paths2 = {paths}')
        return paths

    def score_path(self, x, y):
        paths = set()
        for posx, posy in self.find_paths(x, y):
            if self.map[posy][posx] == 9:
                paths.add((posx, posy))
        return len(paths)

    def score_path2(self, head):
        paths = set()
        for ext_path in self.find_paths2((head,)):
            posx, posy = ext_path[-1]
            if self.map[posy][posx] == 9:
                # print(ext_path)
                paths.add(ext_path)
        return len(paths)

    def solve1(self, inp):
        self.parse_input(inp)
        self.find_trailheads()
        total_score = 0
        for trailhead in self.trailheads:
            total_score += self.score_path(trailhead[0], trailhead[1])
        return total_score

    def solve2(self, inp):
        self.parse_input(inp)
        self.find_trailheads()
        total_score = 0
        for trailhead in self.trailheads:
            total_score += self.score_path2(trailhead)
        return total_score


# ****************************************************************************
# Unittests
# ****************************************************************************

class TestDec10(unittest.TestCase):
    EXAMPLE_INPUT = """
    89010123
    78121874
    87430965
    96549874
    45678903
    32019012
    01329801
    10456732
    """

    def setUp(self):
        self.solver = Dec10()

    @staticmethod
    def print(output):
        print(output, end=' ')
        sys.stdout.flush()

    def get_input(self):
        with open('dec10.txt', 'r') as f:
            return f.read()

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 36)

    def test_solution1(self):
        output = self.solver.solve1(self.get_input())
        self.print(output)

    def test_example2(self):
        output = self.solver.solve2(self.EXAMPLE_INPUT)
        self.assertEqual(output, 81)

    def test_solution2(self):
        output = self.solver.solve2(self.get_input())
        self.print(output)


if __name__ == '__main__':
    unittest.main()
