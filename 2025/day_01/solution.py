from pathlib import Path

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

dial = 50
passwd = 0
for l in input.split():
    c = l[0]
    n = int(l[1:])
    if c == 'L':
        n = 100 - n
    dial = (dial + n) % 100
    print(l, dial)
    if dial == 0:
        passwd += 1

print("Part 1:", passwd)

print("\n\n")

dial = 50
passwd = 0
for l in input.split():
    c = l[0]
    n = int(l[1:])
    iterPass = 0
    iterPass += n // 100
    n = n % 100
    if c == 'L':
        n = -n
    if dial == 0 and c == 'L':
        dial = 100
    dial += n
    if dial >= 100:
        iterPass += 1
        dial -= 100
    elif dial < 0:
        iterPass += 1
        dial += 100
    elif dial == 0:
        iterPass += 1
    passwd += iterPass
    print(l, dial, iterPass, passwd)

print("Part 2:", passwd)
