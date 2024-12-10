from pathlib import Path

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = "2333133121414131402"
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

disk = ['.'] * sum(int(i) for i in input)

curr = 0
id = 0
free = False
for i in input:
    for j in range(int(i)):
        if free:
            disk[curr] = '.'
        else:
            disk[curr] = str(id)
        curr += 1
    if not free:
        id += 1
    free = not free

def is_compact(disk):
    try:
        pos = disk.index('.')
        return all(d == '.' for d in disk[pos:])
    except ValueError:
        return True

def calc_checksum(disk):
    csm = 0
    for i in range(len(disk)):
        if disk[i] != '.':
            csm += i * int(disk[i])
    return csm

dest = 0
source = len(disk)-1

while True:
    while disk[source] == '.' and dest < source:
        source -= 1
    while disk[dest] != '.' and dest < source:
        dest += 1
    if dest >= source:
        break
    disk[source], disk[dest] = disk[dest], disk[source]
    #print(''.join(disk))

print(f'Part 1: {calc_checksum(disk)}')

free_spaces_by_size: 'dict[int, set[int]]' = {}
disk: 'dict[int, tuple[str, int]]' = {}

def register_free_space(pos, size):
    assert pos not in disk
    disk[pos] = ('.', size)
    for j in range(1, size+1):
        free_spaces_by_size.setdefault(j, set()).add(pos)
def deregister_free_space(pos):
    assert disk[pos][0] == '.'
    for j in range(1, disk[pos][1]+1):
        free_spaces_by_size[j].remove(pos)
    del disk[pos]

free = False
id = 0
pos = 0
for i in input:
    if free:
        register_free_space(pos, int(i))
    else:
        disk[pos] = (str(id), int(i))
        id += 1
    pos += int(i)
    free = not free

def ckfs(disk: 'dict[int, tuple[str, int]]'):
    items = sorted(disk.items(), key=lambda x: x[0])
    calc_idx = 0
    for idx, (type, size) in items:
        assert calc_idx == idx
        calc_idx += size

def print_disk(disk: 'dict[int, tuple[str, int]]'):
    items = sorted(disk.items(), key=lambda x: x[0])
    for idx, (type, size) in items:
        print(type * size, end='')
    print()

#print_disk(disk)

files = sorted(((d[0], d[1][0], d[1][1]) for d in disk.items() if d[1][0] != '.'), key=lambda x: int(x[1]), reverse=True)

for pos, id, size in files:
    if size not in free_spaces_by_size:
        continue

    dest_pos = min(free_spaces_by_size[size])

    if dest_pos > pos:
        continue

    dest_size = disk[dest_pos][1]

    deregister_free_space(dest_pos)

    new_size = dest_size - size
    if new_size > 0:
        register_free_space(dest_pos + size, new_size)

    disk[dest_pos] = (id, size)
    del disk[pos]
    register_free_space(pos, size)

    #ckfs(disk)

    #print_disk(disk)

def calc_checksum2(disk: 'dict[int, tuple[str, int]]'):
    csm = 0
    for idx, (id, size) in disk.items():
        if id == '.':
            continue
        for i in range(idx, idx+size):
            csm += i * int(id)
    return csm

print(f"Part 2: {calc_checksum2(disk)}")

