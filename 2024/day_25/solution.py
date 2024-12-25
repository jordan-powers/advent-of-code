from pathlib import Path

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

locks = set()
keys = set()

input = input.split('\n\n')
for entity in input:
    lines = entity.splitlines()
    is_lock = all(c == '#' for c in lines[0]) and all(c == '.' for c in lines[-1])
    is_key = all(c == '.' for c in lines[0]) and all(c == '#' for c in lines[-1])

    assert is_lock != is_key

    if is_lock:
        lines = lines[1:]
    else:
        lines = lines[:-1]

    heights = [0] * len(lines[0])
    for line in lines:
        for c, char in enumerate(line):
            if char == '#':
                heights[c] += 1

    if is_lock:
        locks.add(tuple(heights))
    else:
        keys.add(tuple(heights))

sol1 = 0
for key in keys:
    for lock in locks:
        heights = tuple(key[i] + lock[i] for i in range(len(key)))
        if all(h <= 5 for h in heights):
            sol1 += 1

print(f'Part 1: {sol1}')
