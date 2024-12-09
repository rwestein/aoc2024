import unittest
import sys


class Dec9:
    blocks = []

    def parse_input(self, inp):
        blocks = []
        for i, number in enumerate(inp.strip()):
            number = int(number)
            if i % 2 == 0:
                blocks.extend([int(i/2)]*number)
            else:
                blocks.extend([None] * number)
        self.blocks = blocks

    def next_i(self, i):
        # Find first empty slot
        while i < len(self.blocks) and self.blocks[i] is not None:
            i += 1
        return i

    def previous_j(self, j):
        while j > 0 and self.blocks[j] is None:
            j -= 1
        return j

    def move_blocks(self):
        i = self.next_i(0)
        j = self.previous_j(len(self.blocks)-1)
        while i < j:
            # move block
            self.blocks[i] = self.blocks[j]
            self.blocks[j] = None
            i = self.next_i(i)
            j = self.previous_j(j)

    def move_blocks2(self):
        i = self.next_i(0)
        j = self.previous_j(len(self.blocks)-1)
        filenum = self.blocks[j]
        while i < j and filenum is not None:
            # move blocks
            filenum = self.blocks[j]
            needed_space = 0
            while self.blocks[j-needed_space] == filenum:
                needed_space += 1

            ii = i
            available_space = 0
            while needed_space > available_space and ii < j:
                ii = self.next_i(ii+available_space)
                available_space = 0
                while ii < j and self.blocks[ii+available_space] is None:
                    available_space += 1

            if needed_space <= available_space:
                for k in range(needed_space):
                    self.blocks[ii+k] = self.blocks[j-k]
                    self.blocks[j-k] = None
                i = self.next_i(i)
            else:
                j -= needed_space
            j = self.previous_j(j)

    def print(self):
        print(''.join([(str(b) if b is not None else '.') for b in self.blocks]))

    def calculate_checksum(self):
        checksum = 0
        for i, number in enumerate(self.blocks):
            if number is not None:
                checksum += i * number
        return checksum

    def solve1(self, inp):
        self.parse_input(inp)
        self.move_blocks()
        return self.calculate_checksum()

    def solve2(self, inp):
        self.parse_input(inp)
        self.move_blocks2()
        # self.print()
        return self.calculate_checksum()


# ****************************************************************************
# Unittests
# ****************************************************************************

class TestDec9(unittest.TestCase):
    EXAMPLE_INPUT = "2333133121414131402"

    def setUp(self):
        self.solver = Dec9()

    @staticmethod
    def print(output):
        print(output, end=' ')
        sys.stdout.flush()

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 1928)

    def test_solution1(self):
        with open('dec9.txt', 'r') as f:
            output = self.solver.solve1(f.read())
            self.print(output)
            self.assertEqual(output, 6390180901651)

    def test_example2(self):
        output = self.solver.solve2(self.EXAMPLE_INPUT)
        self.assertEqual(output, 2858)

    def test_solution2(self):
        with open('dec9.txt', 'r') as f:
            output = self.solver.solve2(f.read())
            self.print(output)
            self.assertEqual(output, 6412390114238)


if __name__ == '__main__':
    unittest.main()
