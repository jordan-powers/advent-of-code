from pathlib import Path
from queue import Queue

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

input = [[int(c) if c != '.' else -9 for c in row] for row in input.splitlines()]

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        assert isinstance(other, Vec2)
        return Vec2(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return isinstance(other, Vec2) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

trailheads = []
for r, row in enumerate(input):
    for c, val in enumerate(row):
        if val == 0:
            trailheads.append(Vec2(x=c, y=r))

dirs = [
    Vec2(1, 0),
    Vec2(0, 1),
    Vec2(-1, 0),
    Vec2(0, -1)
]

def point_in_bounds(point: Vec2):
    return point.x >= 0 and point.y >= 0 and point.x < len(input[0]) and point.y < len(input)

def score_trailhead(trailhead: Vec2) -> 'int':
    openset: 'Queue[list[Vec2]]' = Queue()
    openset.put([trailhead])

    summits = set()

    while openset.qsize() > 0:
        head = openset.get()
        curr_pos = head[-1]
        prev_pos = None
        if len(head) > 1:
            prev_pos = head[-2]

        curr_alt = input[curr_pos.y][curr_pos.x]

        if curr_alt == 9:
            summits.add(curr_pos)
            continue

        for dir in dirs:
            new_pos = curr_pos + dir
            if prev_pos is not None and new_pos == prev_pos:
                continue
            if not point_in_bounds(new_pos):
                continue
            new_alt = input[new_pos.y][new_pos.x]
            if new_alt - curr_alt != 1:
                continue

            new_path = head + [new_pos]
            openset.put(new_path)
    return len(summits)

sol1 = 0
for th in trailheads:
    score = score_trailhead(th)
    #print(th, score)
    sol1 += score
print(f"Part 1: {sol1}")

def rate_trailhead(trailhead: Vec2) -> 'int':
    openset: 'Queue[list[Vec2]]' = Queue()
    openset.put([trailhead])

    score = 0

    while openset.qsize() > 0:
        head = openset.get()
        curr_pos = head[-1]
        prev_pos = None
        if len(head) > 1:
            prev_pos = head[-2]

        curr_alt = input[curr_pos.y][curr_pos.x]

        if curr_alt == 9:
            score += 1
            continue

        for dir in dirs:
            new_pos = curr_pos + dir
            if prev_pos is not None and new_pos == prev_pos:
                continue
            if not point_in_bounds(new_pos):
                continue
            new_alt = input[new_pos.y][new_pos.x]
            if new_alt - curr_alt != 1:
                continue

            new_path = head + [new_pos]
            openset.put(new_path)
    return score

sol2 = 0
for th in trailheads:
    rating = rate_trailhead(th)
    #print(th, rating)
    sol2 += rating
print(f"Part 2: {sol2}")
