from pathlib import Path
import sympy
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

def button_presses(m, solution, assigned, free_vars):
    if len(free_vars) > 0:
        var = free_vars[0]
        assert var not in assigned
        varidx = int(str(var)[1:])
        minval = min(m.joltages[k] for k in m.buttons[varidx])
        minsol = math.inf
        for v in range(minval+1):
            minsol = min(minsol, button_presses(m, solution, {**assigned, var: v}, free_vars[1:]))
        return minsol

    count = sum(assigned.values())
    for var, eq in solution.items():
        result = float(eq.subs(assigned))
        if result < 0 or result.is_integer() == False:
            return math.inf
        count += result

    #print(assigned, count)
    return count

part2 = 0
for m in tqdm.tqdm(machines):
    x_syms = sympy.symbols(f'x:{len(m.buttons)}')
    equations = []
    for i, j in enumerate(m.joltages):
        eq = None
        for k, b in enumerate(m.buttons):
            if i in b:
                if eq is None:
                    eq = x_syms[k]
                else:
                    eq = eq + x_syms[k]

        eq = sympy.Eq(eq, j)
        equations.append(eq)

    #print(equations)
    solution = sympy.solve(equations)
    free_vars = set.union(*(eq.free_symbols for eq in solution.values()))
    sol = button_presses(m, solution, {}, list(free_vars))
    #print(sol)
    part2 += sol

print(f"Part 2:", part2)
