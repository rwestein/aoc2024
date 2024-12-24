import unittest
import sys


class Dec21:
    PREDEFINED_SEQUENCES = {
        '029A': '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A',
        '980A': '<v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A',
        '179A': '<v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A',
        '456A': '<v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A',
        '379A': '<v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A'
    }

    KEYPAD1 = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        [None, '0', 'A']
    ]
    KEYPAD2 = [
        [None, '^', 'A'],
        ['<', 'v', '>']
    ]

    def parse_input(self, inp):
        self.codes = []
        for line_ in inp.strip().splitlines():
            if line_.strip():
                self.codes.append(line_.strip())

    def find_position(self, keypad, expected_button):
        for r, row in enumerate(keypad):
            for c, button in enumerate(row):
                if button == expected_button:
                    return r, c

    position_mapping = {}
    def get_position(self, keypad, expected_button):
        keypad_identifier = keypad[0][0]
        key = keypad_identifier, expected_button
        try:
            value = self.position_mapping[key]
        except KeyError:
            # Don't know this one yet, let's find it
            value = self.find_position(keypad, expected_button)
            self.position_mapping[key] = value
        return value

    def find_paths(self, cur_pos, new_pos, keypad):
        delta_x = new_pos[1] - cur_pos[1]
        delta_y = new_pos[0] - cur_pos[0]
        x_path = ''
        y_path = ''
        if delta_x <= 0:
            x_path = '<'*abs(delta_x)
        else:
            x_path = '>'*delta_x
        if delta_y <= 0:
            y_path = '^'*abs(delta_y)
        else:
            y_path = 'v'*delta_y
        # Check crossing None
        if keypad[new_pos[0]][cur_pos[1]] is None:
            # Skip the option to move in Y first
            return set([x_path + y_path + 'A'])
        elif keypad[cur_pos[0]][new_pos[1]] is None:
            # Skip the option to move in X first
            return set([y_path + x_path + 'A'])
        # Just choose one, sequence length is the same
        #return set([y_path+x_path+'A'])
        return set([x_path+y_path+'A', y_path+x_path+'A'])

    def flatten_paths(self, sequences: list) -> set:
        if not sequences:
            return set([''])
        sequences_set = set()
        for path in sequences[0]:
            for flattened_sequence in self.flatten_paths(sequences[1:]):
                sequences_set.add(path+flattened_sequence)
        return sequences_set

    def calculate_sequences(self, code, numpad):
        sequences = []
        cur_pos = self.get_position(numpad, 'A')
        for button in code:
            new_pos = self.get_position(numpad, button)
            # print(f'Find path from {cur_pos} to {new_pos} with button {button}')
            paths = self.find_paths(cur_pos, new_pos, numpad)
            sequences.append(paths)
            cur_pos = new_pos
        return self.flatten_paths(sequences)

    def filter_shortest_sequences(self, sequences: set) -> set:
        filtered_sequences = set()
        sequence_length = None
        for sequence in sequences:
            if sequence_length is None or sequence_length == len(sequence):
                filtered_sequences.add(sequence)
                sequence_length = len(sequence)
            elif sequence_length > len(sequence):
                filtered_sequences = set([sequence])
                sequence_length = len(sequence)
        return filtered_sequences

    def find_shortest_sequence(self, sequences):
        sequence = None
        for s in sequences:
            if sequence is None or len(sequence) >= len(s):
                sequence = s
        return sequence

    def calculate_shortest_sequence(self, code, depth=2):
        sequences = []
        for i in range(depth+1):
            sequences.append(set())

        sequences[0] = self.calculate_sequences(code, self.KEYPAD1)
        for i in range(depth):
            # print(f'depth = {i}')
            for seq1 in sequences[i]:
                sequences[i+1].update(self.calculate_sequences(seq1, self.KEYPAD2))
            #sequences[i+1] = set([self.filter_shortest_sequences(sequences[i+1]).pop()])
        return self.find_shortest_sequence(sequences[depth])

    def calculate_shortest_sequence2(self, code):
        sequences = set()
        sequence_length = None
        for num_sequence in self.calculate_sequences(code, self.KEYPAD1):
            for sequence1 in self.calculate_sequences(num_sequence, self.KEYPAD2):
                for sequence2 in self.calculate_sequences(sequence1, self.KEYPAD2):
                    if sequence_length is None or sequence_length == len(sequence2):
                        sequences.add(sequence2)
                        sequence_length = len(sequence2)
                    elif sequence_length > len(sequence2):
                        sequences = set([sequence2])
                        sequence_length = len(sequence2)
        shortest_seq = sequences.pop()
        # print('shortest seq', shortest_seq)
        return shortest_seq

    def numeric_part(self, code):
        return int(code.replace('A', ''))

    def solve1(self, inp):
        self.parse_input(inp)
        total = 0
        for code in self.codes:
            seq = self.calculate_shortest_sequence(code)
            total += len(seq) * self.numeric_part(code)
        return total

    def solve2(self, inp):
        self.parse_input(inp)
        total = 0
        for code in self.codes:
            seq = self.calculate_shortest_sequence(code, depth=3)
            total += len(seq) * self.numeric_part(code)
        return total


# ****************************************************************************
# Unittests
# ****************************************************************************

class TestDec21(unittest.TestCase):
    EXAMPLE_INPUT = """
    029A
    980A
    179A
    456A
    379A
    """

    def setUp(self):
        self.solver = Dec21()

    def print(self, output):
        if '-v' in sys.argv:
            print(output, end=' ')
            sys.stdout.flush()
        else:
            print(f'{self.id()} = {output}')

    @staticmethod
    def get_input():
        with open('dec21.txt', 'r') as f:
            return f.read()

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 126384)
    def test_one_sequence(self):
        output = self.solver.calculate_sequences('029A', self.solver.KEYPAD1)
        self.assertEqual(output, set(['<A^A>^^AvvvA', '<A^A^^>AvvvA']))
    def test_shortest_sequence1(self):
        output = self.solver.calculate_shortest_sequence('029A')
        self.assertEqual(len(output), 68)
    def test_shortest_sequence2(self):
        output = self.solver.calculate_shortest_sequence('980A')
        self.assertEqual(len(output), 60)
    def test_shortest_sequence3(self):
        output = self.solver.calculate_shortest_sequence('179A')
        self.assertEqual(len(output), 68)
    def test_shortest_sequence4(self):
        output = self.solver.calculate_shortest_sequence('456A')
        self.assertEqual(len(output), 64)
    def test_shortest_sequence5(self):
        output = self.solver.calculate_shortest_sequence('379A')
        self.assertEqual(len(output), 64)
    def _test_investigate_shortest_sequence5(self):
        output1 = self.solver.calculate_shortest_sequence('379A')
        output2 = self.solver.calculate_shortest_sequence2('379A')
        self.assertEqual(output1, output2)

    def test_solution1(self):
        output = self.solver.solve1(self.get_input())
        self.print(output)
        self.assertEqual(output, 107934)

    def test_solution2(self):
        output = self.solver.solve2(self.get_input())
        self.print(output)


if __name__ == '__main__':
    unittest.main()
