from pathlib import Path
import math
from tqdm import trange

import functools

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = "125 17"
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

stones = [int(i) for i in input.split()]

def blink(stones):
    i = 0
    while i < len(stones):
        stone = stones[i]
        if stone == 0:
            stones[i] = 1
            i += 1
            continue

        num_digits = math.floor(math.log10(stone))+1
        if num_digits % 2 == 0:
            split = 10 ** (num_digits // 2)
            left = stone // split
            right = stone % split
            stones[i] = left
            i += 1
            stones.insert(i, right)
            i += 1
            continue

        stones[i] = stone * 2024
        i += 1

# print(stones)
# for i in range(6):
#     blink(stones)
#     print(stones)

for i in trange(25, miniters=1):
    blink(stones)

print(f"Part 1: {len(stones)}")

stones = [int(i) for i in input.split()]

@functools.cache
def count_children(stone, niter):
    if niter == 0:
        return 1

    if stone == 0:
        return count_children(1, niter-1)

    num_digits = math.floor(math.log10(stone))+1
    if num_digits % 2 == 0:
        split = 10 ** (num_digits // 2)
        left = stone // split
        right = stone % split
        return count_children(left, niter-1) + count_children(right, niter-1)

    return count_children(stone * 2024, niter-1)

sol1 = sum(count_children(s, 25) for s in stones)
print(f"Part 1 (again): {sol1}")

stones = [int(i) for i in input.split()]

sol2 = sum(count_children(s, 75) for s in stones)
print(f"Part 2: {sol2}")
