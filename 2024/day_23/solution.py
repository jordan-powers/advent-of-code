from pathlib import Path

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

edges = {}

for line in input.splitlines():
    n1, n2 = line.split('-')

    edges.setdefault(n1, set()).add(n2)
    edges.setdefault(n2, set()).add(n1)

def dfs_search(depth: int, curr: str, prev: list[str], search: str, groups: 'set[tuple[str, str, str]]'):
    if depth == 0:
        if curr == search:
            assert len(prev) == 3
            group = tuple(sorted(prev))
            groups.add(group)
        return

    for node in edges[curr]:
        if node in prev and node != search:
            continue

        dfs_search(depth-1, node, prev + [curr], search, groups)

groups = set()
for node in edges.keys():
    dfs_search(3, node, [], node, groups)

groups = sorted(groups, key=lambda x: x[0])

sol1 = 0
for group in groups:
    if any(k[0] == 't' for k in group):
        print(group)
        sol1 += 1
print(f'Part 1: {sol1}')

def find_fully_connected(curr, vertex_set: list, visited_set: set, graph_set: set):
    vertex_set_2 = [v for v in vertex_set if v in edges[curr] or v == curr]
    if len(vertex_set_2) == 0:
        return
    visited_set.add(curr)
    if all(v in visited_set for v in vertex_set_2):
        graph_set.add(tuple(sorted(vertex_set_2)))
    for v in vertex_set_2:
        if v not in visited_set:
            find_fully_connected(v, vertex_set_2, visited_set, graph_set)

graph_set = set()
for v in edges.keys():
    vertex_set = sorted(edges[v].union((v,)))
    find_fully_connected(v, vertex_set, set(), graph_set)
#print(graph_set)

max_graph = max(graph_set, key=len)

sol2 = ','.join(sorted(max_graph))
print(f'Part 2: {sol2}')
