import unittest
import sys
from collections import deque


class Dec23:
    connections = []
    computers = {}
    verbose = True

    def parse_input(self, inp):
        self.connections = []
        for line_ in inp.strip().splitlines():
            if line_.strip():
                c1, c2 = line_.strip().split('-')
                self.connections.append((c1, c2))

    def process_connections(self):
        self.computers = {}
        for c1, c2 in self.connections:
            if c1 not in self.computers:
                self.computers[c1] = []
            if c2 not in self.computers:
                self.computers[c2] = []
            self.computers[c1].append(c2)
            self.computers[c2].append(c1)

    def find_3_connected(self, c):
        parties = set()
        neighbours = self.computers[c]
        for c1 in self.computers:
            for c2 in self.computers:
                if c1 in neighbours and c2 in neighbours and c2 in self.computers[c1]:
                    party = [c, c1, c2]
                    party.sort()
                    parties.add(tuple(party))
        return parties

    def find_lan_parties(self):
        lan_parties = set()
        for c in self.computers:
            parties = self.find_3_connected(c)
            lan_parties.update(parties)
        return lan_parties

    def filter_specific_parties(self, parties, start):
        filtered_parties = set()
        for party in parties:
            for c in party:
                if c[0].startswith(start):
                    filtered_parties.add(party)
        return filtered_parties

    def solve1(self, inp):
        self.parse_input(inp)
        self.process_connections()
        lan_parties = self.find_lan_parties()
        filtered_parties = self.filter_specific_parties(lan_parties, 't')
        return len(filtered_parties)

    def find_largest_connected(self):
        largest_size = 1
        # parties is a set of tuples
        parties = set([tuple([c]) for c in self.computers])
        # Set new_parties to True to get the first loop kickstarted, then change the type to a set of tuples
        if self.verbose:
            print()
        new_parties = True
        while new_parties:
            new_parties = set()
            for comp, neighbours in self.computers.items():
                for party in parties:
                    if set(party).issubset(set(neighbours)):
                        extended_party = list(party + (comp,))
                        extended_party.sort()
                        new_parties.add(tuple(extended_party))
            largest_size += 1
            if self.verbose:
                print(f'{len(new_parties)} new parties of size {largest_size} found')
            if new_parties:
                parties = new_parties
        party = list(parties.pop())
        party.sort()
        return party


    def solve2(self, inp):
        self.parse_input(inp)
        self.process_connections()
        party = self.find_largest_connected()
        return ','.join(party)


# ****************************************************************************
# Unittests
# ****************************************************************************

class TestDec23(unittest.TestCase):
    EXAMPLE_INPUT = """
    kh-tc
    qp-kh
    de-cg
    ka-co
    yn-aq
    qp-ub
    cg-tb
    vc-aq
    tb-ka
    wh-tc
    yn-cg
    kh-ub
    ta-co
    de-co
    tc-td
    tb-wq
    wh-td
    ta-ka
    td-qp
    aq-cg
    wq-ub
    ub-vc
    de-ta
    wq-aq
    wq-vc
    wh-yn
    ka-de
    kh-ta
    co-tc
    wh-qp
    tb-vc
    td-yn
    """

    def setUp(self):
        self.solver = Dec23()
        self.solver.verbose = '-v' in sys.argv

    def print(self, output):
        if '-v' in sys.argv:
            print(output, end=' ')
            sys.stdout.flush()
        else:
            print(f'{self.id()} = {output}')

    @staticmethod
    def get_input():
        with open('dec23.txt', 'r') as f:
            return f.read()

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 7)

    def test_solution1(self):
        output = self.solver.solve1(self.get_input())
        self.print(output)
        self.assertEqual(output, 1170)

    def test_example2(self):
        output = self.solver.solve2(self.EXAMPLE_INPUT)
        self.assertEqual(output, 'co,de,ka,ta')

    def test_solution2(self):
        output = self.solver.solve2(self.get_input())
        self.print(output)


if __name__ == '__main__':
    unittest.main()
