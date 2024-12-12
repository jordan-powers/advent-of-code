from pathlib import Path
from queue import Queue

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
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

    def __eq__(self, other):
        return isinstance(other, Vec2) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return "Vec2" + str(self)

garden = [list(l) for l in input.splitlines()]
region_map = [[-1] * len(l) for l in garden]

curr_region_id = 0
dirs = [
    Vec2(1, 0),
    Vec2(0, 1),
    Vec2(-1, 0),
    Vec2(0, -1)
]

def pt_in_bounds(pt: Vec2):
    return pt.x >= 0 and pt.y >= 0 and pt.x < len(garden[0]) and pt.y < len(garden)

chars: 'dict[int, str]' = {}
perims: 'dict[int, int]' = {}
areas: 'dict[int, int]' = {}

perim_pts: 'dict[int, set[tuple[Vec2, Vec2]]]' = {}

origins: 'dict[int, Vec2]' = {}

def map_region(pt: Vec2):
    global curr_region_id, perims, areas

    closed_set = set()
    open_set: 'Queue[Vec2]' = Queue()
    open_set.put(pt)
    closed_set.add(pt)

    region_char = garden[pt.y][pt.x]

    origins[curr_region_id] = pt
    chars[curr_region_id] = region_char
    perims[curr_region_id] = 0
    perim_pts[curr_region_id] = set()
    areas[curr_region_id] = 0

    while open_set.qsize() > 0:
        curr = open_set.get()
        # print(curr, garden[curr.y][curr.x], areas[curr_region_id])
        areas[curr_region_id] += 1

        region_map[curr.y][curr.x] = curr_region_id
        for d in dirs:
            nextpt = curr + d

            if nextpt in closed_set:
                continue

            if not pt_in_bounds(nextpt) or garden[nextpt.y][nextpt.x] != region_char:
                perims[curr_region_id] += 1
                perim_pts[curr_region_id].add((curr, nextpt))
                continue

            open_set.put(nextpt)
            closed_set.add(nextpt)

    curr_region_id += 1

# map_region(Vec2(0, 1))

# print(f'{str(0):<2} {chars[0]}: {str(areas[0]):>2} * {str(perims[0]):>2} = {areas[0] * perims[0]}')
# exit(1)

for r, row in enumerate(garden):
    for c, char in enumerate(row):
        if region_map[r][c] == -1:
            map_region(Vec2(c, r))

# print('\n'.join(' '.join(str(i).ljust(2) for i in row) for row in region_map))

sol1 = 0
for i in range(curr_region_id):
    sol1 += areas[i] * perims[i]
    # print(f'{str(i):<2} {chars[i]}: {str(areas[i]):>2} * {str(perims[i]):>2} = {areas[i] * perims[i]}')

print(f'Part 1: {sol1}')

leftdirs = [
    Vec2(1, -1),
    Vec2(1, 1),
    Vec2(-1, 1),
    Vec2(-1, -1)
]

fwddirs = dirs

rightdirs = [
    Vec2(1, 1),
    Vec2(-1, 1),
    Vec2(-1, -1),
    Vec2(1, -1)
]

def calc_sides(rid):
    side_count = 0
    perimset = perim_pts[rid].copy()

    startperim = None
    startdir = None
    curdir = None
    currperim = None

    while True:
        if startperim is None:
            startperim = next(iter(perimset))
            currperim = startperim
            curdir = (dirs.index(currperim[1] - currperim[0]) + 1) % 4
            startdir = curdir
        elif curdir == startdir and currperim == startperim:
            if len(perimset) > 1:
                perimset.remove(currperim)
                startperim = None
                continue
            else:
                return side_count
        else:
            perimset.remove(currperim)

        # print(curdir, currperim, end=' ')

        left_dir = leftdirs[curdir]
        fwd_dir = fwddirs[curdir]
        right_dir = rightdirs[curdir]

        left_perim = (currperim[0] + left_dir, currperim[1])
        fwd_perim = (currperim[0] + fwd_dir, currperim[1] + fwd_dir)
        right_perim = (currperim[0], currperim[1] + right_dir)

        if left_perim in perimset:
            # print('L', left_perim)
            curdir = (curdir + 3) % 4
            side_count += 1
            currperim = left_perim
            continue

        if fwd_perim in perimset:
            # print('F', fwd_perim)
            currperim = fwd_perim
            continue

        # print('R', right_perim)
        curdir = (curdir + 1) % 4
        side_count += 1
        currperim = right_perim

# print(' '.join(['  '] + [str(i).ljust(2) for i in range(len(region_map[0]))]))
# print('\n'.join(' '.join([str(r).ljust(2)] + [str(i).ljust(2) for i in row]) for r, row in enumerate(region_map)))


#print(calc_sides(2))
#exit(1)

sol2 = 0
for i in range(curr_region_id):
    sides = calc_sides(i)
    #print(f'{str(i):<2} {chars[i]}: {str(areas[i]):>2} * {str(sides):>2} = {areas[i] * sides}')
    sol2 += areas[i] * sides

print(f"Part 2: {sol2}")
