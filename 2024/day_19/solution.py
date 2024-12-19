from pathlib import Path

from functools import cache

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

towels, patterns = input.split("\n\n")
towels = [t.strip() for t in towels.split(",")]

patterns = patterns.splitlines()

class Solution:
    def __init__(self, towel_counts: 'dict[str, int]' = {}):
        self.towel_counts = towel_counts

    def __hash__(self):
        counts = (self.towel_counts.get(towel, 0) for towel in towels)
        return hash(counts)

    def __eq__(self, other):
        if not isinstance(other, Solution):
            return False
        for towel in towels:
            if self.towel_counts.get(towel, 0) != other.towel_counts.get(towel, 0):
                return False
        return True

    def __add__(self, other):
        if isinstance(other, Solution):
            copy = self.towel_counts.copy()
            for towel, count in other.towel_counts.items():
                copy[towel] = copy.get(towel, 0) + count
            return Solution(copy)
        elif isinstance(other, str):
            assert other in towels
            copy = self.towel_counts.copy()
            copy[other] = copy.get(other, 0) + 1
            return Solution(copy)
        else:
            raise ValueError('Unsupported type')

    def __str__(self):
        return str(self.towel_counts)

    def __repr__(self):
        return f'Solution({str(self)})'

@cache
def find_all_solutions(pattern: str) -> 'set[Solution]':
    #print(pattern)
    if len(pattern) == 0:
        return set((Solution(),))

    solutions: 'set[Solution]' = set()
    for towel in towels:
        idx = 0
        while True:
            idx = pattern.find(towel, idx)
            if idx < 0:
                break

            prefix = pattern[:idx]
            postfix = pattern[idx + len(towel):]
            #print(prefix + ('*' * len(towel)) + postfix)

            prefix_solutions = find_all_solutions(prefix)
            postfix_solutions = find_all_solutions(postfix)

            #print('prefix_solutions:', prefix_solutions)
            #print('postfix_solutions:', postfix_solutions)

            for presol in prefix_solutions:
                for postsol in postfix_solutions:
                    sol = presol + postsol + towel
                    solutions.add(sol)

            idx += 1
    return solutions

@cache
def find_any_solution(pattern: str) -> 'Solution|None':
    #print(pattern)
    if len(pattern) == 0:
        return Solution()

    for towel in towels:
        idx = 0
        while True:
            idx = pattern.find(towel, idx)
            if idx < 0:
                break

            prefix = pattern[:idx]
            postfix = pattern[idx + len(towel):]
            #print(prefix + ('*' * len(towel)) + postfix)

            prefix_solution = find_any_solution(prefix)
            postfix_solution = find_any_solution(postfix)

            if prefix_solution is not None and postfix_solution is not None:
                return prefix_solution + postfix_solution + towel

            idx += 1
    return None


def find_all_solutions_2(pattern: str) -> 'set[Solution]':
    print(pattern)
    if len(pattern) == 0:
        return set((Solution(),))

    solutions: 'set[Solution]' = set()
    for towel in towels:
        if pattern.endswith(towel):
            solutions.update(sol + towel for sol in find_all_solutions_2(pattern[:-len(towel)]))

    return solutions

def find_all_solutions_3(pattern: str) -> 'set[tuple[int]]':
    solutions_cache: 'list[tuple[int]]' = [set((tuple(0 for t in towels),))]
    for i in range(1, len(pattern)+1):
        curr = pattern[:i]
        solutions_cache.append(set())
        print(curr)
        for towel in towels:
            if curr.endswith(towel):
                sub_solutions = solutions_cache[i-len(towel)]
                #print(curr, towel, solutions)
                solutions_cache[i].update(f'{sol},{towel}' for sol in sub_solutions)
    return solutions_cache[-1]

def build_solutions_cache(solutions_cache: 'dict[str, set[Solution]]', max_len: int):
    from queue import Queue
    to_do: 'Queue[str]' = Queue()

    solutions_cache[''] = set((Solution(),))

    to_do.put('')

    while to_do.qsize() > 0:
        curr = to_do.get()

        for towel in towels:
            next = curr + towel
            if len(next) > max_len:
                continue

            solutions_cache.setdefault(next, set()).update(sol + towel for sol in solutions_cache[curr])
            to_do.put(next)

def count_all_solutions_3(pattern: str) -> 'int':
    solutions_count: 'list[int]' = [1]
    for i in range(1, len(pattern)+1):
        curr = pattern[:i]
        solutions_count.append(0)
        #print(curr)
        for towel in towels:
            if curr.endswith(towel):
                solutions_count[i] += solutions_count[i-len(towel)]
    return solutions_count[-1]

# sol1 = 0
# for pattern in patterns:
#     solution = find_any_solution(pattern)
#     #print(pattern, solution)
#     if solution is not None:
#         sol1 += 1

# print(f"Part 1: {sol1}")

# print(find_all_solutions_3(patterns[0]))
# exit(1)

sol2 = 0
for pattern in patterns:
    sol_count = count_all_solutions_3(pattern)
    print(pattern, sol_count)
    sol2 += sol_count

print(f"Part 2: {sol2}")
