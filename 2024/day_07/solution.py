from pathlib import Path
from tqdm import tqdm
import math

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

def is_solvable(result, operands):
    if len(operands) == 1:
        return result == operands[0]

    curr = operands[-1]
    rest = operands[:-1]

    # PLUS
    if is_solvable(result - curr, rest):
        return True

    # # MINUS
    # if is_solvable(result + curr, rest):
    #     return True

    # MULT
    if is_solvable(result / curr, rest):
        return True

    # # DIV
    # if is_solvable(result * curr, rest):
    #     return True


    return False

sol1 = 0
for line in tqdm(input.split("\n")):
    split = line.index(':')
    result = int(line[:split])
    operands = tuple(int(n) for n in line[split+1:].split())

    solvable = is_solvable(result, operands)

    #print(line, solvable)

    if solvable:
        sol1 += result

print(f"Part 1: {sol1}")

def is_solvable_2(result, operands):
    # print(result, operands)
    if len(operands) == 1:
        return result == operands[0]

    curr = operands[-1]
    rest = operands[:-1]

    # PLUS
    if is_solvable_2(result - curr, rest):
        return True

    # MULT
    if result % curr == 0 and is_solvable_2(result // curr, rest):
        return True

    # CONCAT
    if str(result).endswith(str(curr)):
        #print(">>", curr, math.floor(math.log10(curr)), (10**(math.floor(math.log10(curr)) + 1)), result // (10**(math.floor(math.log10(curr)) + 1)))
        if is_solvable_2(result // (10**(math.floor(math.log10(curr)) + 1)), rest):
            return True

    return False

sol2 = 0
for line in input.split("\n"): #tqdm(input.split("\n")):
    split = line.index(':')
    result = int(line[:split])
    operands = tuple(int(n) for n in line[split+1:].split())

    solvable = is_solvable_2(result, operands)

    # print(line, solvable)

    if solvable:
        sol2 += result

print(f"Part 2: {sol2}")
