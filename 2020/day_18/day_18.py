import pdb
from string import digits
import re
from operator import add, mul

def read_file():
    with open("./input.txt") as f:
        yield from map(lambda c: c.strip(), f.readlines())


operators = {
    '+': add,
    '*': mul
}

def eval_expression(exp: str):
    hold = [1]
    operator = mul
    parens_operator = []
    index = 0
    while index < len(exp):
        num = ''
        while exp[index] in digits:
            num += exp[index]
            index += 1
            if index >= len(exp):
                break
        if num:
            hold[-1] = operator(hold[-1], int(num))
            continue
        ch = exp[index]
        if ch in operators:
            operator = operators[ch]
        elif ch == '(':
            parens_operator.append(operator)
            operator = mul
            hold.append(1)
        elif ch == ')':
            hold, final = hold[:-1], hold[-1]
            parens_operator, this_operator = parens_operator[:-1], parens_operator[-1]
            hold[-1] = this_operator(hold[-1], final)
        index += 1
    return hold[0]

assert eval_expression('2 * 3 + (4 * 5)') == 26
assert eval_expression('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 437
assert eval_expression('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 12240
assert eval_expression('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 13632

total = 0

for line in read_file():
    total += eval_expression(line)
print("--- part 1---")
print(total)

sum_exp = re.compile(r"(\d+) \+ (\d+)")

def eval_part_2(line: str):
    while '(' in line:
        parens = []
        for i in range(len(line)):
            if line[i] == '(':
                parens.append(i + 1)
            if line[i] == ')':
                if len(parens) > 1:
                    parens = parens[:-1]
                else:
                    parens.append(i)
                    break
        i, j = parens
        expression = line[i:j]
        result = eval_part_2(expression)

        line = line.replace(f"({expression})", str(result), 1)

    while match := sum_exp.search(line):
        a, b = match.groups()
        c = int(a) + int(b)
        line = line.replace(match.group(), f"{c}", 1)

    return eval_expression(line)

assert eval_part_2('1 + (2 * 3) + (4 * (5 + 6))') == 51
assert eval_part_2('2 * 3 + (4 * 5)') == 46
assert eval_part_2('5 + (8 * 3 + 9 + 3 * 4 * 3)') == 1445
assert eval_part_2('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))') == 669060
assert eval_part_2('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2') == 23340

total = 0
for line in read_file():
    total += eval_part_2(line)

print("--- part 2 ---")
print(total)
