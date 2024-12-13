import unittest
import sys


class Dec11:
    def parse_input(self, inp):
        self.stones = [int(n) for n in inp.strip().split()]

    def count_stones(self):
        self.stones_dict = {}
        for s in self.stones:
            if s in self.stones_dict:
                self.stones_dict[s] +=1
            else:
                self.stones_dict[s] =1

    def blink(self):
        new_stones = []
        for stone in self.stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone))%2 == 0:
                half = int(len(str(stone))/2)
                new_stones.append(int(str(stone)[:half]))
                new_stones.append(int(str(stone)[half:]))
            else:
                new_stones.append(stone*2024)
        self.stones = new_stones

    def blink(self):
        new_stones = []
        for stone in self.stones:
            if stone == 0:
                new_stones.append(1)
            elif len(str(stone))%2 == 0:
                half = int(len(str(stone))/2)
                new_stones.append(int(str(stone)[:half]))
                new_stones.append(int(str(stone)[half:]))
            else:
                new_stones.append(stone*2024)
        self.stones = new_stones

    def blink2(self):
        new_stones = {}
        for stone, count in self.stones_dict.items():
            if stone == 0:
                new_stones[1] = new_stones.get(1, 0)+count
            elif len(str(stone)) % 2 == 0:
                half = int(len(str(stone))/2)
                new_stones[int(str(stone)[half:])] = new_stones.get(int(str(stone)[half:]), 0)+count
                new_stones[int(str(stone)[:half])] = new_stones.get(int(str(stone)[:half]), 0)+count
            else:
                new_stones[stone*2024] = new_stones.get(stone*2024, 0)+count
        self.stones_dict = new_stones

    def solve1(self, inp):
        self.parse_input(inp)
        for i in range(25):
            self.blink()
        return len(self.stones)

    def solve2(self, inp):
        self.parse_input(inp)
        self.count_stones()
        for i in range(75):
            self.blink2()
        return sum(self.stones_dict.values())


# ****************************************************************************
# Unittests
# ****************************************************************************

class TestDec11(unittest.TestCase):
    EXAMPLE_INPUT = "125 17"

    def setUp(self):
        self.solver = Dec11()

    def print(self, output):
        if '-v' in sys.argv:
            print(output, end=' ')
            sys.stdout.flush()
        else:
            print(f'{self.id()} = {output}')

    @staticmethod
    def get_input():
        with open('dec11.txt', 'r') as f:
            return f.read()

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 55312)

    def test_solution1(self):
        output = self.solver.solve1(self.get_input())
        self.print(output)

    def test_example2(self):
        output = self.solver.solve2(self.EXAMPLE_INPUT)
        self.assertEqual(output, 65601038650482)

    def test_solution2(self):
        output = self.solver.solve2(self.get_input())
        self.print(output)
        self.assertNotEqual(output, 65601038650482)
        # 220377651399268

if __name__ == '__main__':
    unittest.main()
