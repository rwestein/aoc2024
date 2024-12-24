import unittest
import sys


class Dec17:
    verbose = True
    A = 0
    B = 0
    C = 0
    program = []
    ip = 0
    out = []
    abort_when_not_self = False

    def __init__(self):
        self.out = []

    def parse_input(self, inp):
        for line_ in inp.strip().splitlines():
            if line_.strip().startswith('Register'):
                _, reg, value = line_.strip().split()
                value = int(value)
                setattr(self, reg.replace(':',''), value)
            if line_.strip().startswith('Program'):
                program = line_.split(':')[1].strip().split(',')
                self.program = [int(p) for p in program]

    def combo_operand(self, operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C

    def check_abort(self):
        if self.abort_when_not_self:
            if self.out != self.program[:len(self.out)]:
                # abort
                self.ip = len(self.program)
                return True
        return False

    def run_operation(self, opcode, operand):
        if opcode == 0:  # adv, division
            self.A = int(self.A / 2**self.combo_operand(operand))
        elif opcode == 1:  # bxl, bitwise XOR
            self.B = self.B ^ operand
        elif opcode == 2:  # bst, combo mod 8
            self.B = self.combo_operand(operand) % 8
        elif opcode == 3:  # jnz
            if self.A != 0:
                self.ip = operand
                return
        elif opcode == 4:  # bxc, bitwisse XOR
            self.B = self.B ^ self.C
        elif opcode == 5:  # out
            value = self.combo_operand(operand) % 8
            self.out.append(value)
            if self.check_abort():
                return
        elif opcode == 6:  # bdv
            self.B = int(self.A / 2**self.combo_operand(operand))
        elif opcode == 7:  # cdv
            self.C = int(self.A / 2**self.combo_operand(operand))
        self.ip += 2

    def run_program(self):
        self.ip = 0
        self.out = []
        while self.ip < len(self.program):
            opcode = self.program[self.ip]
            operand = self.program[self.ip + 1]
            self.run_operation(opcode, operand)

    def solve1(self, inp):
        self.parse_input(inp)
        self.run_program()
        return ','.join([str(o) for o in self.out])

    def solve2(self, inp):
        self.abort_when_not_self = True
        self.parse_input(inp)
        found = False
        i = 0
        B, C = self.B, self.C
        while not found:
            self.A, self.B, self.C = i, B, C
            self.run_program()
            found = self.out == self.program
            if len(self.out)>7:
                print(i, self.out[:-1])
            if i%1000000==0:
                print(i)
            i+=1
        return i-1


# ****************************************************************************
# Unittests
# ****************************************************************************

class TestDec17(unittest.TestCase):
    EXAMPLE_INPUT = """
    Register A: 729
    Register B: 0
    Register C: 0
    
    Program: 0,1,5,4,3,0
    """
    EXAMPLE_INPUT2 = """
    Register A: 2024
    Register B: 0
    Register C: 0
    
    Program: 0,3,5,4,3,0
    """


    def setUp(self):
        self.solver = Dec17()
        self.solver.verbose = '-v' in sys.argv

    def print(self, output):
        if '-v' in sys.argv:
            print(output, end=' ')
            sys.stdout.flush()
        else:
            print(f'{self.id()} = {output}')

    @staticmethod
    def get_input():
        with open('dec17.txt', 'r') as f:
            return f.read()

    def test_program1(self):
        self.solver.C = 9
        self.solver.program = [2, 6]
        self.solver.run_program()
        self.assertEqual(self.solver.B, 1)

    def test_program2(self):
        self.solver.A = 10
        self.solver.program = [5,0,5,1,5,4]
        self.solver.run_program()
        self.assertEqual(self.solver.out, [0,1,2])

    def test_program3(self):
        self.solver.A = 2024
        self.solver.program = [0,1,5,4,3,0]
        self.solver.run_program()
        self.assertEqual(self.solver.out, [4,2,5,6,7,7,7,7,3,1,0])
        self.assertEqual(self.solver.A, 0)

    def test_program4(self):
        self.solver.B = 29
        self.solver.program = [1,7]
        self.solver.run_program()
        self.assertEqual(self.solver.B, 26)

    def test_program5(self):
        self.solver.B = 2024
        self.solver.C = 43690
        self.solver.program = [4,0]
        self.solver.run_program()
        self.assertEqual(self.solver.B, 44354)

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, '4,6,3,5,6,3,5,2,1,0')

    def test_solution1(self):
        output = self.solver.solve1(self.get_input())
        self.print(output)

    def test_example2(self):
        output = self.solver.solve2(self.EXAMPLE_INPUT2)
        self.assertEqual(output, 117440)

    def test_solution2(self):
        output = self.solver.solve2(self.get_input())
        self.print(output)

    def _test_nibbles(self):
        value = 45483412
        while value:
            print(value%8, end=' ')
            value = int(value/8)
        print()



if __name__ == '__main__':
    unittest.main()
