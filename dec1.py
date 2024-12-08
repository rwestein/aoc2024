import unittest
import sys

class Dec1:
    def parse_list(self, input):
        self.list1 = []
        self.list2 = []
        for line_ in input.strip().splitlines():
            line_ = line_.strip().replace('   ', ' ')
            a, b = line_.strip().split(' ')
            self.list1.append(int(a))
            self.list2.append(int(b))

    def calc_dist(self):
        self.list1.sort()
        self.list2.sort()
        distance = 0
        for a, b in zip(self.list1, self.list2):
            distance += abs(a-b)
        return distance

    def calc_similarity(self):
        similarity = 0
        for x in self.list1:
            for y in self.list2:
                if x == y:
                    similarity += x
        return similarity

    def solve1(self, input):
        self.parse_list(input)
        return self.calc_dist()

    def solve2(self, input):
        self.parse_list(input)
        return self.calc_similarity()


# ****************************************************************************
# Unittests
# ****************************************************************************


class Test(unittest.TestCase):
    EXAMPLE_INPUT = """
    3   4
    4   3
    2   5
    1   3
    3   9
    3   3
    """

    def print(self, output):
        print(output, end=' ')
        sys.stdout.flush()
    def test_example1(self):
        output = Dec1().solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 11)
    def test_solution1(self):
        with open('dec1.txt', 'r') as f:
            input = f.read()
            output = Dec1().solve1(input)
            self.print(output)
    def test_example2(self):
        output = Dec1().solve2(self.EXAMPLE_INPUT)
        self.assertEqual(output, 31)
    def test_solution2(self):
        with open('dec1.txt', 'r') as f:
            input = f.read()
            output = Dec1().solve2(input)
            self.print(output)


if __name__ == '__main__':
    unittest.main()
