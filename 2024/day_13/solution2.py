from pathlib import Path
import re
import math

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

    def __mul__(self, other):
        assert isinstance(other, int) or isinstance(other, float)
        return Vec2(self.x * other, self.y * other)

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

machines = [Machine.parse_str(s) for s in machines]

def solve_machine(machine: Machine, max_pushes=100):
    cost_so_far = math.inf
    push_counts = None

    max_a_pushes = min(machine.prize.x // machine.A.x, machine.prize.y // machine.A.y, max_pushes)
    for num_a_pushes in range(max_a_pushes+1):
        a_result = machine.A * num_a_pushes
        dist_left_to_go = machine.prize - a_result

        num_b_pushes = min(dist_left_to_go.x // machine.B.x, dist_left_to_go.y // machine.B.y, max_pushes)
        cost = (num_a_pushes * A_PRICE) + (num_b_pushes * B_PRICE)

        result = a_result + (machine.B * num_b_pushes)

        if result == machine.prize and cost < cost_so_far:
            cost_so_far = cost
            push_counts = (num_a_pushes, num_b_pushes)

    return (push_counts, cost_so_far)

sol1 = 0
for machine in machines:
    counts, cost = solve_machine(machine)
    # print(machine)
    # print(cost, counts)
    # print()
    if counts is not None:
        sol1 += cost

print(f"Part 1: {sol1}")

def solve_machine_2(machine: Machine):
    ma = machine.A.y / machine.A.x
    mb = machine.B.y / machine.B.x

    assert ma != mb

    bb = machine.prize.y - (mb * machine.prize.x)
    x_int = bb / (ma - mb)

    # print(ma, mb, bb, x_int)

    x_int = round(x_int)

    if x_int < 0:
        return None

    if x_int % machine.A.x != 0:
        return None

    if (machine.prize.x - x_int) % machine.B.x != 0:
        return None

    return (x_int // machine.A.x, (machine.prize.x - x_int) // machine.B.x)

adjustment = Vec2(10000000000000, 10000000000000)

for machine in machines:
    machine.prize = machine.prize + adjustment

sol2 = 0
for machine in machines:
    counts = solve_machine_2(machine)
    # print(machine)
    # print(result)
    # print()
    if counts is not None:
        sol2 += (counts[0] * A_PRICE) + (counts[1] * B_PRICE)
print(f"Part 2: {sol2}")


