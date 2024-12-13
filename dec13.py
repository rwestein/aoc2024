import unittest
import sys
import sympy
from math import lcm


class Dec13:
    def parse_delta(self, text):
        x, y = text.strip().split(',')
        assert x.strip().startswith('X')
        assert y.strip().startswith('Y')
        x = int(x.strip()[1:])
        y = int(y.strip()[1:])
        return x, y

    def parse_position(self, text):
        x, y = text.strip().split(',')
        assert x.strip().startswith('X=')
        assert y.strip().startswith('Y=')
        x = int(x.strip()[2:])
        y = int(y.strip()[2:])
        return x, y

    def parse_input(self, inp):
        self.machines = []
        for line_ in inp.strip().splitlines():
            line_ = line_.strip()
            if line_.startswith('Button A:'):
                buttona = self.parse_delta(line_.split(':')[1])
            if line_.startswith('Button B:'):
                buttonb = self.parse_delta(line_.split(':')[1])
            if line_.startswith('Prize:'):
                prize = self.parse_position(line_.split(':')[1])
                self.machines.append((buttona, buttonb, prize))

    def calculate_tokens_to_spend_for_prize_in_range(self, buttona, buttonb, prize, range_a):
        # 3 to push A, 1 to push B
        min_tokens = 0
        prize_over_b = prize[0] / buttonb[0]
        a_over_b = buttona[0] / buttonb[0]
        for a in range_a:
            # print((prize[0] - a*buttona[0]) / buttonb[0])
            # b = int((prize[0] - a*buttona[0]) / buttonb[0])
            b = prize_over_b - a*a_over_b
            if not b.is_integer():
                continue
            b = int(b)
            # print(f'b = {b}')
            if a*buttona[0] + b*buttonb[0] == prize[0]:
                print(f'x matches at prize position {prize}: a={a}, b={b}')
                if a*buttona[1] + b*buttonb[1] == prize[1]:
                    # Combination found
                    if min_tokens == 0:
                        min_tokens = a*3+b
                        print(f'Combination found at prize position {prize}: a={a}, b={b}')
                        # return min_tokens
                    elif a * 3 + b < min_tokens:
                        min_tokens = a * 3 + b
                        # print(f'Combination improved at prize position {prize}: a={a}, b={b}')
        return min_tokens

    def calculate_tokens_to_spend_for_prize(self, machine):
        buttona, buttonb, prize = machine
        return self.calculate_tokens_to_spend_for_prize_in_range(buttona, buttonb, prize, range(100))

    def calculate_tokens_to_spend_for_prize2(self, machine):
        buttona, buttonb, prize = machine
        prize = (prize[0]+10000000000000, prize[1]+10000000000000)
        lcm0 = lcm(buttona[0], buttonb[0])
        min_a = int(prize[0]/max(buttona[0], buttonb[0]))
        min_a = 0 #int(prize[0]/max(buttona[0], buttonb[0]))
        # print(lcm0)
        max_a = min_a + lcm0 + 2#int(prize[0]/min(buttona[0], buttonb[0]))
        step = 1
        # print(sympy.ntheory.factorint(prize[0]), sympy.ntheory.factorint(prize[1]))
        # Ontbinden in factoren

        return self.calculate_tokens_to_spend_for_prize_in_range(buttona, buttonb, prize, range(min_a, max_a, step))

    def solve1(self, inp):
        self.parse_input(inp)
        tokens_spend = 0
        for machine in self.machines:
            tokens_spend += self.calculate_tokens_to_spend_for_prize(machine)
        return tokens_spend

    def solve2(self, inp):
        self.parse_input(inp)
        tokens_spend = 0
        for machine in self.machines:
            tokens_spend += self.calculate_tokens_to_spend_for_prize2(machine)
        return tokens_spend


# ****************************************************************************
# Unittests
# ****************************************************************************

class TestDec13(unittest.TestCase):
    EXAMPLE_INPUT = """
    Button A: X+94, Y+34
    Button B: X+22, Y+67
    Prize: X=8400, Y=5400
    
    Button A: X+26, Y+66
    Button B: X+67, Y+21
    Prize: X=12748, Y=12176
    
    Button A: X+17, Y+86
    Button B: X+84, Y+37
    Prize: X=7870, Y=6450
    
    Button A: X+69, Y+23
    Button B: X+27, Y+71
    Prize: X=18641, Y=10279
    """

    def setUp(self):
        self.solver = Dec13()

    def print(self, output):
        if '-v' in sys.argv:
            print(output, end=' ')
            sys.stdout.flush()
        else:
            print(f'{self.id()} = {output}')

    @staticmethod
    def get_input():
        with open('dec13.txt', 'r') as f:
            return f.read()

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 480)

    def test_solution1(self):
        output = self.solver.solve1(self.get_input())
        self.print(output)

    # def test_example2(self):
    #     output = self.solver.solve2(self.EXAMPLE_INPUT)
    #     self.assertEqual(output, 480)

    def test_solution2(self):
        output = self.solver.solve2(self.get_input())
        self.print(output)


if __name__ == '__main__':
    unittest.main()
