import unittest
import sys


class Dec9:
    def parse_input(self, inp):
        matrix = []
        for line_ in inp.strip().splitlines():
            if line_.strip():
                matrix.append(line_.strip())
        return matrix

    def solve1(self, inp):
        matrix = self.parse_input(inp)
        return 0

    def solve2(self, inp):
        matrix = self.parse_input(inp)
        return 0


# ****************************************************************************
# Unittests
# ****************************************************************************

class TestDec9(unittest.TestCase):
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
        self.solver = Dec9()

    @staticmethod
    def print(output):
        print(output, end=' ')
        sys.stdout.flush()

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 14)

    # def test_solution1(self):
    #     with open('dec9.txt', 'r') as f:
    #         output = self.solver.solve1(f.read())
    #         self.print(output)
    #         self.assertEqual(output, 359)
    #
    # def test_example2(self):
    #     output = self.solver.solve2(self.EXAMPLE_INPUT)
    #     self.assertEqual(output, 34)
    #
    # def test_solution2(self):
    #     with open('dec9.txt', 'r') as f:
    #         output = self.solver.solve2(f.read())
    #         self.print(output)
    #         self.assertEqual(output, 1293)


if __name__ == '__main__':
    unittest.main()
