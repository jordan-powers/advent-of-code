from pathlib import Path
from collections import defaultdict
import math

USE_SAMPLE_INPUT = False

in_path = Path.cwd() / 'input.txt'

sample_input = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
""".strip()

if USE_SAMPLE_INPUT:
    input = sample_input
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

lines = input.split('\n')

class Range:
    def __init__(self, start: int, len: int):
        self.start = start
        self.len = len

    def __contains__(self, item) -> bool:
        if not isinstance(item, int):
            return False

        return item >= self.start and item < self.start + self.len

    def __str__(self) -> str:
        return f'({self.start}..{self.start + self.len})'

class RangeMap:
    def __init__(self, start: int, dest: int, len: int):
        self.in_range = Range(start, len)
        self.offset = dest - start

    def __contains__(self, item) -> bool:
        return item in self.in_range

    def __getitem__(self, item: int) -> int:
        if not isinstance(item, int):
            raise KeyError('RangeMap can only map ints')

        if not item in self:
            raise ValueError(f'This RangeMap does not contain {item}')

        return item + self.offset

    def __str__(self) -> str:
        op = '+' if self.offset >= 0 else ''
        return str(self.in_range) + f' {op}{self.offset}'

class Map:
    def __init__(self, src: str, dst: str, ranges: 'list[RangeMap]'):
        self.src = src
        self.dst = dst
        self.ranges = ranges

    @staticmethod
    def from_str(map_str: str) -> 'Map':
        lines = map_str.strip().split('\n')
        title = lines[0]
        range_strs = lines[1:]

        src, to, dst = title[:-5].split('-')
        assert to == 'to'

        ranges: 'list[RangeMap]' = []
        for range_str in range_strs:
            dest, start, len = range_str.split()
            range = RangeMap(int(start), int(dest), int(len))
            ranges.append(range)

        return Map(src, dst, ranges)

    def __getitem__(self, item: int) -> int:
        if not isinstance(item, int):
            raise KeyError('Map can only map ints')

        for range in self.ranges:
            if item in range:
                return range[item]

        return item

    def __str__(self) -> str:
        return f'{self.src}-to-{self.dst} map:' + ''.join(['\n    ' + str(range) for range in self.ranges])


map_strs = input.split('\n\n')[1:]
maps: 'list[Map]' = []
for map_str in map_strs:
    map = Map.from_str(map_str)
    maps.append(map)

maps_by_src: 'dict[str, list[Map]]' = defaultdict(list)
for map in maps:
    maps_by_src[map.src].append(map)


seeds = [int(s) for s in lines[0][7:].split()]

def traverse_map(maps_by_src: 'dict[str, Map]', start_type: str, start_value: int, dst_type: str) -> int:
    stack = [(start_type, start_value)]

    while len(stack) > 0:
        curr = stack.pop()
        if curr[0] == dst_type:
            return curr[1]
        maps = maps_by_src[curr[0]]
        for map in maps:
            stack.append((map.dst, map[curr[1]]))

    raise ValueError(f"Could not find path to '{dst_type}' from '{start_type}'")

min_loc = math.inf

for seed in seeds:
    location = traverse_map(maps_by_src, 'seed', seed, 'location')
    print(f'{seed} -> {location}')
    min_loc = min(min_loc, location)

print(f'Part 1: {min_loc}')

min_loc = math.inf

for j in range(0, len(seeds), 2):
    start = seeds[j]
    length = seeds[j+1]

    for k in range(start, start+length):
        location = traverse_map(maps_by_src, 'seed', seed, 'location')
        min_loc = min(min_loc, location)

print(f'Part 2: {min_loc}')
