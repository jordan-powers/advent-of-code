from pathlib import Path

import heapq

USE_SAMPLE_INPUT = True
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

def combinatorials(sets: 'list[list[str]]'):
    if len(sets) == 1:
        return sets[0]

    curr = sets[-1]
    subcomb = combinatorials(sets[:-1])
    ret = []
    for item in curr:
        for subitem in subcomb:
            ret.append(subitem + item)
    return ret

def solve_keypad(layout_id: str, sequence: str) -> 'list[str]':
    curr_pos = start_pos[layout_id]
    solutions = ['']
    for c in sequence:
        dest_pos = char_coords[layout_id][c]
        curr_solutions = [s + "A" for s in djikstra(layout_id, curr_pos, dest_pos)]
        curr_pos = dest_pos

        solutions2 = []
        for sol in solutions:
            for sol2 in curr_solutions:
                solutions2.append(sol + sol2)
        solutions = solutions2

    return solutions

def solve_layers(layers: 'list[str]', start_sequence: 'str'):
    solve_stack = [(start_sequence, layers)]
    best_so_far = None

    while len(solve_stack) > 0:
        seq, layers = solve_stack.pop()

        curr_layer = layers[0]
        remain_layers = layers[1:]
        options = solve_keypad(curr_layer, seq)
        if len(remain_layers) == 0:
            for option in options:
                if best_so_far is None or len(option) < len(best_so_far):
                    best_so_far = option
        else:
            for option in options:
                estimate_final_length = len(option) * (2**len(remain_layers))
                if best_so_far is None or estimate_final_length < len(best_so_far):
                    solve_stack.append((option, remain_layers))
    return best_so_far


layers = ["num", "dir", "dir"]

# curr = "029A"
# for i in range(1, len(layers)+1):
#     sol = solve_layers(layers[:i], curr)
#     print(f"{len(sol):<3} {sol}")

codes = input.splitlines()

sol1 = 0

for code in codes:
    encoded = solve_layers(layers, code)
    complexity = int(code[:-1]) * len(encoded)
    sol1 += complexity

    print(f"{code}: {len(encoded):<3} {complexity:<4} {encoded}")

print(f"Part 1: {sol1}")
