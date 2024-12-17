from pathlib import Path
import re

USE_SAMPLE_INPUT = False
in_path = Path.cwd() / 'input.txt'

if USE_SAMPLE_INPUT:
    input = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
""".strip()
else:
    with in_path.open("r") as inf:
        input = inf.read().strip()

lines = input.splitlines()

reg_a = int(re.match(r"Register A: (\d+)", lines[0]).group(1))
reg_b = int(re.match(r"Register B: (\d+)", lines[1]).group(1))
reg_c = int(re.match(r"Register C: (\d+)", lines[2]).group(1))

assert lines[4].startswith("Program: ")
prog = [int(b) for b in lines[4][len("Program: "):].split(",")]

def eval_prog(prog: list[int], reg_a: int, reg_b: int, reg_c: int, debug=False) -> list[int]:
    ip = 0

    def eval_combo_operand(op):
        match op:
            case 0 | 1 | 2 | 3:
                return op
            case 4:
                return reg_a
            case 5:
                return reg_b
            case 6:
                return reg_c
            case _:
                assert ValueError(f"Invalid combo operand: {op}")

    output = []

    while ip < len(prog):
        if debug:
            print(f"{ip:<2} A={reg_a} B={reg_b} C={reg_c}")

        inst = prog[ip]
        ip += 1
        operand = prog[ip]
        ip += 1

        match inst:
            case 0:
                # adv
                reg_a = reg_a // ( 1<< eval_combo_operand(operand))
            case 1:
                # bxl
                reg_b = reg_b ^ operand
            case 2:
                # bst
                reg_b = eval_combo_operand(operand) & 0x7
            case 3:
                # jnz
                if reg_a != 0:
                    ip = operand
            case 4:
                # bxc
                reg_b = reg_b ^ reg_c
            case 5:
                # out
                output.append(eval_combo_operand(operand) & 0x7)
            case 6:
                # bdv
                reg_b = reg_a // (1 << eval_combo_operand(operand))
            case 7:
                # cdv
                reg_c = reg_a // (1 << eval_combo_operand(operand))
            case _:
                raise ValueError(f"Invalid instruction: {inst}")

    return output

print("Part 1:", f",".join(str(s) for s in eval_prog(prog, reg_a, reg_b, reg_c)))

def disassemble(prog: 'list[int]') -> list[str]:
    out = []
    ip = 0

    def disassemble_combo(op):
        match op:
            case 0 | 1 | 2 | 3:
                return str(op)
            case 4:
                return 'A'
            case 5:
                return 'B'
            case 6:
                return 'C'

    while ip < len(prog):
        inst = prog[ip]
        op = prog[ip+1]

        match inst:
            case 0:
                out.append(f'{ip:<2} A = A // (2**{disassemble_combo(op)})')
            case 1:
                out.append(f'{ip:<2} B = B xor {op}')
            case 2:
                out.append(f'{ip:<2} B = {disassemble_combo(op)} % 8')
            case 3:
                out.append(f'{ip:<2} jnz, {op}')
            case 4:
                out.append(f'{ip:<2} B = B xor C')
            case 5:
                out.append(f'{ip:<2} out, {disassemble_combo(op)}')
            case 6:
                out.append(f'{ip:<2} B = A // (2**{disassemble_combo(op)})')
            case 7:
                out.append(f'{ip:<2} C = A // (2**{disassemble_combo(op)})')

        ip += 2

    return out

def eval_prog_quinine(prog: list[int], reg_a: int, reg_b: int, reg_c: int) -> bool:
    ip = 0

    def eval_combo_operand(op):
        match op:
            case 0 | 1 | 2 | 3:
                return op
            case 4:
                return reg_a
            case 5:
                return reg_b
            case 6:
                return reg_c
            case _:
                assert ValueError(f"Invalid combo operand: {op}")

    output = 0

    while ip < len(prog):
        inst = prog[ip]
        ip += 1
        operand = prog[ip]
        ip += 1

        match inst:
            case 0:
                # adv
                reg_a = reg_a // ( 1<< eval_combo_operand(operand))
            case 1:
                # bxl
                reg_b = reg_b ^ operand
            case 2:
                # bst
                reg_b = eval_combo_operand(operand) & 0x7
            case 3:
                # jnz
                if reg_a != 0:
                    ip = operand
            case 4:
                # bxc
                reg_b = reg_b ^ reg_c
            case 5:
                # out
                val = eval_combo_operand(operand) & 0x7
                if val != prog[output]:
                    return False
                output += 1
            case 6:
                # bdv
                reg_b = reg_a // (1 << eval_combo_operand(operand))
            case 7:
                # cdv
                reg_c = reg_a // (1 << eval_combo_operand(operand))
            case _:
                raise ValueError(f"Invalid instruction: {inst}")
    return output == len(prog)

def solve_prog(prog, sol_so_far):
    if len(prog) == 0:
        return sol_so_far

    for i in range(8):
        A = (sol_so_far*8) + i
        B = A % 8
        B = B ^ 3
        C = A // (2**B)
        B = B ^ C
        B = B ^ 5
        if B % 8 == prog[-1]:
            sol = solve_prog(prog[:-1], A)
            if sol is not None:
                return sol
    return None

sol2 = solve_prog(prog, 0)

# print('\n'.join(disassemble(prog)))
# print(prog)
# print(sol2, eval_prog_quinine(prog, sol2, 0, 0), eval_prog(prog, sol2, 0, 0))

print(f"Part 2: {sol2}")


