from pathlib import Path

import heapq

from queue import Queue

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
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
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        assert isinstance(other, Vec2)
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        assert isinstance(other, Vec2)
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        assert isinstance(other, int) or isinstance(other, float)
        return Vec2(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mod__(self, other):
        assert isinstance(other, Vec2)
        return Vec2(self.x % other.x, self.y % other.y)

    def __eq__(self, other):
        return isinstance(other, Vec2) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return "Vec2" + str(self)

maze = [list(line) for line in input.splitlines()]

def find_pos(maze: 'list[list[str]]', search_char: str):
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if char == search_char:
                return Vec2(c, r)
    raise ValueError(f"No '{search_char}' found in input")

def check_in_bounds(maze: 'list[list[str]]', pos: Vec2):
    return pos.x >= 0 and pos.y >= 0 and pos.x < len(maze[0]) and pos.y < len(maze)

dirs = [
    Vec2(1, 0),
    Vec2(0, 1),
    Vec2(-1, 0),
    Vec2(0, -1)
]

class AStarNode:
    def __init__(self, pos: Vec2, cost: int, estimate):
        self.pos = pos
        self.cost = cost
        self.estimate = estimate

    def __lt__(self, other):
        assert isinstance(other, AStarNode)
        return (self.cost + self.estimate) < (other.cost + other.estimate)

dirs = [
    Vec2(1, 0),
    Vec2(0, 1),
    Vec2(-1, 0),
    Vec2(0, -1)
]

def astar(maze: 'list[list[str]]', start_pos, end_pos, max_score: int|None = None):
    diff = end_pos - start_pos

    if start_pos == end_pos:
        return 0

    openset = [AStarNode(start_pos, 0, abs(diff.x) + abs(diff.y))]

    closedset: 'set[Vec2]' = set()

    while len(openset) > 0:
        curr = heapq.heappop(openset)

        for dir in dirs:
            next = curr.pos + dir

            if not check_in_bounds(maze, next):
                continue

            if maze[next.y][next.x] == '#':
                continue

            if next == end_pos:
                return curr.cost+1

            if max_score is not None and curr.cost+1 >= max_score:
                continue

            if next not in closedset:
                closedset.add(next)
                diff = end_pos - next
                estimate = abs(diff.x) + abs(diff.y)
                heapq.heappush(openset, AStarNode(next, curr.cost + 1, estimate))
    return None

def print_maze(maze, closedset):
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            pos = Vec2(c, r)
            if pos in closedset:
                print('X', end='')
            else:
                print(char, end='')
        print()

def calc_dists(maze: 'list[list[str]]'):
    costs = {}

    openset: 'Queue[Vec2]' = Queue()
    closedset: 'set[Vec2]' = set()

    start_pos = find_pos(maze, 'S')
    end_pos = find_pos(maze, 'E')

    openset.put(start_pos)
    closedset.add(start_pos)
    costs[start_pos] = 0

    while openset.qsize() > 0:
        curr = openset.get()

        for dir in dirs:
            next = curr + dir
            if not check_in_bounds(maze, next):
                continue

            if next in closedset:
                continue

            if maze[next.y][next.x] == '#':
                continue

            openset.put(next)
            closedset.add(next)
            costs[next] = costs[curr] + 1

    end_cost = costs[end_pos]
    dists = {}
    for point, cost in costs.items():
        dists[point] = end_cost - cost

    return dists


def find_cheats(maze: 'list[list[str]]'):
    openset: 'Queue[(Vec2, int)]' = Queue()
    closedset: 'set[Vec2]' = set()

    start_pos = find_pos(maze, 'S')
    end_pos = find_pos(maze, 'E')

    openset.put((start_pos, 0))
    closedset.add(start_pos)

    shortcut_savings = {}

    dists = calc_dists(maze)
    no_cheat_cost = dists[start_pos]

    while openset.qsize() > 0:
        # print_maze(maze, closedset)
        # print()
        # time.sleep(0.5)

        curr_pos, curr_cost = openset.get()

        curr_char = maze[curr_pos.y][curr_pos.x]

        for dir in dirs:
            next = curr_pos + dir
            if not check_in_bounds(maze, next):
                continue

            if next in closedset:
                continue

            if curr_char == '#':
                if maze[next.y][next.x] == '#':
                    continue

                shortcut_cost = dists[next] + curr_cost + 1

                diff = no_cheat_cost - shortcut_cost

                if diff > 0:
                    shortcut_savings[diff] = shortcut_savings.get(diff, 0) + 1
            else:
                openset.put((next, curr_cost + 1))
                closedset.add(next)

    return shortcut_savings


#print(astar(maze, find_pos(maze, 'S'), find_pos(maze, 'E')))

cheats = find_cheats(maze)

if USE_SAMPLE_INPUT:
    keys = sorted(cheats.keys())
    print("Part 1")
    for k in keys:
        print(f'There are {cheats[k]} cheats that save {k} picoseconds')
    print()
else:
    sol1 = 0
    for savings, count in cheats.items():
        if savings >= 100:
            sol1 += count

    print(f"Part 1: {sol1}")

def find_pts_within_radius(maze: 'list[list[str]]', center: Vec2, radius: int):
    out: 'set[Vec2]' = set()

    openset = Queue()
    closedset = set()

    openset.put((center, 0))
    closedset.add(center)

    while openset.qsize() > 0:
        curr_pos, curr_dist = openset.get()
        for dir in dirs:
            next = curr_pos + dir
            if not check_in_bounds(maze, next):
                continue
            if next in closedset:
                continue
            if maze[next.y][next.x] != '#':
                out.add(next)

            if curr_dist + 1 < radius:
                openset.put((next, curr_dist + 1))
                closedset.add(next)
    return out

def find_cheats_2(maze: 'list[list[str]]'):
    openset: 'Queue[(Vec2, int)]' = Queue()
    closedset: 'set[Vec2]' = set()

    start_pos = find_pos(maze, 'S')
    end_pos = find_pos(maze, 'E')

    openset.put((start_pos, 0))
    closedset.add(start_pos)

    shortcut_savings = {}

    dists = calc_dists(maze)
    no_cheat_cost = dists[start_pos]

    while openset.qsize() > 0:
        curr_pos, curr_cost = openset.get()

        pts = find_pts_within_radius(maze, curr_pos, 20)
        for pt in pts:
            diff = pt - curr_pos

            shortcut_cost = dists[pt] + curr_cost + abs(diff.x) + abs(diff.y)

            diff = no_cheat_cost - shortcut_cost

            if diff > 0:
                shortcut_savings[diff] = shortcut_savings.get(diff, 0) + 1

        for dir in dirs:
            next = curr_pos + dir

            if next in closedset:
                continue

            if maze[next.y][next.x] == '#':
                continue

            else:
                openset.put((next, curr_cost + 1))
                closedset.add(next)

    return shortcut_savings


cheats = find_cheats_2(maze)
if USE_SAMPLE_INPUT:
    keys = sorted(cheats.keys())
    keys = [k for k in keys if k >= 50]
    print("Part 2")
    for k in keys:
        print(f'There are {cheats[k]} cheats that save {k} picoseconds')
else:
    sol2 = 0
    for savings, count in cheats.items():
        if savings >= 100:
            sol2 += count

    print(f"Part 2: {sol2}")
