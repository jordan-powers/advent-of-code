from pathlib import Path
import time

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

input = [list(s) for s in input.split("\n")]

input_part2 = [s.copy() for s in input]

def find_char_pos(input):
    for r, row in enumerate(input):
        for c, char in enumerate(row):
            if char == '^':
                return (r, c)

    for r in input:
        print(''.join(r))
    raise ValueError("No ^ in input!")

curr_pos = find_char_pos(input)

def pos_in_bounds(pos):
    return pos[0] >= 0 and pos[1] >= 0 and pos[0] < len(input) and pos[1] < len(input[0])

dirs = [
    (-1, 0),
    (0, 1),
    (1, 0),
    (0, -1)
]

def calc_next_pos(curr_pos, dir_idx):
    curr_dir = dirs[dir_idx % len(dirs)]
    return (curr_pos[0] + curr_dir[0], curr_pos[1] + curr_dir[1])

def is_obstacle(pos):
    if not pos_in_bounds(pos):
        return False
    return input[pos[0]][pos[1]] == '#'

curr_dir_idx = 0
while pos_in_bounds(curr_pos):
    next_pos = calc_next_pos(curr_pos, curr_dir_idx)
    while is_obstacle(next_pos):
        curr_dir_idx = (curr_dir_idx + 1) % len(dirs)
        next_pos = calc_next_pos(curr_pos, curr_dir_idx)
    input[curr_pos[0]][curr_pos[1]] = 'X'
    curr_pos = next_pos

sol1 = 0
for row in input:
    for col in row:
        if col == 'X':
            sol1 += 1

# for line in input:
#     print(''.join(line))
print(f"Part 1: {sol1}")

def is_loop(input):
    prev_path = set()
    curr_pos = find_char_pos(input)
    curr_dir_idx = 0

    while True:
        # time.sleep(0.25)

        # print()
        # for r in input:
        #     print(''.join(r))
        # print(curr_pos, curr_dir_idx)

        if not pos_in_bounds(curr_pos):
            return False

        next_pos = calc_next_pos(curr_pos, curr_dir_idx)
        while is_obstacle(next_pos):
            curr_dir_idx = (curr_dir_idx + 1) % len(dirs)
            next_pos = calc_next_pos(curr_pos, curr_dir_idx)

        curr_posdir = (curr_pos[0], curr_pos[1], curr_dir_idx)
        if curr_posdir in prev_path:
            return True
        prev_path.add(curr_posdir)

        input[curr_pos[0]][curr_pos[1]] = 'X'
        curr_pos = next_pos

# input = [c.copy() for c in input_part2]
# input[7][6] = '#'
# is_loop(input)

# exit(1)

sol2 = 0

for r, row in enumerate(input_part2):
    for c, col in enumerate(row):
        input = [c.copy() for c in input_part2]
        # print(r, c, col)
        if col not in ('#', '^'):
            input[r][c] = '#'
            if is_loop(input):
                # print(f"Found loop at ({r}, {c})")
                sol2 += 1

print(f"Part 2: {sol2}")
