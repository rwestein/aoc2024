import unittest
import sys


class Dec20:
    verbose = True
    cheat = set()

    def parse_input(self, inp):
        self.matrix = []
        for line_ in inp.strip().splitlines():
            if line_.strip():
                self.matrix.append(line_.strip())
        self.sizex = len(self.matrix[0])
        self.sizey = len(self.matrix)
        self.source, self.destination = self.find_source_destination()

    def find_source_destination(self):
        for r, row in enumerate(self.matrix):
            for c, char in enumerate(row):
                if char == 'S':
                    source = c, r
                if char == 'E':
                    destination = c, r
        return source, destination

    def is_allowed(self, x, y):
        if (x, y) in self.cheat:
            return True
        if 0 <= x < self.sizex and 0 <= y < self.sizey:
            return self.matrix[y][x] in '.SE'
        return False

    def get_adjacents(self, point):
        x, y = point
        adjacents = []
        if self.is_allowed(x+1, y): adjacents.append((x+1, y))
        if self.is_allowed(x-1, y): adjacents.append((x-1, y))
        if self.is_allowed(x, y+1): adjacents.append((x, y+1))
        if self.is_allowed(x, y-1): adjacents.append((x, y-1))
        return adjacents

    def create_visited_matrix(self):
        self.visited = []
        for r in range(self.sizey):
            self.visited.append([False]*self.sizex)

    def is_visited(self, point):
        return self.visited[point[1]][point[0]]

    def add_visited(self, point):
        self.visited[point[1]][point[0]] = True

    def shortest_path_in_maze(self):
        self.create_visited_matrix()
        queue = []
        parents = {}
        queue.append(self.source)
        self.add_visited(self.source)
        while queue:
            s = queue.pop(0)
            if s == self.destination:
                break

            # Get all adjacent vertices of the dequeued vertex s.
            # If an adjacent has not been visited, then mark it visited and enqueue it
            for adjacent in self.get_adjacents(s):
                if not self.is_visited(adjacent):
                    self.add_visited(adjacent)
                    parents[adjacent] = s
                    queue.append(adjacent)

        # Backtrack the shortest path
        s = self.destination
        path = [s]
        while parents[s] != self.source:
            s = parents[s]
            path.insert(0, s)
        path.insert(0, self.source)
        return path

    def find_num_potential_cheat_routes(self):
        num_cheat_routes = 0
        for r, row in enumerate(self.matrix):
            for c, char in enumerate(row):
                if char == '#':
                    num_cheat_routes += 1
        return num_cheat_routes

    progress_counter = 0
    def progress(self, mod=1):
        if self.verbose:
            self.progress_counter += 1
            if self.progress_counter % mod == 0:
                print('.', end='')
                sys.stdout.flush()

    def find_cheat_routes(self):
        cheat_results = []
        for r, row in enumerate(self.matrix):
            for c, char in enumerate(row):
                if char == '#':
                    self.cheat = set([(c, r)])
                    path = self.shortest_path_in_maze()
                    duration = len(path)-1
                    cheat_results.append(duration)
                    self.progress(10)
        return cheat_results

    def compact_cheat_route(self, cheat_route):
        # start, end = cheat_route[0], cheat_route[-1]
        compacted_cheat_route = []
        for x, y in cheat_route:
            if self.matrix[y][x] == '#':
                compacted_cheat_route.append((x,y))
        return tuple(compacted_cheat_route)

    def goes_through_walls(self, source, destination):
        sx, sy = source
        dx, dy = destination
        minx, maxx = min(sx, dx), max(sx, dx)
        miny, maxy = min(sy, dy), max(sy, dy)
        for x in range(minx, maxx+1):
            if self.matrix[sy][x] == '#':
                return set([(x1, miny) for x1 in range(minx, maxx+1)] + [(maxx, y1) for y1 in range(miny, maxy+1)])
        for y in range(miny, maxy+1):
            if self.matrix[y][dx] == '#':
                return set([(x1, miny) for x1 in range(minx, maxx+1)] + [(maxx, y1) for y1 in range(miny, maxy+1)])

    def find_cheat_routes2(self, no_cheat_path, upto=2):
        cheat_routes = set()
        for i, pointi in enumerate(no_cheat_path):
            for j, pointj in enumerate(no_cheat_path):
                if i<j:
                    x1, y1 = pointi
                    x2, y2 = pointj
                    if 1 < abs(x1-x2)+abs(y1-y2) <= upto:
                        cheat_route = self.goes_through_walls(pointi, pointj)
                        if cheat_route:
                            cheat_route = self.compact_cheat_route(cheat_route)
                            if cheat_route not in cheat_routes:
                                cheat_routes.add(cheat_route)
        return cheat_routes

    def solve1(self, inp, saves_at_least=100):
        cheats_that_qualify = []
        self.parse_input(inp)
        no_cheat_path = self.shortest_path_in_maze()
        no_cheat_duration = len(no_cheat_path)-1
        num_cheats = self.find_num_potential_cheat_routes()
        # print(f'Trying {num_cheats} cheats')
        for cheat_duration in self.find_cheat_routes():
            if no_cheat_duration - cheat_duration >= saves_at_least:
                cheats_that_qualify.append(no_cheat_duration - cheat_duration)
        cheats_that_qualify.sort()
        # print(cheats_that_qualify)
        return len(cheats_that_qualify)

    def solve(self, saves_at_least, upto):
        cheats_that_qualify = []
        no_cheat_path = self.shortest_path_in_maze()
        no_cheat_duration = len(no_cheat_path)-1
        cheat_routes = self.find_cheat_routes2(no_cheat_path, upto=upto)
        if self.verbose: print(f'trying {len(cheat_routes)} cheats:', end=' ')
        for cheat in cheat_routes:
            self.cheat = cheat
            cheat_path = self.shortest_path_in_maze()
            self.progress(10)
            cheat_duration = len(cheat_path)-1
            if no_cheat_duration - cheat_duration >= saves_at_least:
                cheats_that_qualify.append(no_cheat_duration - cheat_duration)
        cheats_that_qualify.sort()
        # print(cheats_that_qualify)
        return len(cheats_that_qualify)

    def solve1a(self, inp, saves_at_least=100):
        self.parse_input(inp)
        return self.solve(saves_at_least, 2)

    def solve2(self, inp, saves_at_least=100):
        self.parse_input(inp)
        # Current implementation is slooooooow, but I've got time...
        # Took 17019.381 seconds (a bit under 5 hours)
        return self.solve(saves_at_least, 20)


