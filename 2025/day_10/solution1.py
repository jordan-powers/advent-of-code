from pathlib import Path
import heapq
import tqdm

USE_SAMPLE_INPUT = True
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
[..#.##.##] (0,1,2,3,4,5,8) (2,3,5,7) (2,5,6,7) (0,3,4,5,6,7,8) (0,2,4,6,7,8) (0,1,2,4,5,8) (0,2,4,5,6) (0,1,3,4,7,8) (0,1) (2,3,6) {55,25,58,54,55,53,44,43,42}
""".strip()

else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

class Machine:
    def __init__(self, buttons, joltages):
        assert isinstance(buttons, frozenset)
        assert isinstance(joltages, tuple)
        self.joltages = joltages
        self.buttons = buttons

    def __repr__(self):
        return f'Machine({repr(self.buttons)}, {repr(joltages)})'

machines: 'list[Machine]' = []

for line in input.split("\n"):
    buttons = set()
    for part in line.split():
        if part[0] == '[':
            continue
        elif part[0] == '(':
            buts = tuple(int(b) for b in part[1:-1].split(','))
            buttons.add(buts)
        else:
            assert part[0] == '{'
            joltages = tuple(int(j) for j in part[1:-1].split(','))
    machines.append(Machine(frozenset(buttons), joltages))

# for m in machines:
#     print(m)

class State:
    def __init__(self, m: Machine, presses: int, joltages: tuple[int]):
        self.m = m
        self.presses = presses
        self.joltages = joltages

        self.sorted_buttons = sorted(self.m.buttons, key=lambda k: len(k), reverse=True)

    def greedy_estimate(self):
        joltages = list(self.joltages)
        estimate = 0
        for button in self.sorted_buttons:
            if any(joltages[b] <= 0 for b in button):
                continue
            count = min(joltages[b] for b in button)
            for b in button:
                joltages[b] -= count
            estimate += count
        return estimate

    def estimate(self):
        return self.presses + self.greedy_estimate()

    def __lt__(self, other):
        assert isinstance(other, State)
        #return self.presses < other.presses
        return self.estimate() < other.estimate()

    def __eq__(self, other):
        assert isinstance(other, State)
        return self.presses == other.presses and self.joltages == other.joltages

    def __hash__(self):
        return hash((self.presses, self.joltages))

    def __repr__(self):
        return f'State({self.presses}, {self.joltages}, estimate={self.greedy_estimate()})'

def greedy_solution(m: Machine, joltages):
    joltages = list(joltages)
    sorted_buttons = sorted(m.buttons, key=lambda k: len(k), reverse=True)
    estimate = 0
    for button in sorted_buttons:
        if any(joltages[b] <= 0 for b in button):
            continue
        count = min(joltages[b] for b in button)
        for b in button:
            joltages[b] -= count
        estimate += count
    if all(j == 0 for j in joltages):
        return estimate
    return None

def solve_buttons_1(m: Machine):
    queue = [State(m, 0, m.joltages)]
    heapq.heapify(queue)


    seen = set()

    while len(queue) > 0:
        curr = heapq.heappop(queue)
        print(curr)

        if all(j == 0 for j in curr.joltages):
            return curr.presses

        sol = greedy_solution(m, curr.joltages)
        if sol is not None:
            return sol

        for button in m.buttons:
            new_joltages = tuple(j-1 if i in button else j for i, j in enumerate(curr.joltages))
            if any(j < 0 for j in new_joltages):
                continue

            new_state = State(m, curr.presses + 1, tuple(new_joltages))
            if new_state in seen:
                continue
            seen.add(new_state)
            heapq.heappush(queue, new_state)

    assert False, "No solution found!"

part2 = 0
for m in machines:
    solution = solve_buttons_1(m)
    print(m, solution)
    part2 += solution

print('Part 2:', part2)
