from pathlib import Path

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
""".strip()

else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

input = [[c for c in line] for line in input.split('\n')]

beams = set()
for i, char in enumerate(input[0]):
    if char == 'S':
        beams.add(i)

def print_beams(crow):
    for i, row in enumerate(input):
        if i == crow:
            for j, c in enumerate(row):
                if j in beams:
                    print('|', end='')
                else:
                    print(c, end='')
            print()
        else:
            print(''.join(row))

splitcount = 0
for i, row in enumerate(input[1:]):
    new_beams = set()
    #print_beams(i+1)
    for beam in beams:
        if row[beam] == '^':
            splitcount += 1
            if beam > 0:
                new_beams.add(beam - 1)
            if beam < len(row)-1:
                new_beams.add(beam + 1)
        else:
            assert row[beam] == '.'
            new_beams.add(beam)
    beams = new_beams
    #print()

print("Part 1", splitcount)

beams = [0 for _ in range(len(input[0]))]
for i, char in enumerate(input[0]):
    if char == 'S':
        beams[i] = 1

def print_beams_2(crow):
    for i, row in enumerate(input):
        if i == crow:
            for j, c in enumerate(row):
                if beams[j] > 0:
                    print(f'{beams[j]:02}', end='')
                else:
                    print(' ' + c, end='')
            print()
        else:
            print(' '.join(row))

for i, row in enumerate(input[1:]):
    new_beams = [0 for _ in range(len(row))]
    #print_beams_2(i+1)
    for j, c in enumerate(row):
        if beams[j] == 0:
            continue
        if c == '^':
            if j > 0:
                new_beams[j - 1] += beams[j]
            if j < len(row) - 1:
                new_beams[j + 1] += beams[j]
        else:
            assert c == '.'
            new_beams[j] += beams[j]
    beams = new_beams
    #print()

print("Part 2", sum(beams))