# ****************************************************************************
# Unittests
# ****************************************************************************

class TestDec20(unittest.TestCase):
    EXAMPLE_INPUT = """
    ###############
    #...#...#.....#
    #.#.#.#.#.###.#
    #S#...#.#.#...#
    #######.#.#.###
    #######.#.#...#
    #######.#.###.#
    ###..E#...#...#
    ###.#######.###
    #...###...#...#
    #.#####.#.###.#
    #.#...#.#.#...#
    #.#.#.#.#.#.###
    #...#...#...###
    ###############
    """

    def setUp(self):
        self.solver = Dec20()
        self.solver.verbose = '-v' in sys.argv

    def print(self, output):
        if '-v' in sys.argv:
            print(output, end=' ')
            sys.stdout.flush()
        else:
            print(f'{self.id()} = {output}')

    @staticmethod
    def get_input():
        with open('dec20.txt', 'r') as f:
            return f.read()

    def test_solve_maze(self):
        self.solver.parse_input(self.EXAMPLE_INPUT)
        output = self.solver.shortest_path_in_maze()
        self.assertEqual(len(output)-1, 84)

    def test_example1(self):
        output = self.solver.solve1(self.EXAMPLE_INPUT, 6)
        self.assertEqual(output, 16)

    def _test_solution1(self):
        output = self.solver.solve1a(self.get_input())
        self.print(output)
        self.assertEqual(output, 1389)

    def test_example1a(self):
        output = self.solver.solve1a(self.EXAMPLE_INPUT, 6)
        self.assertEqual(output, 16)

    def test_example2(self):
        output = self.solver.solve2(self.EXAMPLE_INPUT)
        self.assertEqual(output, 0)

    def _test_solution2(self):
        output = self.solver.solve2(self.get_input())
        self.print(output)
        self.assertGreater(output, 306417)


if __name__ == '__main__':
    unittest.main()
