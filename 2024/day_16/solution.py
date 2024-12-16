from pathlib import Path
import math
import heapq

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

    def norm(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))


if USE_SAMPLE_INPUT:
    input = """
#########
###E#####
#.#.#.###
#.....#.#
#.#.###.#
#.#.....#
#.###.###
#...#.#.#
#.#.#.###
#.......#
#######S#
#########
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

maze = [list(line) for line in input.splitlines()]

def find_pos(maze: 'list[list[str]]', search_char: str):
    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if char == search_char:
                return Vec2(c, r)
    raise ValueError(f"No '{search_char}' found in input")

dirs = [
    Vec2(1, 0),
    Vec2(0, 1),
    Vec2(-1, 0),
    Vec2(0, -1)
]

class DeerState:
    def __init__(self, pos: Vec2, dir: int):
        self.pos = pos
        self.dir = dir

    def __eq__(self, other):
        return isinstance(other, DeerState) and self.pos == other.pos and self.dir == other.dir

    def __hash__(self):
        return hash((self.pos, self.dir))

    def __str__(self):
        return f"DeerState({self.pos}, {self.dir})"

    def __repr__(self):
        return str(self)

class AStar_Node:
    def __init__(self, state: DeerState, score: int, estimation: int, prev: 'AStar_Node|None'):
        self.state = state
        self.dir = dir
        self.score = score
        self.estimation = estimation
        self.prev = prev

    def __lt__(self, other):
        assert isinstance(other, AStar_Node)
        return (self.score + self.estimation) < (other.score + other.estimation)

def astar_heuristic(pos: Vec2, dest: Vec2):
    return (dest - pos).norm()

def solve_maze(maze: 'list[list[str]]'):
    dest = find_pos(maze, 'E')

    start_state = DeerState(find_pos(maze, 'S'), 0)
    openset: 'list[AStar_Node]' = [AStar_Node(start_state, 0, astar_heuristic(Vec2(0, 0), dest), None)]
    closedset: 'set[DeerState]' = set()

    while len(openset) > 0:
        curr = heapq.heappop(openset)

        if curr.state.pos == dest:
            return (curr.score, curr)

        closedset.add(curr.state)

        fwd_state = DeerState(curr.state.pos + dirs[curr.state.dir], curr.state.dir)
        left_state = DeerState(curr.state.pos, (curr.state.dir + 3) % 4)
        right_state = DeerState(curr.state.pos, (curr.state.dir + 1) % 4)

        if fwd_state not in closedset and maze[fwd_state.pos.y][fwd_state.pos.x] != '#':
            fwd_node = AStar_Node(fwd_state, curr.score + 1, astar_heuristic(fwd_state.pos, dest), curr)
            heapq.heappush(openset, fwd_node)

        if left_state not in closedset:
            left_node = AStar_Node(left_state, curr.score + 1000, astar_heuristic(left_state.pos, dest), curr)
            heapq.heappush(openset, left_node)

        if right_state not in closedset:
            right_node = AStar_Node(right_state, curr.score + 1000, astar_heuristic(right_state.pos, dest), curr)
            heapq.heappush(openset, right_node)

    raise ValueError("Unsolvable")

maze_best_score, node = solve_maze(maze)

scored_maze = [[0 for c in row] for row in maze]
while node is not None:
    scored_maze[node.state.pos.y][node.state.pos.x] = node.score
    node = node.prev

# print('\n'.join(' '.join(str(s).ljust(6) for s in row) for row in scored_maze))

print(f"Part 1: {maze_best_score}")

class BfsNode:
    def __init__(self, state: DeerState, score: int):
        self.state = state
        self.score = score

    def __lt__(self, other):
        assert isinstance(other, BfsNode)
        return self.score < other.score

def bfs_solve(maze: 'list[list[str]]'):
    dest = find_pos(maze, 'E')

    openset: 'list[BfsNode]' = []
    scores: 'dict[DeerState, int]' = {}
    came_before: 'dict[DeerState, set[DeerState]]' = {}

    start_state = DeerState(find_pos(maze, 'S'), 0)
    heapq.heappush(openset, BfsNode(start_state, 0))
    scores[start_state] = 0
    came_before[start_state] = set()

    end_state = None

    while len(openset) > 0:
        curr = heapq.heappop(openset)

        if curr.state.pos == dest:
            if end_state is None or curr.score < scores[end_state]:
                end_state = curr.state
            continue

        fwd_node = BfsNode(DeerState(curr.state.pos + dirs[curr.state.dir], curr.state.dir), curr.score + 1)
        left_node = BfsNode(DeerState(curr.state.pos, (curr.state.dir + 3) % 4), curr.score + 1000)
        right_node = BfsNode(DeerState(curr.state.pos, (curr.state.dir + 1) % 4), curr.score + 1000)

        for node in (fwd_node, left_node, right_node):
            if maze[node.state.pos.y][node.state.pos.x] == '#':
                continue

            if node.state in scores:
                if node.score == scores[node.state]:
                    came_before[node.state].add(curr.state)
                elif node.score < scores[node.state]:
                    scores[node.state] = node.score
                    came_before[node.state] = set((curr.state,))
                    heapq.heappush(openset, node)
            else:
                scores[node.state] = node.score
                came_before[node.state] = set((curr.state,))
                heapq.heappush(openset, node)

    assert end_state is not None

    to_explore: 'list[DeerState]' = [end_state]
    nodes: 'set[DeerState]' = set()

    while len(to_explore) > 0:
        curr = to_explore.pop()
        nodes.add(curr)
        for node in came_before[curr]:
            if node not in nodes:
                nodes.add(node)
                to_explore.append(node)


    return set((n, scores[n]) for n in nodes)

states = bfs_solve(maze)

scored_maze = [[0 for c in row] for row in maze]
for state, score in states:
    scored_maze[state.pos.y][state.pos.x] = score

# print('\n'.join(' '.join(str(s).ljust(6) for s in row) for row in scored_maze))

# nodes = set(s[0].pos for s in states)
# for r, row in enumerate(maze):
#     for c, char in enumerate(row):
#         if Vec2(c, r) in nodes:
#             print('O', end='')
#         else:
#             print(char, end='')
#     print()

dest = find_pos(maze, 'E')
score = next(s for s in states if s[0].pos == dest)

if score[1] != maze_best_score:
    raise RuntimeError(f"Part 2 score of {score[1]} does not match part 1 score of {maze_best_score}")

nodes = set(s[0].pos for s in states)

print(f"Part 2: {len(nodes)}")
