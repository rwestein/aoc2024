import unittest
import sys


class Dec22:
    sequences = []
    def __init__(self):
        self.sequences = []

    def parse_input(self, inp):
        self.secrets = []
        for line_ in inp.strip().splitlines():
            if line_.strip():
                self.secrets.append(int(line_.strip()))

    def solve_once(self, secret):
        secret = ((64 * secret) ^ secret) % 16777216
        secret = ((int(secret / 32)) ^ secret) % 16777216
        secret = ((secret * 2048) ^ secret) % 16777216
        return secret

    def solve_day(self, secret):
        prev_price = secret % 10
        # sequence = [(prev_price, 0)]
        sequence = []
        for _ in range(2000):
            secret = self.solve_once(secret)
            price = secret % 10
            sequence.append((price, price - prev_price))
            prev_price = price
        self.sequences.append(sequence)
        return secret

    def map_sequence(self, sequence):
        mapping = {}
        for i, (price, _) in enumerate(sequence):
            if i >= 3:
                seq = tuple([d for (p, d) in sequence[i-3:i+1]])
                # print(i, seq)
                if seq not in mapping: # or mapping[seq] < price:
                    mapping[seq] = price
        return mapping

    def solve1(self, inp):
        self.parse_input(inp)
        total = 0
        for secret in self.secrets:
            total += self.solve_day(secret)
        return total

    def sum_of_prices(self, delta_sequence, print_cutoff=1600):
        price_sum = 0
        ps = []
        for prices in self.prices:
            p = prices.get(delta_sequence, 0)
            if p > 0:
                ps.append(str(p))
            price_sum += p
        if price_sum >= print_cutoff:
            seq = ','.join([str(d) for d in delta_sequence])
            ps1 = ",".join(ps[:10])
            ps2 = ",".join(ps[-10:])
            print(f'{seq}: {ps1},...,{ps2} sum={price_sum}')
        return price_sum

    def solve2(self, inp):
        self.parse_input(inp)
        for secret in self.secrets:
            self.solve_day(secret)
        self.prices = []
        all_delta_sequences = set()
        for seq in self.sequences:
            mapping = self.map_sequence(seq)
            self.prices.append(mapping)
            all_delta_sequences.update(mapping.keys())
        best_sum = 0
        for delta_sequence in all_delta_sequences:
            price_sum = self.sum_of_prices(delta_sequence)
            if price_sum > best_sum:
                best_sum = price_sum
        return best_sum


# ****************************************************************************
# Unittests
# ****************************************************************************

class TestDec22(unittest.TestCase):
    EXAMPLE_INPUT = """
    1
    10
    100
    2024
    """
    EXAMPLE_INPUT2 = """
    1
    2
    3
    2024
    """

    def setUp(self):
        self.solver = Dec22()

    def print(self, output):
        if '-v' in sys.argv:
            print(output, end=' ')
            sys.stdout.flush()
        else:
            print(f'{self.id()} = {output}')

    @staticmethod
    def get_input():
        with open('dec22.txt', 'r') as f:
            return f.read()

    def test_solve_10x(self):
        next_10 = []
        secret = 123
        for i in range(10):
            secret = self.solver.solve_once(secret)
            next_10.append(secret)
        self.assertEqual(next_10, [
            15887950,
            16495136,
            527345,
            704524,
            1553684,
            12683156,
            11100544,
            12249484,
            7753432,
            5908254
        ])

    def test_solve_day(self):
        output = self.solver.solve_day(1)
        self.assertEqual(output, 8685429)

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 37327623)

    def test_solution1(self):
        output = self.solver.solve1(self.get_input())
        self.print(output)

    def test_solve_day2(self):
        self.solver.solve_day(123)
        self.assertEqual(self.solver.sequences[0][:10],
                         [(0, -3), (6, 6), (5, -1), (4, -1), (4, 0), (6, 2), (4, -2), (4, 0), (2, -2), (4, 2)])

    def test_example2(self):
        output = self.solver.solve2(self.EXAMPLE_INPUT2)
        self.assertEqual(output, 23)

    def test_solution2(self):
        output = self.solver.solve2(self.get_input())
        self.assertNotEqual(output, 1640)
        self.assertNotEqual(output, 1643)
        self.print(output)


if __name__ == '__main__':
    unittest.main()
