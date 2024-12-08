import copy
import unittest
import sys


class Dec7:
    def parse_input(self, input):
        lines = []
        for line_ in input.strip().splitlines():
            if line_.strip() and ':' in line_:
                result, parts = line_.strip().split(':')
                result = int(result)
                parts = [int(n) for n in parts.strip().split(' ')]
                lines.append((result, parts))
        return lines

    def evaluates(self, line_):
        result, values = line_[0], line_[1]
        num_operators = len(values)-1
        for possibilities in range(2**num_operators):
            eval_string = f'{values[0]}'
            for i in range(len(values)-1):
                op = '*' if (possibilities & 1<<i) else '+'
                eval_string = f'({eval_string}{op}{values[i+1]})'
            calculated = eval(eval_string)
            if calculated == result:
                return True
        #     return True

    def create_possibilities(self, operators, length):
        possibilities = ['']
        for i in range(length):
            new_possibilities = []
            for o in operators:
                for p in possibilities:
                    new_possibilities.append(p+o)
            possibilities = new_possibilities
        return possibilities

    def evaluates2(self, line_):
        result, values = line_[0], line_[1]
        num_operators = len(values)-1
        for possibility in self.create_possibilities('+*|', num_operators):
            eval_value = values[0]
            for i, op in enumerate(possibility):
                if op == '|':
                    eval_value = int(f'{eval_value}{values[i+1]}')
                elif op == '*':
                    eval_value = eval_value * values[i+1]
                elif op == '+':
                    eval_value = eval_value + values[i+1]
            if eval_value == result:
                return True

    def solve1(self, input):
        lines = self.parse_input(input)
        total = 0
        for line_ in lines:
            if self.evaluates(line_):
                total += line_[0]
        return total

    def solve2(self, input):
        lines = self.parse_input(input)
        total = 0
        for line_ in lines:
            if self.evaluates2(line_):
                total += line_[0]
        return total


# --------------------

class Test(unittest.TestCase):
    EXAMPLE_INPUT = """
    190: 10 19
    3267: 81 40 27
    83: 17 5
    156: 15 6
    7290: 6 8 6 15
    161011: 16 10 13
    192: 17 8 14
    21037: 9 7 18 13
    292: 11 6 16 20
    """
    def setUp(self):
        self.solver = Dec7()

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 3749)

    def test_solution1(self):
        with open('dec7.txt', 'r') as f:
            output = self.solver.solve1(f.read())
            print(output)
            self.assertEqual(output, 1708857123053)

    def test_possibilities2(self):
        pos = self.solver.create_possibilities('*+', 3)
        self.assertEqual(len(pos), 2**3)

    def test_possibilities3(self):
        pos = self.solver.create_possibilities('*+|', 4)
        self.assertEqual(len(pos), 3**4)

    def test_example2(self):
        output = self.solver.solve2(self.EXAMPLE_INPUT)
        self.assertEqual(output, 11387)

    def test_solution2(self):
        with open('dec7.txt', 'r') as f:
            output = self.solver.solve2(f.read())
            print(output)
            self.assertEqual(output, 189207836795655)


unittest.main()
