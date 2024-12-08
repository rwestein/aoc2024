import copy
import sys
import unittest


class Dec2:
    def __init__(self, input):
        self.reports = self.parse_input(input)

    def parse_input(self, input):
        reports = []
        for line_ in input.strip().splitlines():
            report = [int(n) for n in line_.strip().split(' ')]
            reports.append(report)
        return reports

    def is_safe(self, report):
        safe = True
        prev_num = None
        direction = None
        for num in report:
            if prev_num is not None:
                if direction is None:
                    direction = 1 if (num - prev_num) < 0 else -1
                if direction == 1 and not (1 <= prev_num - num <= 3):
                    safe = False
                if direction == -1 and not (1 <= num - prev_num <= 3):
                    safe = False
            prev_num = num
        return safe

    def is_safe2(self, report):
        if self.is_safe(report):
            return True
        for i in range(len(report)):
            new_report = [n for j, n in enumerate(report) if j!=i]
            if self.is_safe(new_report):
                return True
        return False

    def solve1(self):
        num_safe = 0
        for report in self.reports:
            num_safe += self.is_safe(report)
        return num_safe
    def solve2(self):
        num_safe = 0
        for report in self.reports:
            num_safe += self.is_safe2(report)
        return num_safe


# ****************************************************************************
# Unittests
# ****************************************************************************


class TestDec2(unittest.TestCase):
    EXAMPLE_INPUT = """
        7 6 4 2 1
        1 2 7 8 9
        9 7 6 2 1
        1 3 2 4 5
        8 6 4 4 1
        1 3 6 7 9
    """
    EXAMPLE_INPUT2 = '7 6 4 2 1'
    def print(self, output):
        print(output, end=' ')
        sys.stdout.flush()
    def test_example1(self):
        output = Dec2(self.EXAMPLE_INPUT).solve1()
        self.assertEqual(output, 2)
    def test_example1b(self):
        output = Dec2(self.EXAMPLE_INPUT2).solve1()
        self.assertEqual(output, 1)

    def test_solution1(self):
        with open('dec2.txt') as f:
            input = f.read()
        output = Dec2(input).solve1()
        self.print(output)
        self.assertEqual(output, 282)

    def test_example2(self):
        output = Dec2(self.EXAMPLE_INPUT).solve2()
        self.assertEqual(output, 4)
    def test_solution2(self):
        with open('dec2.txt') as f:
            input = f.read()
        output = Dec2(input).solve2()
        self.print(output)


if __name__ == '__main__':
    unittest.main()