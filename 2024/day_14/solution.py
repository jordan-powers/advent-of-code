from pathlib import Path
import re
from tqdm import trange

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

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

class Robot:
    def __init__(self, pos: Vec2, vel: Vec2):
        self.pos = pos
        self.vel = vel

    def __str__(self):
        return f"Robot(pos={str(self.pos)}, vel={str(self.vel)})"

    def __repr__(self):
        return str(self)

if USE_SAMPLE_INPUT:
    input = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
""".strip()
    dims = Vec2(11, 7)
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()
    dims = Vec2(101, 103)

parser = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")

robots = []
for line in input.splitlines():
    match = parser.match(line)
    vals = [int(v) for v in match.groups()]
    robots.append(Robot(Vec2(vals[0], vals[1]), Vec2(vals[2], vals[3])))

def draw_robots(robots: 'list[Robot]', dims: 'Vec2', time: 'int') -> 'list[list[int]]':
    grid = [[0 for c in range(dims.x)] for r in range(dims.y)]
    for robot in robots:
        pos = (robot.pos + (robot.vel * time)) % dims
        grid[pos.y][pos.x] += 1

    return grid

def print_grid(grid: 'list[list[int]]'):
    print('\n'.join(''.join(str(c) if c > 0 else '.' for c in r) for r in grid))

def calculate_safety_factor(grid):
    split = Vec2(len(grid[0]) // 2, len(grid) // 2)

    q1 = sum(sum(row[:split.x]) for row in grid[:split.y])
    q2 = sum(sum(row[split.x+1:]) for row in grid[:split.y])
    q3 = sum(sum(row[:split.x]) for row in grid[split.y+1:])
    q4 = sum(sum(row[split.x+1:]) for row in grid[split.y+1:])

    # print(q1, q2, q3, q4)

    return q1 * q2 * q3 * q4

# print(robots)

# print_grid(draw_robots(robots, dims, 100))


sol1 = calculate_safety_factor(draw_robots(robots, dims, 100))
print(f"Part 1: {sol1}")

def calc_neighbor_score(grid: 'list[list[int]]'):
    neighbor_score = 0
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == 0:
                continue
            points = [Vec2(c-1, r-1), Vec2(c, r-1), Vec2(c, r+1), Vec2(c-1, r), Vec2(c+1, r), Vec2(c-1, r+1), Vec2(c, r+1), Vec2(c+1, r+1)]
            for p in points:
                if p.x < 0 or p.y < 0 or p.x >= len(grid[0]) or p.y >= len(grid):
                    continue
                neighbor_score += grid[p.y][p.x]

    return neighbor_score

scores = [(i, calc_neighbor_score(draw_robots(robots, dims, i))) for i in trange(10_000, desc="Search for tree pattern")]
scores.sort(key=lambda x: x[1], reverse=True)

# for score in scores[:100]:
#     print(f"Step {score[0]}: {score[1]}")
#     print_grid(draw_robots(robots, dims, score[0]))
#     print()

easter_egg_coords = (Vec2(31, 38), Vec2(62, 71))

easter_egg_grid = draw_robots(robots, dims, scores[0][0])

curr = 0
while True:
    grid = draw_robots(robots, dims, curr)
    if all(all(grid[r][c] == easter_egg_grid[r][c] for c in range(easter_egg_coords[0].x, easter_egg_coords[1].x)) for r in range(easter_egg_coords[0].y, easter_egg_coords[1].y)):
        print_grid(grid)
        print(f"Part 2: {curr}")
        break
    curr += 1
