import unittest
import sys


class Dec12:
    matrix = [[]]
    sizex = 0
    sizey = 0
    verbose = False

    def parse_input(self, inp):
        matrix = []
        for line_ in inp.strip().splitlines():
            if line_.strip():
                matrix.append(line_.strip())
        self.matrix = matrix
        self.sizex = len(self.matrix[0])
        self.sizey = len(self.matrix)

    def matches(self, x, y, plant):
        if 0<=x<self.sizex and 0<=y<self.sizey:
            m = self.matrix[y][x] == plant and not self.visited[y][x]
            if m:
                self.visited[y][x] = True
            return m
        else:
            return False

    def matches2(self, x, y, plant):
        if 0<=x<self.sizex and 0<=y<self.sizey:
            m = self.matrix[y][x] == plant and (x,y) in self.region
            return m
        else:
            return False

    def extend_perimeter(self, x, y, plant):
        count = 0
        if self.matches2(x+1, y, plant): count += 1
        if self.matches2(x-1, y, plant): count += 1
        if self.matches2(x, y+1, plant): count += 1
        if self.matches2(x, y-1, plant): count += 1
        if count == 1:
            return 2
        elif count == 2:
            return 0
        elif count == 3:
            return -2
        else:
            raise ValueError(f'Perimeter extension of plant {plant} with {count} neighbors on position {x}, {y} not expected')

    def extend_sides(self, x, y, plant):
        # nw n ne
        # w  c  e
        # sw s se

        # 1 group to extend:
        # 1,0 1,1 1,2 2,1 1,2 3,2 2,2 2,3 3,3 4,3
        # ... ... o.. oo. ooo oo. oo. ooo ooo ooo
        # on. on. on. on. .n. on. on. on. ono ono
        # ... o.. o.. ... ... oo. o.. o.. o.. oo.
        #  0   2   4  -2   4  -4   0   2  -2  -4

        # Multiple groups to extend:
        # 1,3 1,3 2,1
        # ooo o.o .o.
        # .n. .n. on.
        # o.. oo. ..o
        #  4   2  -2  -4   -2

        n = self.matches2(x, y-1, plant)
        e = self.matches2(x+1, y, plant)
        w = self.matches2(x-1, y, plant)
        s = self.matches2(x, y+1, plant)
        count = sum([n, e, w, s])

        nw = self.matches2(x-1, y-1, plant)
        ne = self.matches2(x+1, y-1, plant)
        sw = self.matches2(x-1, y+1, plant)
        se = self.matches2(x+1, y+1, plant)
        diag = sum([nw, ne, sw, se])



        mapping = {(1, 0): 0,
                   (1, 1): 2,
                   (2, 1): -2,
                   (1, 2): 4,
                   (1, 3): 2,
                   (2, 3): 2,
                   (3, 3): -2,
                   (2, 2): 0,
                   (2, 0): 2,
                   (3, 2): -4,
                   (4, 3): -4,
                   }
        # if plant == 'R':
        #     print(f'{x}, {y}, ({count}, {diag}) ->, {mapping[count, diag]}')
        return mapping[count, diag]

    def find_region(self, startx, starty):
        self.region = [(startx, starty)]
        self.visited[starty][startx] = True
        plant = self.matrix[starty][startx]
        area = 1
        perimeter = 4
        added = 1
        while added:
            added = 0
            for x, y in self.region:
                if self.matches(x+1, y, plant):
                    self.region.append((x+1, y))
                    area += 1
                    added += 1
                    perimeter += self.extend_perimeter(x+1, y, plant)
                if self.matches(x-1, y, plant):
                    self.region.append((x-1, y))
                    area += 1
                    added += 1
                    perimeter += self.extend_perimeter(x-1, y, plant)
                if self.matches(x, y+1, plant):
                    self.region.append((x, y+1))
                    area += 1
                    added += 1
                    perimeter += self.extend_perimeter(x, y+1, plant)
                if self.matches(x, y-1, plant):
                    self.region.append((x, y-1))
                    area += 1
                    added += 1
                    perimeter += self.extend_perimeter(x, y-1, plant)
        # print(plant, area, perimeter)
        return area, perimeter, plant

    def find_region2(self, startx, starty):
        self.region = [(startx, starty)]
        self.visited[starty][startx] = True
        plant = self.matrix[starty][startx]
        area = 1
        sides = 4
        added = 1
        while added:
            added = 0
            for x, y in self.region:
                if self.matches(x+1, y, plant):
                    self.region.append((x+1, y))
                    area += 1
                    added += 1
                    sides += self.extend_sides(x+1, y, plant)
                if self.matches(x-1, y, plant):
                    self.region.append((x-1, y))
                    area += 1
                    added += 1
                    sides += self.extend_sides(x-1, y, plant)
                if self.matches(x, y+1, plant):
                    self.region.append((x, y+1))
                    area += 1
                    added += 1
                    sides += self.extend_sides(x, y+1, plant)
                if self.matches(x, y-1, plant):
                    self.region.append((x, y-1))
                    area += 1
                    added += 1
                    sides += self.extend_sides(x, y-1, plant)

        return area, sides, plant

    def mark_unvisited(self):
        self.visited = []
        for y in range(self.sizey):
            self.visited.append([])
            for x in range(self.sizex):
                self.visited[-1].append(False)

    def find_regions(self):
        regions = []
        self.mark_unvisited()
        for x in range(self.sizex):
            for y in range(self.sizey):
                if not self.visited[y][x]:
                    area, perimeter, plant = self.find_region(x, y)
                    if self.verbose:
                        print(plant, area, perimeter)
                    regions.append((area, perimeter))
        return regions

    def find_regions2(self):
        regions = []
        self.mark_unvisited()
        for x in range(self.sizex):
            for y in range(self.sizey):
                if not self.visited[y][x]:
                    area, sides, plant = self.find_region2(x,y)
                    # if self.verbose:
                    #     print(plant, area, sides)
                    regions.append((area, sides))
        return regions

    def solve1(self, inp):
        self.parse_input(inp)
        total = 0
        regions = self.find_regions()
        for area, perimeter in regions:
            total += area * perimeter
        return total

    def solve2(self, inp):
        self.parse_input(inp)
        total = 0
        regions = self.find_regions2()
        for area, sides in regions:
            total += area * sides
        return total


