from pathlib import Path
import re

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
x00: 1
x01: 1
x02: 0
y00: 1
y01: 0
y02: 1

x00 XOR y00 -> z00
x00 AND y00 -> c01
x01 XOR y01 -> i01
x01 AND y01 -> j01
c01 AND i01 -> k01
j01 OR k01 -> c02
c01 XOR i01 -> z01
x02 XOR y02 -> i02
x02 AND y02 -> j02
c02 AND i02 -> k02
j02 OR k02 -> c03
c02 XOR i02 -> z02
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

parser = re.compile(r'(\S+) (OR|AND|XOR) (\S+) -> (\S+)')

in_values, in_rules = input.split('\n\n')

values = {}
for line in in_values.splitlines():
    nstr, vstr = line.split(': ')
    values[nstr] = bool(vstr == '1')

rules = {}
value_ids = set()

swaps = {
    "nnt": "gws",
    "gws": "nnt",
    "z13": "npf",
    "npf": "z13",
    "z19": "cph",
    "cph": "z19",
    "z33": "hgj",
    "hgj": "z33"
}

for rule in in_rules.splitlines():
    match = parser.match(rule)
    assert bool(match)

    operand1, operator, operand2, result = match.groups()

    if result in swaps:
        result = swaps[result]

    operand1, operand2 = sorted((operand1, operand2))

    rules[(operand1, operand2, operator)] = result

    value_ids.update((operand1, operand2))

test_values = {}

max_bit = max(int(v[1:]) for v in value_ids if v[0] in ('x', 'y'))

carry = {}
i = {}
j = {}
k = {}

for bit in range(max_bit+1):
    if bit == 0:
        carry[bit] = rules[(f"x{bit:02}", f"y{bit:02}", "AND")]
        continue

    i[bit] = rules[(f"x{bit:02}", f"y{bit:02}", "XOR")]
    j[bit] = rules[(f"x{bit:02}", f"y{bit:02}", "AND")]

    print(f"{bit:<2} i={i[bit]} j={j[bit]} ", end="")
    assert i[bit][0] not in ('x', 'y', 'z')
    assert j[bit][0] not in ('x', 'y', 'z')


    op1, op2 = sorted((i[bit], carry[bit-1]))


    assert rules[(op1, op2, "XOR")] == f"z{bit:02}"
    k[bit] = rules[(op1, op2, "AND")]

    print(f"k={k[bit]} ", end="")
    assert k[bit][0] not in ('x', 'y', 'z')


    op1, op2 = sorted((k[bit], j[bit]))
    carry[bit] = rules[(op1, op2, "OR")]
    print(f"c={carry[bit]}")


print(f"Part 2:", ','.join(sorted(swaps.keys())))
