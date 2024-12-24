import unittest
import sys


class Dec16:
    verbose = True

    def parse_input(self, inp):
        self.matrix = []
        for line_ in inp.strip().splitlines():
            if line_.strip():
                self.matrix.append(line_.strip())
        for r, row in enumerate(self.matrix):
            for c, char in enumerate(row):
                if char == 'S':
                    self.source = c, r, '>'
                elif char == 'E':
                    self.destination = c, r, None
        self.sizex = len(self.matrix[0])
        self.sizey = len(self.matrix)

    ROTATE_CW = {'>':'v','v':'<','<':'^','^':'>'}
    ROTATE_CCW = {'>':'^','v':'>','<':'v','^':'<'}

    def is_valid(self, v):
        x, y, _ = v
        if 0 <= x < self.sizex and 0 <= y < self.sizey:
            return self.matrix[y][x] != '#'
        return False

    def get_neighbours(self, u):
        x, y, d = u
        if d == '<':
            one_step = x-1, y, d
        elif d == '^':
            one_step = x, y-1, d
        elif d == '>':
            one_step = x+1, y, d
        elif d == 'v':
            one_step = x, y+1, d

        potential_neighbours = [one_step, (x, y, self.ROTATE_CW[d]), (x, y, self.ROTATE_CCW[d])]
        return [v for v in potential_neighbours if self.is_valid(v)]

    def calculate_distance(self, u, v):
        x1, y1, d1 = u
        x2, y2, d2 = v
        distance = abs(x1-x2) + abs(y1-y2) + (1000 if d1 != d2 else 0)
        return distance

    def shortest_path(self):
        #  1  function Dijkstra(Graph, source):
        #  2
        #  3      for each vertex v in Graph.Vertices:
        #  4          dist[v] ← INFINITY
        #  5          prev[v] ← UNDEFINED
        #  6          add v to Q
        #  7      dist[source] ← 0
        #  8
        #  9      while Q is not empty:
        # 10          u ← vertex in Q with minimum dist[u]
        # 11          remove u from Q
        # 12
        # 13          for each neighbor v of u still in Q:
        # 14              alt ← dist[u] + Graph.Edges(u, v)
        # 15              if alt < dist[v]:
        # 16                  dist[v] ← alt
        # 17                  prev[v] ← u
        # 18
        # 19      return dist[], prev[]

        #  3      for each vertex v in Graph.Vertices:
        #  4          dist[v] ← INFINITY
        #  5          prev[v] ← UNDEFINED
        #  6          add v to Q
        #  7      dist[source] ← 0
        dist = {}
        prev = {}
        queue = set()
        for x in range(self.sizex):
            for y in range(self.sizey):
                for d in ['<','>','^','v']:
                    v = x, y, d
                    if self.is_valid(v):
                        dist[v] = 1e10
                        prev[v] = ()
                        queue.add(v)
        dist[self.source] = 0
        #  9      while Q is not empty:
        # 10          u ← vertex in Q with minimum dist[u]
        # 11          remove u from Q
        # 12
        while queue:
            u = None
            for uu in queue:
                if u is None or dist[uu] < dist[u]:
                    u = uu
            queue.remove(u)

            # 13          for each neighbor v of u still in Q:
            # 14              alt ← dist[u] + Graph.Edges(u, v)
            # 15              if alt < dist[v]:
            # 16                  dist[v] ← alt
            # 17                  prev[v] ← u
            for v in self.get_neighbours(u):
                if v in queue:
                    alt = dist[u] + self.calculate_distance(u, v)
                    if alt == dist[v]:
                        prev[v] = prev[v]+(u,)
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = (u,)
        return dist, prev

    def print_dist(self, dist):
        for v,d in dist.items():
            str_v = f'{v[0]}, {v[1]}, {v[2]}'
            print(f'{str_v:13s}= {d:3d}  ', end='\n' if (v[2]=='v') else ' ')

    def find_destination_dist(self, dist):
        x, y, _ = self.destination
        min_dist = 1e10
        for (vx, vy, _), dist in dist.items():
            if x==vx and y==vy and dist < min_dist:
                min_dist = dist
        return min_dist

    def solve1(self, inp):
        self.parse_input(inp)
        dist, _ = self.shortest_path()
        # self.print_dist(dist)
        return self.find_destination_dist(dist)

    def trace_back(self, dist, prev):
        # Find best destination
        x, y, _ = self.destination
        min_dist = 1e10
        for (vx, vy, d), dist in dist.items():
            if x==vx and y==vy and dist < min_dist:
                min_dist = dist
                destination = vx, vy, d
        best_spots = set()
        queue = set([destination])
        while queue:
            node = queue.pop()
            best_spots.add(node[:2])
            for p in prev.get(node, []):
                queue.add(p)
        return best_spots

    def solve2(self, inp):
        self.parse_input(inp)
        dist, prev = self.shortest_path()
        best_spots = self.trace_back(dist, prev)
        return len(best_spots)


# ****************************************************************************
# Unittests
# ****************************************************************************

class TestDec16(unittest.TestCase):
    EXAMPLE_INPUT = """
    ###############
    #.......#....E#
    #.#.###.#.###.#
    #.....#.#...#.#
    #.###.#####.#.#
    #.#.#.......#.#
    #.#.#####.###.#
    #...........#.#
    ###.#.#####.#.#
    #...#.....#.#.#
    #.#.#.###.#.#.#
    #.....#...#.#.#
    #.###.#.#.#.#.#
    #S..#.....#...#
    ###############
    """
    EXAMPLE_INPUT2 = """
    #################
    #...#...#...#..E#
    #.#.#.#.#.#.#.#.#
    #.#.#.#...#...#.#
    #.#.#.#.###.#.#.#
    #...#.#.#.....#.#
    #.#.#.#.#.#####.#
    #.#...#.#.#.....#
    #.#.#####.#.###.#
    #.#.#.......#...#
    #.#.###.#####.###
    #.#.#...#.....#.#
    #.#.#.#####.###.#
    #.#.#.........#.#
    #.#.#.#########.#
    #S#.............#
    #################
    """

    def setUp(self):
        self.solver = Dec16()
        self.solver.verbose = '-v' in sys.argv

    def print(self, output):
        if '-v' in sys.argv:
            print(output, end=' ')
            sys.stdout.flush()
        else:
            print(f'{self.id()} = {output}')

    @staticmethod
    def get_input():
        with open('dec16.txt', 'r') as f:
            return f.read()

    def test_example1a(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT)
        self.assertEqual(output, 7036)

    def test_example1b(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT2)
        self.assertEqual(output, 11048)

    def _test_solution1(self):
        output = self.solver.solve1(self.get_input())
        self.print(output)
        self.assertLess(output, 91440)

    def test_example2a(self):
        output = self.solver.solve2(self.EXAMPLE_INPUT)
        self.assertEqual(output, 45)

    def test_example2b(self):
        output = self.solver.solve2(self.EXAMPLE_INPUT2)
        self.assertEqual(output, 64)

    def test_solution2(self):
        output = self.solver.solve2(self.get_input())
        self.print(output)


if __name__ == '__main__':
    unittest.main()
