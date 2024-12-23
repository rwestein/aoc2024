import datetime
import os
import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('day', nargs='?', default=datetime.date.today().day)
args = parser.parse_args()

day = args.day
year = datetime.date.today().year

TEMPLATE = f"""import unittest
import sys


class Dec{day}:
    verbose = True
    
    def parse_input(self, inp):
        self.matrix = []
        for line_ in inp.strip().splitlines():
            if line_.strip():
                self.matrix.append(line_.strip())

    def solve1(self, inp):
        self.parse_input(inp)
        return 0

    def solve2(self, inp):
        self.parse_input(inp)
        return 0


# ****************************************************************************
# Unittests
# ****************************************************************************

class TestDec{day}(unittest.TestCase):
    EXAMPLE_INPUT = \"\"\"
    \"\"\"

    def setUp(self):
        self.solver = Dec{day}()
        self.solver.verbose = '-v' in sys.argv

    def print(self, output):
        if '-v' in sys.argv:
            print(output, end=' ')
            sys.stdout.flush()
        else:
            print(f'{{self.id()}} = {{output}}')

    @staticmethod
    def get_input():
        with open('dec{day}.txt', 'r') as f:
            return f.read()

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 0)

    # def test_solution1(self):
    #     output = self.solver.solve1(self.get_input())
    #     self.print(output)
    #
    # def test_example2(self):
    #     output = self.solver.solve2(self.EXAMPLE_INPUT)
    #     self.assertEqual(output, 0)
    #
    # def test_solution2(self):
    #     output = self.solver.solve2(self.get_input())
    #     self.print(output)


if __name__ == '__main__':
    unittest.main()
"""

# Get the token by looking at session Cookies
token = open('.token.txt').read()

py_file = f'dec{day}.py'
if not os.path.exists(py_file):
    with open(py_file, 'w') as f:
        f.write(TEMPLATE)

inp_file = f'dec{day}.txt'
if not os.path.exists(inp_file):
    response = requests.get(f'https://adventofcode.com/{year}/day/{day}/input', headers={'Cookie': f'session={token}'})
    print(response.text)
    if response.status_code == 200:
        with open(inp_file, 'w') as f:
            f.write(response.text)
