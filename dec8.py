import copy
import unittest
import sys

class Dec8:
    coordinates = []

    def parse_input(self, input):
        matrix = []
        for line_ in input.strip().splitlines():
            if line_.strip():
                matrix.append(line_.strip())
        return matrix

    def convert_map_to_coordinates(self, map):
        self.coordinates = []
        for r, row in enumerate(map):
            for c, signal in enumerate(row):
                if signal != '.':
                    self.coordinates.append((c, r, signal))
        self.sizex = len(map[0])
        self.sizey = len(map)

    def solve1(self, input):
        matrix = self.parse_input(input)
        self.convert_map_to_coordinates(matrix)
        antinodes = set()
        for c1 in self.coordinates:
            for c2 in self.coordinates:
                if c1[2] == c2[2] and c1[0:2] != c2[0:2]:
                    # Create two antinodes
                    antinode1 = 2*c1[0]-c2[0], 2*c1[1]-c2[1]
                    antinode2 = 2*c2[0]-c1[0], 2*c2[1]-c1[1]
                    if 0 <= antinode1[0] < self.sizex and 0 <= antinode1[1] < self.sizey:
                        antinodes.add(antinode1)
                    if 0 <= antinode2[0] < self.sizex and 0 <= antinode2[1] < self.sizey:
                        antinodes.add(antinode2)
        return len(antinodes)

    def solve2(self, input):
        matrix = self.parse_input(input)
        self.convert_map_to_coordinates(matrix)
        antinodes = set()
        for c1 in self.coordinates:
            for c2 in self.coordinates:
                if c1[2] == c2[2] and c1[0:2] != c2[0:2]:
                    for freq in range(-self.sizex, self.sizex):
                        # Create antinodes
                        antinode = c1[0]+freq*(c2[0]-c1[0]), c1[1]+freq*(c2[1]-c1[1])
                        if 0 <= antinode[0] < self.sizex and 0 <= antinode[1] < self.sizey:
                            antinodes.add(antinode)
        return len(antinodes)


# --------------------

class Test(unittest.TestCase):
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

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 14)

    def test_solution1(self):
        with open('dec8.txt', 'r') as f:
            output = self.solver.solve1(f.read())
            print(output)
            self.assertEqual(output, 359)

    def test_example2(self):
        output = self.solver.solve2(self.EXAMPLE_INPUT)
        self.assertEqual(output, 34)

    def test_solution2(self):
        with open('dec8.txt', 'r') as f:
            output = self.solver.solve2(f.read())
            print(output)
            self.assertEqual(output, 1293)     # Correct answer

unittest.main()
