from pathlib import Path
import re
import math
import heapq
import time
import tqdm

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

A_PRICE = 3
B_PRICE = 1
MAX_DEPTH = 100

machines = input.split("\n\n")


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

    def norm(self):
        return math.sqrt(self.x**2 + self.y**2)

class Machine:
    COORD_PARSER = re.compile(r"X[+=](\d+), Y[+=](\d+)$")
    def __init__(self, A: Vec2, B: Vec2, prize: Vec2):
        self.A = A
        self.B = B
        self.prize = prize

        self.min_price_per_step = min(A_PRICE/A.norm(), B_PRICE/B.norm())

    def __str__(self):
        return f"Machine(A={self.A}, B={self.B}, prize={self.prize})"

    def __repr__(self):
        return str(self)

    @staticmethod
    def parse_str(input: str) -> 'Machine':
        a_raw, b_raw, prize_raw = input.splitlines()
        a_match = Machine.COORD_PARSER.search(a_raw)
        b_match = Machine.COORD_PARSER.search(b_raw)
        prize_match = Machine.COORD_PARSER.search(prize_raw)

        assert a_match and b_match and prize_match

        a = Vec2(int(a_match.group(1)), int(a_match.group(2)))
        b = Vec2(int(b_match.group(1)), int(b_match.group(2)))
        prize = Vec2(int(prize_match.group(1)), int(prize_match.group(2)))

        return Machine(a, b, prize)

    def heuristic(self, pos: Vec2) -> int:
        return (self.prize - pos).norm() * self.min_price_per_step

class AStar_Node:
    def __init__(self, pos: Vec2, prev_button: 'tuple[str|None, Vec2]', cost: int, estimated_remaining_cost: int, depth: tuple[int, int]):
        self.pos = pos
        self.prev_button = prev_button
        self.cost = cost
        self.estimated_remaining_cost = estimated_remaining_cost
        self.depth = depth

    def __lt__(self, other):
        assert isinstance(other, AStar_Node)
        return (self.cost + self.estimated_remaining_cost) < (other.cost + other.estimated_remaining_cost)

    def __str__(self):
        return '\n'.join([
            "AStar Node:",
            f"   pos={self.pos}",
            f"   prev_button={self.prev_button}",
            f"   cost={self.cost}",
            f"   estimated_remaining_cost={self.estimated_remaining_cost}",
            f"   depth={self.depth}",
            f"   total_cost={self.cost + self.estimated_remaining_cost}"
        ])

def astar(machine: Machine, max_depth=MAX_DEPTH):
    openset: 'list[AStar_Node]' = [AStar_Node(Vec2(0, 0), (None, Vec2(0, 0)), 0, machine.heuristic(Vec2(0, 0)), (0, 0))]
    closedset: 'set[Vec2]' = set()

    prev_buttons: 'dict[Vec2, tuple[str|None, Vec2]]' = {}

    while len(openset) > 0:
        #min_cost = min(n.cost + n.estimated_remaining_cost for n in openset)
        curr = heapq.heappop(openset)
        #assert curr.cost + curr.estimated_remaining_cost == min_cost
        #time.sleep(0.5)
        if curr.pos == machine.prize:
            # path = []
            # curr_pos = curr.pos
            # while True:
            #     button, prev = prev_buttons[curr_pos]
            #     if button is None:
            #         break

            #     path.append(button)
            #     curr_pos = prev

            return (curr.cost, curr.depth)
        if curr.pos in closedset:
            continue

        # print(curr, end="\n\n")

        # print(curr.estimated_remaining_cost + curr.cost)

        closedset.add(curr.pos)
        prev_buttons[curr.pos] = curr.prev_button

        a_pos = curr.pos + machine.A
        b_pos = curr.pos + machine.B

        if curr.depth[0] < max_depth:
            a_node = AStar_Node(a_pos, ('A', curr.pos), curr.cost + A_PRICE, machine.heuristic(a_pos), (curr.depth[0] + 1, curr.depth[1]))
            heapq.heappush(openset, a_node)

        if curr.depth[1] < max_depth:
            b_node = AStar_Node(b_pos, ('B', curr.pos), curr.cost + B_PRICE, machine.heuristic(b_pos), (curr.depth[0], curr.depth[1] + 1))
            heapq.heappush(openset, b_node)

    return None

machines = [Machine.parse_str(s) for s in machines]

print(astar(machines[11]))
exit(1)

sol1 = 0
for machine in machines:
    result = astar(machine)
    print(machine)
    print(result)
    print()
    if result:
        sol1 += result[0]

print(f"Part 1: {sol1}")

exit(1)

adjustment = Vec2(10000000000000, 10000000000000)

for machine in machines:
    machine.prize = machine.prize + adjustment

print(machines[1])
print(astar(machines[1], math.inf))
