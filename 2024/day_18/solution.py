from pathlib import Path
from queue import Queue
import heapq
import math

import time
import subprocess

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
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
""".strip()
    grid_size = Vec2(7, 7)
    num_bytes = 12
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()
    grid_size = Vec2(71, 71)
    num_bytes = 1024

byte_locs = []
for loc in input.splitlines():
    x, y = loc.split(',')
    byte_locs.append(Vec2(int(x), int(y)))

class AStarNode:
    def __init__(self, pos: Vec2, score: int, estimate: int, prev: 'AStarNode|None'):
        self.pos = pos
        self.score = score
        self.estimate = estimate
        self.prev = prev

    def __lt__(self, other):
        assert isinstance(other, AStarNode)
        return (self.score + self.estimate) < (other.score + other.estimate)

dirs = [
    Vec2(1, 0),
    Vec2(0, 1),
    Vec2(-1, 0),
    Vec2(0, -1)
]

def print_grid(byte_locs: 'set[Vec2]', path: 'list[Vec2]|None' = None, openset: 'set[Vec2]|None' = None, closedset: 'set[Vec2]|None' = None):
    if path is not None:
        path = set(path)

    for r in range(grid_size.y):
        for c in range(grid_size.x):
            curr = Vec2(c, r)
            if curr in byte_locs:
                print('#', end='')
            elif path is not None and curr in path:
                print('O', end='')
            elif openset is not None and curr in openset:
                print('?', end='')
            elif closedset is not None and curr in closedset:
                print('X', end='')
            else:
                print('.', end='')
        print()

def test_in_bounds(pt: Vec2):
    return pt.x >= 0 and pt.y >= 0 and pt.x < grid_size.x and pt.y < grid_size.y

def astar(byte_locs: 'list[Vec2]', debug=False):
    dest = grid_size + Vec2(-1, -1)

    open_set = [AStarNode(Vec2(0, 0), 0, dest.norm(), None)]
    closed_set: 'set[Vec2]' = set()

    while len(open_set) > 0:
        curr = heapq.heappop(open_set)

        if debug:
            subprocess.run('cls', shell=True)
            print_grid(byte_locs, path=None, openset=set(c.pos for c in open_set), closedset=closed_set)
            print()
            time.sleep(0.05)

        if curr.pos == dest:
            path = []
            while curr is not None:
                path.append(curr.pos)
                curr = curr.prev
            return path[::-1]

        for dir in dirs:
            next = curr.pos + dir
            if next not in closed_set and test_in_bounds(next) and next not in byte_locs:
                closed_set.add(next)
                estimate = (dest - next).norm()
                heapq.heappush(open_set, AStarNode(next, curr.score + 1, estimate, curr))

    return None

class BfsNode:
    def __init__(self, pos: Vec2, prev: 'BfsNode|None'):
        self.pos = pos
        self.prev = prev


def bi_bfs(byte_locs: 'list[Vec2]', debug=False):
    start = Vec2(0,0)
    dest = grid_size + Vec2(-1, -1)

    start_node = BfsNode(start, None)
    end_node = BfsNode(dest, None)

    bfs_queue: 'Queue[list[BfsNode]]' = Queue()
    bfs_queue.put([start_node])
    bfs_queue.put([end_node])
    open_set: 'dict[Vec2, BfsNode]' = {
        start_node.pos: start_node,
        end_node.pos: end_node
    }
    closed_set: 'set[Vec2]' = set((start, dest))

    while bfs_queue.qsize() > 0:
        curr_level = bfs_queue.get()
        next_level = []
        next_pts = set()

        if debug:
            subprocess.run('cls', shell=True)
            print_grid(byte_locs, path=None, openset=set(open_set.keys()), closedset=closed_set)
            print()
            time.sleep(0.1)

        for node in curr_level:
            del open_set[node.pos]
            #print(node.pos)
            closed_set.add(node.pos)

            for dir in dirs:
                next = node.pos + dir
                if next in next_pts or next in closed_set or next in byte_locs or not test_in_bounds(next):
                    continue

                #print("    ", next, next in open_set)
                if next in open_set:
                    path = []
                    curr = node
                    while curr is not None:
                        path.append(curr.pos)
                        curr = curr.prev
                    path = path[::-1]
                    curr = open_set[next]
                    while curr is not None:
                        path.append(curr.pos)
                        curr = curr.prev
                    if path[0] != start:
                        path = path[::-1]
                    return path

                next_node = BfsNode(next, node)
                next_level.append(next_node)
                next_pts.add(next)
                open_set[next] = next_node

        if len(next_level) > 0:
            bfs_queue.put(next_level)

    return None

byte_locs_orig = byte_locs
byte_locs = set(byte_locs[:num_bytes])
#print_grid(byte_locs)

# tic = time.perf_counter()
# path = astar(byte_locs)
# toc = time.perf_counter() - tic
# print(f"A*: {toc}")

# tic = time.perf_counter()
path2 = bi_bfs(byte_locs)
# toc = time.perf_counter() - tic
# print(f"BiBFS: {toc}")

# print_grid(byte_locs, path)
# print_grid(byte_locs, path2)


print(f"Part 1: {len(path2)-1}")

for i in range(num_bytes+1, len(byte_locs_orig)):
    #print(i)
    path = bi_bfs(set(byte_locs_orig[:i]))
    if path is None:
        print(f"Part 2: {byte_locs_orig[i-1]}")
        break
