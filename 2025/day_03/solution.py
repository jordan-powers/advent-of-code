from pathlib import Path
from tqdm import tqdm

from multiprocessing import Pool

def calc_joltage(bank, joltage):
        if bank == '':
            return 0

        if joltage == 0:
            j1 = calc_joltage(bank[1:], int(bank[0]) * 10)
            j2 = calc_joltage(bank[1:], 0)
        else:
            assert joltage % 10 == 0
            j1 = joltage + int(bank[0])
            j2 = calc_joltage(bank[1:], joltage)

        return max(j1, j2)

def calc_joltage_2(bank, joltage=0, rem_bat=12, best_so_far=0):
        if rem_bat == 0:
            return joltage
        max_bound = (joltage+1) * (10 ** rem_bat)
        if max_bound < best_so_far:
            return 0
        if bank == '':
            return 0
        j1 = calc_joltage_2(bank[1:], (joltage * 10) + int(bank[0]), rem_bat-1, best_so_far)

        i = 1
        while i < len(bank) and bank[i] == bank[0]:
            i += 1
        j2 = calc_joltage_2(bank[i:], joltage, rem_bat, max(j1, best_so_far))

        return max(j1, j2)

if __name__ == '__main__':

    USE_SAMPLE_INPUT = False
    in_path = Path.cwd() / 'input.txt'

    if USE_SAMPLE_INPUT:
        input = """
    987654321111111
    811111111111119
    234234234234278
    818181911112111
    """.strip()
    else:
        with in_path.open("r") as inf:
            input = inf.read().strip()

    total_joltage = 0
    for bank in input.split('\n'):
        joltage = calc_joltage(bank, 0)
        # print(bank, joltage)
        total_joltage += joltage

    print("Part 1:", total_joltage)

    print("\n\n")

    with Pool(16) as p:
         joltages = list(tqdm(p.imap(calc_joltage_2, input.split('\n')), total=200))

    print("Part 2:", sum(joltages))
