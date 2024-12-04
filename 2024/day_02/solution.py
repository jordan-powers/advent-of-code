from pathlib import Path

if False:
    input_s = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".strip()
else:
    input_p = Path(__file__).parent / 'input.txt'

    assert input_p.is_file()

    with input_p.open('r') as inf:
        input_s = inf.read().strip()

reports = []
for line in input_s.split('\n'):
    line = line.split()
    if not line:
        continue
    report = tuple(int(i) for i in line)
    reports.append(report)

part1_sol = len(reports)
for r in reports:
    #print(r, end='')
    lastdiff = None
    for i in range(1, len(r)):
        diff = r[i] - r[i-1]
        if diff == 0 or abs(diff) > 3:
            #print(f' at {i}, {diff} out of bounds', end='')
            part1_sol -= 1
            break
        if lastdiff is not None and (diff > 0) != (lastdiff > 0):
            #print(f' at {i}, ({diff} > 0) != ({lastdiff} > 0)', end='')
            part1_sol -= 1
            break
        lastdiff = diff

    #print()

print(f"Part 1: {part1_sol}")

def is_safe(r: tuple) -> bool:
    #print(r, end='')
    lastdiff = None
    for i in range(1, len(r)):
        diff = r[i] - r[i-1]
        if diff == 0 or abs(diff) > 3:
            #print(f' fail on {i}, diff={diff}')
            return False
        if lastdiff is not None and (diff > 0) != (lastdiff > 0):
            #print(f' fail on {i}, diff={diff}, lastdiff={lastdiff}')
            return False
        lastdiff = diff
    #print()
    return True

part1_sol = 0
for r in reports:
    if is_safe(r):
        part1_sol += 1

print(f"Part 1 (again): {part1_sol}")

part2_sol = 0
for r in reports:
    if is_safe(r):
        part2_sol += 1
        continue

    for i in range(len(r)):
        subr = r[0:i] + r[i+1:]
        if is_safe(subr):
            part2_sol += 1
            break

print(f"Part 2: {part2_sol}")
