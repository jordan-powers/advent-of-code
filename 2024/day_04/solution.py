from pathlib import Path

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

input = input.split('\n')

dirs = [
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
    (-1, 0),
    (-1, 1),
]

def test_word(pos, dir, word="XMAS"):
    curr = pos
    for c in word:
        if curr[0] < 0 or curr[0] >= len(input[0]) or curr[1] < 0 or curr[1] >= len(input):
            return False
        #print(c, curr, input[curr[0]][curr[1]])
        if input[curr[0]][curr[1]] != c:
            return False
        curr[0] += dir[0]
        curr[1] += dir[1]
    return True

part1_sol = 0
for r, row in enumerate(input):
    for c, letter in enumerate(row):
        if letter == "X":
            for dir in dirs:
                if test_word([r, c], dir):
                    part1_sol += 1

print(f"Part 1: {part1_sol}")

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

dirs = [Vec2(d[1], d[0]) for d in dirs]

def test_word_vec(pos, dir, word="XMAS"):
    curr = pos
    for c in word:
        if curr.x < 0 or curr.x >= len(input[0]) or curr.y < 0 or curr.y >= len(input):
            return False
        #print(c, curr, input[curr[0]][curr[1]])
        if input[curr.y][curr.x] != c:
            return False
        curr += dir
    return True

def test_mas(pos, diridx):
    x1 = test_word_vec(pos + dirs[diridx], dirs[(diridx + 4) % 8], "MAS") or test_word_vec(pos + dirs[diridx], dirs[(diridx + 4) % 8], "SAM")
    x2 = test_word_vec(pos + dirs[(diridx + 2) % 8], dirs[(diridx + 6) % 8], "MAS") or test_word_vec(pos + dirs[(diridx + 2) % 8], dirs[(diridx + 6) % 8], "SAM")

    return x1 and x2

output = [['.'] * len(r) for r in input]

def inc_str(s):
    if s == '.':
        return '1'
    else:
        return str(int(s)+1)

def copy_mas(pos, diridx):
    global output
    output[pos.y][pos.x] = input[pos.y][pos.x] #inc_str(output[pos.y][pos.x])
    for i in range(4):
        dir = dirs[(diridx + (2*i)) % 8]
        curr = pos + dir
        output[curr.y][curr.x] = input[curr.y][curr.x] #inc_str(output[curr.y][curr.x])

# input = """
# M.S.M
# .A.A.
# M.S.M
# """.strip().split('\n')

part2_sol = 0
for r, row in enumerate(input):
    for c, letter in enumerate(row):
        if letter == "A":
            # if test_mas(Vec2(c, r), 0):
            #     copy_mas(Vec2(c,r), 0)
            #     part2_sol += 1
            if test_mas(Vec2(c, r), 1):
                copy_mas(Vec2(c,r), 1)
                part2_sol += 1

print(f"Part 2: {part2_sol}")

# output = '\n'.join(''.join(r) for r in output)
# print(output)

