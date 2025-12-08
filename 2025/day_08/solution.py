from pathlib import Path
import math
from collections import defaultdict
import tqdm

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
""".strip()

    num_conns = 10

else:
    with in_path.open("r") as inf:
        input = inf.read().strip()
    num_conns = 1000

class Vec3:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        if not isinstance(other, Vec3):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __add__(self, other):
        assert isinstance(other, Vec3)
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        assert isinstance(other, Vec3)
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def mag(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __repr__(self):
        return f'Vec3({self.x},{self.y},{self.z})'


points: 'set[Vec3]' = set()

for line in input.split('\n'):
    x, y, z = line.split(',')
    points.add(Vec3(int(x), int(y), int(z)))

def closest_pair(points: 'list[Vec3]', exclude_pairs: 'set[tuple[Vec3, Vec3]]') -> 'tuple[int, tuple[Vec3, Vec3]]':
    if len(points) == 1:
        return (math.inf, (points[0], points[0]))
    elif len(points) == 2:
        if (points[1], points[0]) in exclude_pairs or (points[0], points[1]) in exclude_pairs:
            return (math.inf, (points[1], points[0]))
        else:
            return ((points[1] - points[0]).mag(), (points[1], points[0]))

    split = len(points) // 2
    dl, pairl = closest_pair(points[:split], exclude_pairs)
    dr, pairr = closest_pair(points[split:], exclude_pairs)
    if dl < dr:
        d = dl
        pair = pairl
    else:
        d = dr
        pair = pairr

    midX = points[split].x
    merge_set: 'list[Vec3]' = []
    for point in points:
        if abs(point.x - midX) < d:
            merge_set.append(point)

    merge_set.sort(key=lambda p: p.y)
    for i in range(len(merge_set)):
        curr = merge_set[i]
        for j in range(i+1, len(merge_set)):
            test = merge_set[j]
            if test.y - curr.y >= d:
                break
            if (test, curr) in exclude_pairs or (curr, test) in exclude_pairs:
                continue
            currd = (test - curr).mag()
            if currd < d:
                d = currd
                pair = (test, curr)
    merge_set.sort(key=lambda p: p.z)
    for i in range(len(merge_set)):
        curr = merge_set[i]
        for j in range(i+1, len(merge_set)):
            test = merge_set[j]
            if test.z - curr.z >= d:
                break
            if (test, curr) in exclude_pairs or (curr, test) in exclude_pairs:
                continue
            currd = (test - curr).mag()
            if currd < d:
                d = currd
                pair = (test, curr)
    return (d, pair)

sorted_points = sorted(points, key=lambda p: p.x)
exclude_pairs: 'set[Vec3]' = set()
connections: 'dict[Vec3, set[Vec3]]' = defaultdict(set)

for i in tqdm.trange(num_conns, desc="making connections"):
    d, pair = closest_pair(sorted_points, exclude_pairs)
    #print(pair)
    exclude_pairs.add(pair)
    connections[pair[0]].add(pair[1])
    connections[pair[1]].add(pair[0])

#print()

def build_circuit(p: 'Vec3', visited: 'set[Vec3]'):
    if p in visited:
        return
    visited.add(p)
    for conn in connections[p]:
        build_circuit(conn, visited)

all_visited: 'set[Vec3]' = set()
circuits: 'list[set[Vec3]]' = []
for p in tqdm.tqdm(points, desc="finding circuits"):
    if p in all_visited:
        continue
    circuit: 'set[Vec3]' = set()
    build_circuit(p, circuit)
    all_visited.update(circuit)
    circuits.append(circuit)

circuits.sort(key=lambda c: len(c), reverse=True)
part1 = 1
for c in circuits[:3]:
    #print(c)
    part1 *= len(c)

print("Part 1:", part1)


so_far = 0
with tqdm.tqdm(total=len(points), desc="making connections") as pbar:
    while True:
        circuit: 'set[Vec3]' = set()
        build_circuit(next(iter(points)), circuit)
        if len(circuit) == len(points):
            break

        pbar.update(len(circuit) - so_far)
        so_far = len(circuit)

        d, pair = closest_pair(sorted_points, exclude_pairs)
        exclude_pairs.add(pair)
        if pair[0] not in circuit or pair[1] not in circuit:
            connections[pair[0]].add(pair[1])
            connections[pair[1]].add(pair[0])


print(pair)

print("Part 2:", pair[0].x * pair[1].x)
