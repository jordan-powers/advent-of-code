from pathlib import Path

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        assert isinstance(other, Vec2)
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        assert isinstance(other, Vec2)
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        assert isinstance(other, int) or isinstance(other, float)
        return Vec2(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mod__(self, other):
        assert isinstance(other, Vec2)
        return Vec2(self.x % other.x, self.y % other.y)

    def __eq__(self, other):
        return isinstance(other, Vec2) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return "Vec2" + str(self)

class Robot:
    def __init__(self, pos: Vec2, vel: Vec2):
        self.pos = pos
        self.vel = vel

    def __str__(self):
        return f"Robot(pos={str(self.pos)}, vel={str(self.vel)})"

    def __repr__(self):
        return str(self)

if USE_SAMPLE_INPUT:
    input = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

dirs = {
    '^': Vec2(0, -1),
    '>': Vec2(1, 0),
    'v': Vec2(0, 1),
    '<': Vec2(-1, 0)
}

board, moves = input.split("\n\n")
moves = moves.replace("\n", "")

moves_str = moves
moves = [dirs[d] for d in moves]

board = [list(line) for line in board.splitlines()]
board_orig = [row.copy() for row in board]

def find_robot(board: 'list[list[str]]'):
    for r, row in enumerate(board):
        for c, char in enumerate(row):
            if char == '@':
                return Vec2(c, r)

    raise ValueError('Could not find \'@\' in input!')

def move_char(board: 'list[list[str]]', pos: Vec2, dir: Vec2):
    curr_char = board[pos.y][pos.x]

    if curr_char == '#':
        return False
    if curr_char == '.':
        return True

    next_pos = pos + dir
    if not move_char(board, next_pos, dir):
        return False

    board[next_pos.y][next_pos.x] = curr_char
    board[pos.y][pos.x] = '.'
    return True

def print_board(board: 'list[list[str]]'):
    print(f'\n'.join(''.join(row) for row in board))

def gps_sum(board: 'list[list[str]]'):
    gsum = 0
    for r, row in enumerate(board):
        for c, char in enumerate(row):
            if char in 'O[':
                gps = (r * 100) + c
                gsum += gps
    return gsum

robot_pos = find_robot(board)

for i, move in enumerate(moves):
    # print(f'Step {i} ({moves_str[i]}):')
    if move_char(board, robot_pos, move):
        robot_pos = robot_pos + move
    # print_board(board)
    # print()

print(f"Part 1: {gps_sum(board)}")

board_2: 'list[list[str]]' = []
for row in board_orig:
    row2 = []
    for char in row:
        if char == '@':
            row2 += ['@', '.']
        elif char == 'O':
            row2 += ['[', ']']
        else:
            row2 += [char, char]
    board_2.append(row2)

def can_move_char(board: 'list[list[str]]', pos: Vec2, dir: Vec2):
    curr_char = board[pos.y][pos.x]

    if curr_char == '#':
        return False
    elif curr_char == '.':
        return True

    check_pts = [pos + dir]

    if dir.y != 0:
        if curr_char == '[':
            box2 = pos + Vec2(1, 0)
            assert board[box2.y][box2.x] == ']'
            check_pts.append(box2 + dir)
        elif curr_char == ']':
            box2 = pos + Vec2(-1, 0)
            assert board[box2.y][box2.x] == '['
            check_pts.append(box2 + dir)

    for next_pos in check_pts:
        if not can_move_char(board, next_pos, dir):
            return False

    return True

def do_move_char(board: 'list[list[str]]', pos: Vec2, dir: Vec2):
    curr_char = board[pos.y][pos.x]
    #print(pos, curr_char)
    assert curr_char != '#'
    if curr_char == '.':
        return

    move_pts = [pos]
    if dir.y != 0:
        if curr_char == '[':
            box2 = pos + Vec2(1, 0)
            assert board[box2.y][box2.x] == ']'
            move_pts.append(box2)
        elif curr_char == ']':
            box2 = pos + Vec2(-1, 0)
            assert board[box2.y][box2.x] == '['
            move_pts.append(box2)

    for mpos in move_pts:
        npos = mpos + dir
        do_move_char(board, npos, dir)
        board[npos.y][npos.x] = board[mpos.y][mpos.x]
        board[mpos.y][mpos.x] = '.'

robot_pos = find_robot(board_2)

# print_board(board_2)
for i, move in enumerate(moves):
    # print(f'Step {i} ({moves_str[i]}):')
    if can_move_char(board_2, robot_pos, move):
        do_move_char(board_2, robot_pos, move)
        robot_pos = robot_pos + move
    # print_board(board_2)
    # print()

print(f"Part 2: {gps_sum(board_2)}")
