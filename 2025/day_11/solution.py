from pathlib import Path
from collections import defaultdict

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
""".strip()

else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

edges = {}
for line in input.split('\n'):
    source, dests = line.split(':')
    dests = dests.split()
    edges[source] = dests

def dfs_search(curr: 'str', visited:'set[str]'):
    if curr == "out":
        return 1

    count = 0
    for next in edges[curr]:
        if (curr, next) in visited:
            continue
        count += dfs_search(next, visited.union(((curr, next), )))
    return count

print("Part 1:", dfs_search("you", set()))

if USE_SAMPLE_INPUT:
    input = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
""".strip()


edges2 = defaultdict(list)

for line in input.split('\n'):
    source, dests = line.split(':')
    for dest in dests.split():
        edges2[dest].append(source)

def topological_sort(edges: 'dict[str, list[str]]', start: 'str'):
    incoming_edges = defaultdict(set)
    for n in edges.keys():
        for e in edges[n]:
            incoming_edges[e].add(n)

    s = [start]
    l = []
    while len(s) > 0:
        n = s.pop()
        l.append(n)
        for m in edges[n]:
            incoming_edges[m].remove(n)
            if len(incoming_edges[m]) == 0:
                s.append(m)

    return l

def calc_counts(edges: 'dict[str, list[str]]', ordered: 'list[str]', to_node: 'str'):
    counts = {to_node: 1}
    start = ordered.index(to_node)

    for curr in ordered[start:]:
        curr_count = counts.get(curr, 0)
        for node in edges[curr]:
            counts[node] = counts.get(node, 0) + curr_count

    return counts

# edges3 = {
#     "g": ["d", "e", "f"],
#     "e": ["d"],
#     "f": ["d"],
#     "d": ["b", "a", "c"],
#     "b": ["a"],
#     "c": ["a"],
#     "a": []
# }

# ordered = topological_sort(edges3, "g")
# print(calc_counts(edges3, ordered, "e"))
# exit()
# print(calc_counts("g"))
# exit()

ordered = topological_sort(edges2, "out")

out_counts = calc_counts(edges2, ordered, "out")
dac_counts = calc_counts(edges2, ordered, "dac")
fft_counts = calc_counts(edges2, ordered, "fft")

#print("Part 1:", calc_counts(edges, topological_sort(edges, "out"), "out").get("you"))

# print(out_counts.get("dac", 0), dac_counts.get("fft", 0), fft_counts.get("svr", 0))
# print(out_counts.get("fft", 0), fft_counts.get("dac", 0), dac_counts.get("svr", 0))

part2 = out_counts.get("dac", 0) * dac_counts.get("fft", 0) * fft_counts.get("svr", 0) \
    + out_counts.get("fft", 0) * fft_counts.get("dac", 0) * dac_counts.get("svr", 0)

print("Part 2:", part2)
