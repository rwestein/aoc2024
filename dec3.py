import unittest
import re
import sys


class Dec3:
    def __init__(self, input):
        self.input = input

    def parse_input(self, input):
        muls = []
        for mul in re.findall(r'(mul\([0-9][0-9]?[0-9]?,[0-9][0-9]?[0-9]?\))', input):
            match = re.match(r'mul\(([0-9]*),([0-9]*)\)', mul)
            muls.append((int(match.group(1)), int(match.group(2))))
        # print(muls)
        return muls
        # return [(2, 4), (5, 5), (11, 8), (8, 5)]

    def multiply(self):
        total = 0
        for x, y in self.multiplications:
            total += x * y
        return total

    def solve1(self):
        self.multiplications = self.parse_input(self.input)
        return self.multiply()

    def solve2(self):
        total = 0
        state = True
        for part in re.split(r"(don't\(\)|do\(\))", self.input):
            if part == 'do()':
                state = True
            elif part == "don't()":
                state = False
            elif state:
                self.multiplications = self.parse_input(part)
                total += self.multiply()

        # for x, y in self.multiplications:
        #     total += x * y
        return total


# ****************************************************************************
# Unittests
# ****************************************************************************


class TestDec3(unittest.TestCase):
    EXAMPLE_INPUT = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    EXAMPLE_INPUT2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    @staticmethod
    def print(output):
        print(output, end=' ')
        sys.stdout.flush()

    def test_example1(self):
        output = Dec3(self.EXAMPLE_INPUT).solve1()
        self.assertEqual(output, 161)

    def test_read1(self):
        with open('dec3.txt') as f:
            input = f.read()
        output = Dec3(input).solve1()
        self.print(output)

    def test_example2(self):
        output = Dec3(self.EXAMPLE_INPUT2).solve2()
        self.assertEqual(output, 48)

    def test_read2(self):
        with open('dec3.txt') as f:
            input = f.read()
        output = Dec3(input).solve2()
        self.print(output)


if __name__ == '__main__':
    unittest.main()