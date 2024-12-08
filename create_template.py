import datetime
import os

day = datetime.date.today().day

TEMPLATE = f"""import unittest
import sys


class Dec{day}:
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

class TestDec{day}(unittest.TestCase):
    EXAMPLE_INPUT = \"\"\"
    \"\"\"

    def setUp(self):
        self.solver = Dec{day}()

    @staticmethod
    def print(output):
        print(output, end=' ')
        sys.stdout.flush()

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 0)

    # def test_solution1(self):
    #     with open('dec{day}.txt', 'r') as f:
    #         output = self.solver.solve1(f.read())
    #         self.print(output)
    #         self.assertEqual(output, 0)
    #
    # def test_example2(self):
    #     output = self.solver.solve2(self.EXAMPLE_INPUT)
    #     self.assertEqual(output, 0)
    #
    # def test_solution2(self):
    #     with open('dec{day}.txt', 'r') as f:
    #         output = self.solver.solve2(f.read())
    #         self.print(output)
    #         self.assertEqual(output, 0)


unittest.main()
"""

py_file = f'dec{day}.py'
inp_file = f'dec{day}.txt'

if not os.path.exists(py_file):
    with open(py_file, 'w') as f:
        f.write(TEMPLATE)

if not os.path.exists(inp_file):
    with open(inp_file, 'w') as f:
        f.write('')
