from pathlib import Path

USE_SAMPLE_INPUT = False

in_path = Path.cwd() / 'input.txt'

sample_input = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".strip()

if USE_SAMPLE_INPUT:
    input = sample_input
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

input = input.split('\n')

in_num = False
nums = '0123456789'

def get_test_points(area_size: 'tuple(int, int)', x: int, x2: int, y: int) -> 'list[tuple(int, int)]':
    test_points = []
    x_range_min = max(x-1, 0)
    x_range_max = min(x2+1, area_size[0])

    if y > 0:
        for x3 in range(x_range_min, x_range_max):
            test_points.append((x3, y-1))

    if x_range_min < x:
        test_points.append((x_range_min, y))

    if x_range_max > x2:
        test_points.append((x2, y))

    if y+1 < area_size[1]:
        for x3 in range(x_range_min, x_range_max):
            test_points.append((x3, y+1))

    return test_points


part_sum = 0

for y in range(len(input)):
    in_num = False
    for x in range(len(input[0])):
        c = input[y][x]
        if c in nums:
            if in_num:
                continue

            in_num = True

            x2 = x
            while x2 < len(input[0]) and input[y][x2] in nums:
                x2 += 1
            full_num = input[y][x:x2]

            test_points = get_test_points((len(input[0]), len(input)), x, x2, y)

            is_part_no = False
            for point in test_points:
                c2 = input[point[1]][point[0]]
                if c2 != '.' and c2 not in nums:
                    is_part_no = True
                    break

            print(y, full_num, is_part_no)

            if is_part_no:
                part_sum += int(full_num)

        else:
            in_num = False

print(f"Part 1: {part_sum}")

class Number:
    next_num_id = 1
    def __init__(self, value: int):
        self.value = value
        self.id = Number.next_num_id
        Number.next_num_id += 1

    def __eq__(self, other) -> bool:
        return isinstance(other, Number) and other.id == self.id

    def __hash__(self) -> int:
        return self.id

class Symbol:
    def __init__(self, value: str):
        self.value = value

grid = [[None for _ in range(len(input[0]))] for _ in range(len(input))]

for y in range(len(input)):
    curr_num = None
    for x in range(len(input[0])):
        c = input[y][x]
        if c in nums:
            if curr_num is not None:
                grid[y][x] = curr_num
                continue

            x2 = x
            while x2 < len(input[0]) and input[y][x2] in nums:
                x2 += 1
            full_num = input[y][x:x2]

            curr_num = Number(int(full_num))
            grid[y][x] = curr_num
        else:
            curr_num = None

            if c != '.':
                grid[y][x] = Symbol(c)

sum_ratios = 0
for y in range(len(grid)):
    for x in range(len(grid[0])):
        obj = grid[y][x]
        if isinstance(obj, Symbol) and obj.value == '*':
            test_points = get_test_points((len(input[0]), len(input)), x, x+1, y)
            nums = set()
            for point in test_points:
                obj2 = grid[point[1]][point[0]]

                if isinstance(obj2, Number):
                    nums.add(obj2)

            nums = list(nums)
            if len(nums) == 2:
                print(f'Gear at ({x}, {y}): {nums[0].value} * {nums[1].value} = {nums[0].value * nums[1].value}')
                sum_ratios += nums[0].value * nums[1].value

print('Part 2:', sum_ratios)
