from pathlib import Path
import re


USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
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

print(values)

unresolved_rules = set()

for rule in in_rules.splitlines():
    match = parser.match(rule)
    assert bool(match)

    operand1, operator, operand2, result = match.groups()

    rule = (operator, operand1, operand2, result)
    unresolved_rules.add(rule)

while len(unresolved_rules) > 0:
    crules = list(unresolved_rules)
    for crule in crules:
        operator, operand1, operand2, result = crule
        if operand1 in values and operand2 in values:
            unresolved_rules.remove(crule)
            match operator:
                case "AND":
                    values[result] = values[operand1] and values[operand2]
                case "OR":
                    values[result] = values[operand1] or values[operand2]
                case "XOR":
                    values[result] = values[operand1] != values[operand2]
                case _:
                    raise ValueError(f"Unknown operantor {operator}")


for k in sorted(values.keys()):
    print(f'{k:<3}: {values[k]}')

keys = sorted([k for k in values.keys() if k[0] == 'z'], key=lambda x: int(x[1:]))

value = ''.join(['1' if values[k] else '0' for k in keys])[::-1]
print(value)
print(f'Part 1: {int(value, 2)}')
