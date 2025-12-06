from pathlib import Path

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
""".strip()

else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

fresh: 'set[int]' = set()

intervals, ingredients = input.split('\n\n')
intervals = [(int(s), int(e)) for s, e in (i.split('-') for i in intervals.split('\n'))]
intervals.sort(key=lambda x: x[0])

merged_intervals = []
cint = intervals[0]
for interval in intervals[1:]:
    if interval[0] <= cint[1]:
        cint = (cint[0], max(cint[1], interval[1]))
    else:
        merged_intervals.append(cint)
        cint = interval

merged_intervals.append(cint)

fresh_count = 0
for ingredient in ingredients.split('\n'):
    ingredient = int(ingredient)
    fresh = False
    for interval in merged_intervals:
        if ingredient >= interval[0] and ingredient <= interval[1]:
            fresh = True
            break
    if fresh:
        fresh_count += 1

print("Part 1:", fresh_count)

fresh_count = 0
for interval in merged_intervals:
    fresh_count += interval[1] - interval[0] + 1

print("Part 2:", fresh_count)
