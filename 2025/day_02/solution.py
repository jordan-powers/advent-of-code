from pathlib import Path
import math

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

invalid_sum = 0
for irange in input.split(','):
    start, end = irange.split('-')
    start = int(start)
    end = int(end)

    for j in range(start, end+1):
        n = int(math.log10(j))
        if n % 2 == 0:
            continue
        divisor = 10**((n + 1) / 2)
        if j // divisor == j % divisor:
            invalid_sum += j

print("Part 1", invalid_sum)

print('\n\n')

invalid_sum = 0
for irange in input.split(','):
    start, end = irange.split('-')
    start = int(start)
    end = int(end)

    for j in range(start, end+1):
        n = int(math.log10(j))
        maxn = int((n + 1) / 2)
        for ni in range(1, maxn+1):
            divisor = 10**ni
            isseq = True
            part = j % divisor
            left = j // divisor
            if part == 0 or int(math.log10(part)) != ni-1:
                continue
            while left > 0:
                if left % divisor != part:
                    isseq = False
                    break
                left = left // divisor
            if isseq:
                print(j)
                invalid_sum += j
                break

print("Part 2", invalid_sum)
