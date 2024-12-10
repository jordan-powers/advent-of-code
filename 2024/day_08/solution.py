from pathlib import Path

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

input = input.splitlines()

antenna_positions: 'dict[char,set[tuple[int, int]]]' = {}
for r, row in enumerate(input):
    for c, char in enumerate(row):
        if char != '.':
            antenna_positions.setdefault(char, set()).add((r, c))

def combos(pointset: 'set[tuple[int,int]]') -> 'set[tuple[tuple[int,int], tuple[int,int]]]':
    points = list(pointset)
    outset = set()
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            outset.add((points[i], points[j]))
    return outset

def test_in_bounds(point: 'tuple[int,int]') -> 'bool':
    return point[0] >= 0 and point[1] >= 0 and point[0] < len(input) and point[1] < len(input[0])

nodes: 'set[tuple[int,int]]' = set()
for a, pointset in antenna_positions.items():
    comboset = combos(pointset)
    for p1, p2 in comboset:
        diff = (p2[0] - p1[0], p2[1] - p1[1])
        n1 = (p2[0] + diff[0], p2[1] + diff[1])
        n2 = (p1[0] - diff[0], p1[1] - diff[1])
        if test_in_bounds(n1):
            nodes.add(n1)
        if test_in_bounds(n2):
            nodes.add(n2)

input = [list(r) for r in input]

# for n in nodes:
#     input[n[0]][n[1]] = '#'

# for r in input:
#     print(''.join(r))

print(f'Part 1: {len(nodes)}')

nodes: 'set[tuple[int,int]]' = set()
for a, pointset in antenna_positions.items():
    comboset = combos(pointset)
    for p1, p2 in comboset:
        diff = (p2[0] - p1[0], p2[1] - p1[1])
        curr = p2
        while test_in_bounds(curr):
            nodes.add(curr)
            curr = (curr[0] + diff[0], curr[1] + diff[1])
        curr = p1
        while test_in_bounds(curr):
            nodes.add(curr)
            curr = (curr[0] - diff[0], curr[1] - diff[1])

for n in nodes:
    input[n[0]][n[1]] = '#'

for r in input:
    print(''.join(r))

print(f'Part 2: {len(nodes)}')
