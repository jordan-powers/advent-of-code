from pathlib import Path

in_path = Path.cwd() / "input.txt"

nums = []

search = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

lines = []



def find_item(line: str, from_back = False) -> int:
    itr = range(len(line)-1, -1, -1) if from_back else range(len(line))
    for i in itr:
        for key in search.keys():
            if i + len(key) > len(line):
                continue
            if line[i:i+len(key)] == key:
                return search[key]

    raise ValueError(f'Could not find value in "{line}"')


with in_path.open("r") as inf:
    lines = inf.readlines()

# lines = """
# two1nine
# eightwothree
# abcone2threexyz
# xtwone3four
# 4nineeightseven2
# zoneight234
# 7pqrstsixteen
# """.strip().split('\n')

for line in lines:
    first = find_item(line, False)
    last = find_item(line, True)
    num = first * 10 + last
    nums.append(num)

    print(f"{num}: {line.strip()}")

print("Solution:", sum(nums))
