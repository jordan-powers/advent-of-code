from pathlib import Path

import heapq

from functools import cache

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

layout_chars = {
    "num": "0123456789A",
    "dir": "^>v<A"
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

@cache
def solve_char(layers: 'tuple[str]', char: str, start_char: str):
    if len(layers) == 1:
        return char

    curr_layer = layers[0]
    #print(curr_layer, curr_start_pos, char_coords[curr_layer][char])
    options = djikstra(curr_layer, char_coords[curr_layer][start_char], char_coords[curr_layer][char])

    resolved_options = []
    for option in options:
        option += 'A'
        resolved_option = ''
        curr_pos = 'A'
        for char in option:
            resolved_option += solve_char(layers[1:], char, curr_pos)
            curr_pos = char

        resolved_options.append(resolved_option)

    ret =  min(resolved_options, key=len)
    #print(f"Solve for {char} on layer {len(layers)}, get {ret}")
    return ret

def solve_code(layers: 'list[str]', code: str):
    curr_pos = 'A'
    solution = ''
    for c in code:
        solution += solve_char(tuple(layers), c, curr_pos)
        curr_pos = c
    return solution

def build_char_cache(char_cache, layers):
    for i, layer in enumerate(layers[::-1]):
        char_cache.append({})
        for fromchar in layout_chars[layer]:
            for tochar in layout_chars[layer]:
                if i == 0:
                    char_cache[i][(fromchar, tochar)] = 1
                    continue
                options = djikstra(layer, char_coords[layer][fromchar], char_coords[layer][tochar])
                resolved_options = []
                for option in options:
                    option += 'A'
                    resolved = 0
                    curr_pos = 'A'
                    for char in option:
                        resolved += char_cache[i-1][(curr_pos, char)]
                        curr_pos = char
                    resolved_options.append(resolved)
                char_cache[i][(fromchar, tochar)] = min(resolved_options)

def solve_code2(layers: 'list[str]', code: str):
    curr_pos = 'A'
    solution = 0
    for c in code:
        solution += char_cache[len(layers)-1][(curr_pos, c)]
        curr_pos = c
    return solution

codes = input.splitlines()

layers = ["num", "dir", "dir", "dir"]

char_cache = []

build_char_cache(char_cache, layers)

sol1 = 0
for code in codes:
    encoded_len = solve_code2(layers, code)
    complexity = int(code[:-1]) * encoded_len

    print(f"{code}: {encoded_len:<3} {complexity:<4}")

    sol1 += complexity

print(f"Part 1: {sol1}")

print()

layers = ["num"] + (["dir"] * 26)

char_cache = []

build_char_cache(char_cache, layers)

sol2 = 0
for code in codes:
    encoded_len = solve_code2(layers, code)
    complexity = int(code[:-1]) * encoded_len

    print(f"{code}: {encoded_len:<3} {complexity:<4}")

    sol2 += complexity

print(f"Part 2: {sol2}")
