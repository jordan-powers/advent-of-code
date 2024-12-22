from pathlib import Path

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
1
10
100
2024
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

def calc_sn(sn):
    sn = ((sn << 6) ^ sn) & 0xFFFFFF
    sn = ((sn >> 5) ^ sn) & 0xFFFFFF
    sn = ((sn << 11) ^ sn) & 0xFFFFFF
    return sn

monkey_nums = [int(n) for n in input.splitlines()]

# curr = 123
# for i in range(10):
#     curr = calc_sn(curr)
#     print(f'{i+1:<2} {curr}')

sol1 = 0
for n in monkey_nums:
    sn = n
    for _ in range(2000):
        sn = calc_sn(sn)
    sol1 += sn
    if USE_SAMPLE_INPUT:
        print(f"{n}: {sn}")

print(f"Part 1: {sol1}")

if USE_SAMPLE_INPUT:
    input = """
1
2
3
2024
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

monkey_nums = [int(n) for n in input.splitlines()]

seq_accumulator = {}
for n in monkey_nums:
    prev_diffs = []
    curr_seqs = set()

    curr = n
    for _ in range(2000):
        next = calc_sn(curr)
        diff = (next%10) - (curr%10)
        curr = next
        prev_diffs.append(diff)
        if len(prev_diffs) > 4:
            prev_diffs.pop(0)
        if len(prev_diffs) == 4:
            key = tuple(prev_diffs)
            if key not in curr_seqs:
                curr_seqs.add(key)
                seq_accumulator[key] = seq_accumulator.get(key, 0) + (curr % 10)

best = max(seq_accumulator.items(), key=lambda x: x[1])
# print(best)

print(f'Part 2: {best[1]}')
