from pathlib import Path
import heapq

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
    def __init__(self, lights, buttons, joltages):
        self.lights = lights
        self.buttons = buttons
        self.joltages = joltages

    # def __str__(self):
    #     return f'[{self.lights}] ' + ' '.join('(' + ','.join(str(b) for b in but) + ')' for but in self.buttons) + f' {{{self.joltages}}}'

    def __repr__(self):
        return f'Machine({repr(self.lights)}, {self.buttons}, {repr(self.joltages)})'

machines: 'list[Machine]' = []

for line in input.split("\n"):
    buttons = []
    for part in line.split():
        if part[0] == '[':
            lights = 0
            for l in part[1:-1][::-1]:
                lights <<= 1
                if l == '#':
                    lights |= 1
        elif part[0] == '(':
            buts = 0
            for b in part[1:-1].split(','):
                buts |= (1 << int(b))
            buttons.append(buts)
        else:
            assert part[0] == '{'
            joltages = part[1:-1]
    machines.append(Machine(lights, buttons, joltages))

# for m in machines:
#     print(m)

class State:
    def __init__(self, presses: 'frozenset[int]', lights: int):
        self.presses = presses
        self.lights = lights

    def __lt__(self, other):
        assert isinstance(other, State)
        return len(self.presses) < len(other.presses)

    def __repr__(self):
        return f'State({self.presses}, {self.lights})'

def solve_buttons_1(m: Machine):
    queue = [State(frozenset(), 0)]
    heapq.heapify(queue)

    seen = set()

    while len(queue) > 0:
        curr = heapq.heappop(queue)

        if curr.lights == m.lights:
            return curr

        for i in range(len(m.buttons)):
            if i in curr.presses:
                continue
            new_presses = curr.presses.union((i,))
            if new_presses in seen:
                continue
            seen.add(new_presses)
            new_lights = curr.lights ^ m.buttons[i]
            heapq.heappush(queue, State(new_presses, new_lights))

    assert False, "No solution found!"


solve_buttons_1(machines[1])


part1 = 0
for m in machines:
    solution = solve_buttons_1(m)
    #print(m, solution)
    part1 += len(solution.presses)

print('Part 1:', part1)
