from pathlib import Path

import re

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

searchre = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")

part1_sol = 0
results = searchre.findall(input)
for r in results:
    part1_sol += int(r[0]) * int(r[1])

print(f"Part 1: {part1_sol}")

if USE_SAMPLE_INPUT:
    input = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

searchre = re.compile(r"(?:do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\))")

part2_sol = 0
do = True
for match in searchre.finditer(input):
    if match.group(0) == "do()":
        do = True
    elif match.group(0) == "don't()":
        do = False
    elif do:
        part2_sol += int(match.group(1)) * int(match.group(2))

print(f"Part 2: {part2_sol}")
