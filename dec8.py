import unittest
import sys

class Dec8:
    coordinates = []
    sizex = 0
    sizey = 0

    @staticmethod
    def parse_input(inp):
        matrix = []
        for line_ in inp.strip().splitlines():
            if line_.strip():
                matrix.append(line_.strip())
        return matrix

    def convert_map_to_coordinates(self, matrix):
        self.coordinates = []
        for r, row in enumerate(matrix):
            for c, signal in enumerate(row):
                if signal != '.':
                    self.coordinates.append((c, r, signal))
        self.sizex = len(matrix[0])
        self.sizey = len(matrix)

    def create_antinodes(self, freq_range):
        antinodes = set()
        for c1 in self.coordinates:
            for c2 in self.coordinates:
                if c1[2] == c2[2] and c1[0:2] != c2[0:2]:
                    for freq in freq_range:
                        antinode = c1[0]+freq*(c2[0]-c1[0]), c1[1]+freq*(c2[1]-c1[1])
                        if 0 <= antinode[0] < self.sizex and 0 <= antinode[1] < self.sizey:
                            antinodes.add(antinode)
        return antinodes

    def solve1(self, inp):
        matrix = self.parse_input(inp)
        self.convert_map_to_coordinates(matrix)
        antinodes = self.create_antinodes([-1, 2])
        return len(antinodes)

    def solve2(self, inp):
        matrix = self.parse_input(inp)
        self.convert_map_to_coordinates(matrix)
        antinodes = self.create_antinodes(range(-self.sizex, self.sizex))
        return len(antinodes)


# ****************************************************************************
# Unittests
# ****************************************************************************

class TestDec8(unittest.TestCase):
    EXAMPLE_INPUT = """
    ............
    ........0...
    .....0......
    .......0....
    ....0.......
    ......A.....
    ............
    ............
    ........A...
    .........A..
    ............
    ............
    """
    def setUp(self):
        self.solver = Dec8()

    def print(self, output):
        print(output, end=' ')
        sys.stdout.flush()

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 14)

    def test_solution1(self):
        with open('dec8.txt', 'r') as f:
            output = self.solver.solve1(f.read())
            self.print(output)
            self.assertEqual(output, 359)

    def test_example2(self):
        output = self.solver.solve2(self.EXAMPLE_INPUT)
        self.assertEqual(output, 34)

    def test_solution2(self):
        with open('dec8.txt', 'r') as f:
            output = self.solver.solve2(f.read())
            self.print(output)
            self.assertEqual(output, 1293)


if __name__ == '__main__':
    unittest.main()
