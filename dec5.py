import unittest
import functools
import sys


class Dec5:
    def parse_input(self, input):
        order = []
        produce = []
        first_part = True
        for line_ in input.strip().splitlines():
            line_ = line_.strip()
            if not line_:
                first_part = False
            else:
                if first_part:
                    order.append(tuple([int(n) for n in line_.split('|')]))
                else:
                    produce.append([int(n) for n in line_.split(',')])
        return order, produce

    def check_order(self, produce):
        for i, p1 in enumerate(produce):
            for j, p2 in enumerate(produce):
                if i<j and (p2, p1) in self.order:
                    return False
        return True

    def solve1(self, input):
        self.order, produce = self.parse_input(input)
        total = 0
        for prod in produce:
            if self.check_order(prod):
                # print(prod)
                total += prod[int((len(prod)-1)/2)]
        # print(self.order)
        # print(produce)
        # print('total', total)
        return total

    def reorder(self, produce):
        def sort_func(a,b):
            if (a,b) in self.order:
                return -1
            if (b,a) in self.order:
                return 1
            raise ValueError(f'Unknown sort order for {a}, {b}')
        new_produce = produce[:]
        new_produce.sort(key=functools.cmp_to_key(sort_func))
        return new_produce

    def solve2(self, input):
        self.order, produce = self.parse_input(input)
        total = 0
        for prod in produce:
            if not self.check_order(prod):
                reprod = self.reorder(prod)
                total += reprod[int((len(prod)-1)/2)]
        return total

#--------------------

class Test(unittest.TestCase):
    EXAMPLE_INPUT = """
    47|53
    97|13
    97|61
    97|47
    75|29
    61|13
    75|53
    29|13
    97|29
    53|29
    61|53
    97|53
    61|29
    47|13
    75|47
    97|75
    47|61
    75|61
    47|29
    75|13
    53|13
    
    75,47,61,53,29
    97,61,53,29,13
    75,29,13
    75,97,47,61,53
    61,13,29
    97,13,75,29,47
    """
    @staticmethod
    def print(output):
        print(output, end=' ')
        sys.stdout.flush()

    def test_example1(self):
        output = Dec5().solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 143)
    def test_solution1(self):
        with open('dec5.txt', 'r') as f:
            input = f.read()
            output = Dec5().solve1(input)
            self.print(output)
    def test_example2(self):
        output = Dec5().solve2(self.EXAMPLE_INPUT)
        self.assertEqual(output, 123)
    def test_solution2(self):
        with open('dec5.txt', 'r') as f:
            input = f.read()
            output = Dec5().solve2(input)
            self.print(output)


if __name__ == '__main__':
    unittest.main()
