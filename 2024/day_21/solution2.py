from pathlib import Path

import heapq

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
029A
980A
179A
456A
379A
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

    def manhattan(self):
        return abs(self.x) + abs(self.y)

dirs = [
    Vec2(1, 0),
    Vec2(0, 1),
    Vec2(-1, 0),
    Vec2(0, -1)
]

dir_strs = {
    Vec2(1, 0): '>',
    Vec2(0, 1): 'v',
    Vec2(-1, 0): '<',
    Vec2(0, -1): '^'
}

numeric_layout = '789\n456\n123\n#0A'
directional_layout = '#^A\n<v>'

numeric_layout = [list(line) for line in numeric_layout.splitlines()]
directional_layout = [list(line) for line in directional_layout.splitlines()]

layouts = {
    "num": numeric_layout,
    "dir": directional_layout
}

start_pos = {
    "num": Vec2(2, 3),
    "dir": Vec2(2, 0)
}

char_coords: 'dict[str, dict[str, Vec2]]' = {lid: {} for lid in layouts.keys()}

for layout_id, layout in layouts.items():
    for r, row in enumerate(layout):
        for c, char in enumerate(row):
            assert char not in char_coords[layout_id]
            if char != '#':
                char_coords[layout_id][char] = Vec2(c, r)

class DjikstraNode:
    def __init__(self, pos: Vec2, prev: 'DjikstraNode|None', cost: int):
        self.pos = pos
        self.prev = prev
        self.cost = cost

    def __lt__(self, other):
        assert isinstance(other, DjikstraNode)
        return self.cost < other.cost

def check_pos(layout: 'list[list[str]]', pos: Vec2):
    if pos.x < 0 or pos.y < 0 or pos.x >= len(layout[0]) or pos.y >= len(layout):
        return False

    if layout[pos.y][pos.x] == '#':
        return False

    return True

djikstra_cache: 'dict[str, dict[tuple[Vec2,Vec2], list[list[str]]]]' = {k: {} for k in layouts.keys()}

def djikstra(layout_id: str, start_pos: Vec2, dest: Vec2) -> 'list[list[str]]':
    global djikstra_cache

    layout = layouts[layout_id]
    cache_key = (start_pos, dest)
    if cache_key in djikstra_cache[layout_id]:
        return djikstra_cache[layout_id][cache_key]

    assert check_pos(layout, start_pos) and check_pos(layout, dest)

    openset: 'list[DjikstraNode]' = [DjikstraNode(start_pos, None, 0)]
    closedset: 'set[Vec2]' = set()

    min_cost = None
    terms = []

    while len(openset) > 0:
        curr = heapq.heappop(openset)

        if min_cost is not None and curr.cost > min_cost:
            break

        if curr.pos == dest:
            if min_cost is None or curr.cost < min_cost:
                terms = [curr]
                min_cost = curr.cost
            elif curr.cost == min_cost:
                terms.append(curr)

        for dir in dirs:
            next_pos = curr.pos + dir

            if next_pos in closedset:
                continue

            if not check_pos(layout, next_pos):
                continue

            next = DjikstraNode(next_pos, curr, curr.cost + 1)
            heapq.heappush(openset, next)
            closedset.add(next)

    paths = []
    for term in terms:
        curr = term
        path = []
        while curr.prev is not None:
            dir = curr.pos - curr.prev.pos
            path.append(dir_strs[dir])
            curr = curr.prev
        paths.append(''.join(path[::-1]))
    djikstra_cache[cache_key] = paths
    return paths

def dist_score(seq: str):
    if len(seq) < 2:
        return 0
    score = 0
    curr = start_pos["dir"]
    for c in seq:
        next = char_coords["dir"][c]
        score += (next - curr).manhattan()
        curr = next
    return score

def rep_score(seq: str):
    if len(seq) < 2:
        return len(seq)

    score = 0
    curr = seq[0]
    for c in seq[1:]:
        if c != curr:
            score += 1
            curr = c
    return score

class ScoredSolution:
    def __init__(self, solution: 'str'):
        self.solution = solution
        self.dist_score = dist_score(solution)
        self.rep_score = rep_score(solution)

    def __lt__(self, other):
        assert isinstance(other, ScoredSolution)
        if self.dist_score == other.dist_score:
            return self.rep_score < other.rep_score
        else:
            return self.dist_score < other.dist_score

def solve_keypad(layout_id: str, sequence: str) -> 'str':
    curr_pos = start_pos[layout_id]
    solutions = ['']
    for c in sequence:
        dest_pos = char_coords[layout_id][c]
        curr_solutions = [s + "A" for s in djikstra(layout_id, curr_pos, dest_pos)]
        curr_pos = dest_pos
        solutions2 = []
        for sol1 in solutions:
            for sol2 in curr_solutions:
                solutions2.append(sol1 + sol2)
        solutions = solutions2

    return solutions

str_dirs = {s: dir for dir, s in dir_strs.items()}

def apply(layout_id, sequence):
    curr_pos = start_pos[layout_id]
    out = ''
    for s in sequence:
        if s == 'A':
            out += layouts[layout_id][curr_pos.y][curr_pos.x]
        else:
            curr_pos += str_dirs[s]
    return out


codes = input.splitlines()

layers = ["num", "dir", "dir"]

curr = "v<A<AA>>^AvAA<^A>Av<<A>>^AvA^Av<<A>>^AAv<A>A^A<A>Av<<A>A>^AAA<A>vA^A"
for layer in layers[::-1]:
    print(curr)
    curr = apply(layer, curr)
print(curr)
exit(1)


sol1 = 0

for code in codes:
    encoded = code
    for i, layer in enumerate(layers):
        encodings = solve_keypad(layer, encoded)
        if i < len(layers)-1:
            encoded = min(ScoredSolution(e) for e in encodings).solution
        else:
            encoded = encodings[0]
    complexity = int(code[:-1]) * len(encoded)
    sol1 += complexity

    print(f"{code}: {len(encoded):<3} {complexity:<4} {encoded}")

print(f"Part 1: {sol1}")

exit(1)

layers = ["num"] + (["dir"] * 25)

codes = input.splitlines()

sol2 = 0

for code in codes:
    encoded = code
    print(encoded)
    for layer in layers:
        print(layer, encoded)
        encoded = solve_keypad(layer, encoded)
    complexity = int(code[:-1]) * len(encoded)
    sol1 += complexity

    print(f"{code}: {len(encoded):<3} {complexity:<4} {encoded}")

print(f"Part 2: {sol2}")
