from pathlib import Path

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""".strip()

else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

grid = input.split('\n')

dirs = [
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1)
]

rolls = []

for r in range(len(grid)):
    for c in range(len(grid[0])):
        if grid[r][c] != '@':
            continue
        roll_count = 0
        for dir in dirs:
            rt = r + dir[0]
            ct = c + dir[1]
            if rt < 0 or rt >= len(grid) or ct < 0 or ct >= len(grid[0]):
                continue
            if grid[rt][ct] == '@':
                roll_count += 1
        if roll_count < 4:
            rolls.append((r, c))

print("Part 1:", len(rolls))

counts = [[-1] * len(grid[0]) for _ in range(len(grid))]
for r in range(len(grid)):
    for c in range(len(grid[0])):
        if grid[r][c] != '@':
            continue
        roll_count = 0
        for dir in dirs:
            rt = r + dir[0]
            ct = c + dir[1]
            if rt < 0 or rt >= len(grid) or ct < 0 or ct >= len(grid[0]):
                continue
            if grid[rt][ct] == '@':
                roll_count += 1
        counts[r][c] = roll_count

def print_counts():
    for row in counts:
        for c in row:
            if c == -1:
                print('.', end='')
            else:
                print('@', end='')
        print()
    print('\n\n')

print_counts()

total_removed = 0
while True:
    new_counts = [[c for c in r] for r in counts]
    removed_count = 0
    for r in range(len(counts)):
        for c in range(len(counts[0])):
            if counts[r][c] >= 0 and counts[r][c] < 4:
                removed_count += 1
                new_counts[r][c] = -1
                for dir in dirs:
                    rt = r + dir[0]
                    ct = c + dir[1]
                    if rt < 0 or rt >= len(grid) or ct < 0 or ct >= len(grid[0]):
                        continue
                    if counts[rt][ct] > 0 and new_counts[rt][ct] >= 0:
                        new_counts[rt][ct] -= 1
    counts = new_counts
    total_removed += removed_count
    if removed_count == 0:
        break

print("Part 2:", total_removed)
