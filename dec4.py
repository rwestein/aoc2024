import unittest
from unittest import skip
import re

class Dec4:
    def parse_input(self, input):
        lines = []
        for line_ in input.strip().splitlines():
            line_ = line_.strip()
            lines.append(line_)
        return lines

    def diag_lines(self, lines):
        diag_lines = []
        for d in range(len(lines[0])+len(lines)):
            diag_line = ''
            for dd in range(d+1):
                try:
                    if dd>=0 and d-dd>=0:
                        # print(dd,d-dd)
                        diag_line += lines[dd][d-dd]
                except IndexError:
                    pass
            if diag_line:
                diag_lines.append(diag_line)
        return diag_lines

    def combine_lines(self, lines):
        combinations = []
        for line_ in lines:
            combinations.append(line_)
            combinations.append(line_[::-1])
        for c in range(len(lines[0])):
            vert_line = ''.join([line_[c] for line_ in lines])
            combinations.append(vert_line)
            combinations.append(vert_line[::-1])
        for diag_line in self.diag_lines(lines):
            combinations.append(diag_line)
            combinations.append(diag_line[::-1])
        lines.reverse()
        for diag_line in self.diag_lines(lines):
            combinations.append(diag_line)
            combinations.append(diag_line[::-1])
        return combinations

    def count(self, line_):
        return len(re.findall('XMAS', line_))

    def solve1(self, input):
        lines = self.parse_input(input)
        combinations = self.combine_lines(lines)
        total = 0
        for line_ in combinations:
            total += self.count(line_)
        return total

    def solve2(self, input):
        xcount = 0
        lines = self.parse_input(input)
        for r, line_ in enumerate(lines):
            for c, char in enumerate(line_):
                if char == 'A' and r > 0 and c > 0:
                    # Potential X
                    try:
                        tl, tr, bl, br = lines[r-1][c-1], lines[r-1][c+1], lines[r+1][c-1], lines[r+1][c+1]
                        if tl+br in ['MS', 'SM'] and tr+bl in ['MS', 'SM']:
                            xcount +=1
                    except IndexError:
                        pass
        return xcount

#--------------------

class Test(unittest.TestCase):
    EXAMPLE_INPUT = """
    MMMSXXMASM
    MSAMXMSMSA
    AMXSXMAAMM
    MSAMASMSMX
    XMASAMXAMM
    XXAMMXXAMA
    SMSMSASXSS
    SAXAMASAAA
    MAMMMXMMMM
    MXMXAXMASX
    """
    def test_diag_lines(self):
        dec = Dec4()
        lines =  dec.parse_input(self.EXAMPLE_INPUT)
        #print(lines)
        output = dec.diag_lines(lines)
        #self.assertEqual(output, ['M', 'MM', 'ASM', 'MMAS'])

    def test_example1(self):
        output = Dec4().solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 18)
    def test_solution1(self):
        with open('dec4.txt', 'r') as f:
            input = f.read()
            output = Dec4().solve1(input)
            print(output)
    def test_example2(self):
        output = Dec4().solve2(self.EXAMPLE_INPUT)
        self.assertEqual(output, 9)
    def test_solution2(self):
        with open('dec4.txt', 'r') as f:
            input = f.read()
            output = Dec4().solve2(input)
            print(output)


unittest.main()