# ****************************************************************************
# Unittests
# ****************************************************************************

class TestDec12(unittest.TestCase):
    EXAMPLE_INPUT = """
    RRRRIICCFF
    RRRRIICCCF
    VVRRRCCFFF
    VVRCCCJFFF
    VVVVCJJCFE
    VVIVCCJJEE
    VVIIICJJEE
    MIIIIIJJEE
    MIIISIJEEE
    MMMISSJEEE
    """
    EXAMPLE_INPUT2 = """
    OOOOO
    OXOXO
    OOOOO
    OXOXO
    OOOOO
    """
    EXAMPLE_INPUT3 = """
    AAAAAA
    AAABBA
    AAABBA
    ABBAAA
    ABBAAA
    AAAAAA
    """

    def setUp(self):
        self.solver = Dec12()

    def print(self, output):
        if '-v' in sys.argv:
            print(output, end=' ')
            sys.stdout.flush()
        else:
            print(f'{self.id()} = {output}')

    @staticmethod
    def get_input():
        with open('dec12.txt', 'r') as f:
            return f.read()

    def test_example1a(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 1930)

    def test_example1b(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT2)
        self.assertEqual(output, 772)

    def test_solution1(self):
        output = self.solver.solve1(self.get_input())
        self.print(output)

    def test_example2(self):
        output = self.solver.solve2(self.EXAMPLE_INPUT)
        self.assertEqual(output, 1206)

    def test_example2b(self):
        self.solver.verbose = True
        output = self.solver.solve2(self.EXAMPLE_INPUT3)
        self.assertEqual(output, 368)

    def test_solution2(self):
        output = self.solver.solve2(self.get_input())
        self.print(output)
        self.assertLess(output, 879236)  # Wrong input
        self.assertLess(output, 877724)  # Also wrong input
        self.assertLess(output, 875298)  # Third wrong attempt


if __name__ == '__main__':
    unittest.main()
