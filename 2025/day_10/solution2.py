from pathlib import Path
import math
import tqdm

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""".strip()

else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

class Machine:
    def __init__(self, buttons: 'list[frozenset[int]]', joltages: 'tuple[int]'):
        self.joltages = joltages
        self.buttons = buttons

        self.cache = {}

    def __repr__(self):
        return f'Machine({repr(self.buttons)}, {repr(joltages)})'

    def presscount(self, joltages):
        if sum(joltages) == 0:
            return 0
        if joltages in self.cache:
            return self.cache[joltages]
        print(joltages)
        min_count = math.inf
        for button in self.buttons:
            new_joltages = tuple(j-1 if i in button else j for i, j in enumerate(joltages))
            if any(j < 0 for j in new_joltages):
                continue
            min_count = min(min_count, self.presscount(new_joltages))

        self.cache[joltages] = min_count + 1
        return min_count + 1

machines: 'list[Machine]' = []

for line in input.split("\n"):
    buttons = []
    for part in line.split():
        if part[0] == '[':
            continue
        elif part[0] == '(':
            buts = frozenset(int(b) for b in part[1:-1].split(','))
            buttons.append(buts)
        else:
            assert part[0] == '{'
            joltages = tuple(int(j) for j in part[1:-1].split(','))
    machines.append(Machine(frozenset(buttons), joltages))

part2 = 0
for m in machines:
    solution = m.presscount(m.joltages)
    print(m, solution)
    part2 += solution

print('Part 2:', part2)
