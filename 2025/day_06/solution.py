from pathlib import Path

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    with (Path.cwd() / 'sample_input.txt').open("r") as inf:
        input = inf.read()
else:
    with in_path.open("r") as inf:
        input = inf.read()[:-1]

lines = input.split("\n")

nums = [[int(n) for n in row.split()] for row in lines[:-1]]
ops = lines[-1].split()

assert len(ops) == len(nums[0])

results: 'list[int]' = []

for col in range(len(ops)):
    op = ops[col]
    if op == '+':
        result = 0
    else:
        assert op == '*'
        result = 1

    for row in nums:
        if op == '+':
            result += row[col]
        else:
            assert op == '*'
            result *= row[col]
    results.append(result)

#print(results)
print("Part 1", sum(results))

problems: 'list[list[str]]' = []

prev_i = None
for i, c in enumerate(lines[-1]):
    if c == ' ':
        continue
    if prev_i == None:
        prev_i = i
        continue

    prob = slice(prev_i, i-1)
    prev_i = i
    curr_prob = []
    for row in lines[:-1]:
        curr = row[prob]
        curr_prob.append(curr)
    problems.append(curr_prob)

prob = slice(prev_i, len(lines[-1]))
curr_prob = []
for row in lines[:-1]:
    curr = row[prob]
    curr_prob.append(curr)
problems.append(curr_prob)

total = 0
for i, problem in enumerate(problems):
    op = ops[i]
    if op == '+':
        result = 0
    else:
        assert op == '*'
        result = 1

    for j in range(len(problem[0])):
        n = ''
        for p in problem:
            if p[j] != ' ':
                n += p[j]
        n = int(n)
        if op == '+':
            result += n
        else:
            assert op == '*'
            result *= n
    total += result

print("Part 2", total)
