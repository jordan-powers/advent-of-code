from pathlib import Path
import heapq
import tqdm
import numpy as np

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
    def __init__(self, buttons: 'list[set[int]]', joltages: 'tuple[int]'):
        self.joltages = joltages
        self.buttons = buttons

    def __repr__(self):
        return f'Machine({repr(self.buttons)}, {repr(joltages)})'

machines: 'list[Machine]' = []

for line in input.split("\n"):
    buttons = []
    for part in line.split():
        if part[0] == '[':
            continue
        elif part[0] == '(':
            buts = tuple(int(b) for b in part[1:-1].split(','))
            buttons.append(buts)
        else:
            assert part[0] == '{'
            joltages = tuple(int(j) for j in part[1:-1].split(','))
    machines.append(Machine(buttons, joltages))


for m in machines:
    a = np.zeros((len(m.joltages), len(m.buttons)), dtype=np.int8)
    for r in range(len(m.joltages)):
        for c, b in enumerate(m.buttons):
            if r in b:
                a[r, c] = 1

    b = np.array(m.joltages, dtype=np.int8).reshape((-1,1))
    sol = np.linalg.lstsq(a, b)
    print(sol)
    print(sol[0].sum())
