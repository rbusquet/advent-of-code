from pathlib import Path

from more_itertools import transpose

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    lines = [line.split() for line in input.read_text().splitlines()]
    total = 0
    for problem in transpose(lines):
        *operands, operator = problem
        if operator == "+":
            total += sum(int(op) for op in operands)
        elif operator == "*":
            result = 1
            for op in operands:
                result *= int(op)
            total += result
        else:
            raise ValueError(f"unknown operator {operator}")
    return total


empty_line = (" ", " ", " ", " ", " ")


def part_2() -> int:
    lines = input.read_text().splitlines()
    total = 0

    partial = 0
    current_operator = "+"
    for problem in transpose(lines):
        match problem:
            case (*digits, "+"):
                operand = int("".join(digits))
                partial += operand
                current_operator = "+"
            case (*digits, "*"):
                operand = int("".join(digits))
                partial += operand
                current_operator = "*"
            case (*digits, " ") if set(problem) != {" "}:
                operand = int("".join(digits))
                if current_operator == "+":
                    partial += operand
                elif current_operator == "*":
                    partial *= operand
                else:
                    raise ValueError(f"unknown operator {current_operator}")
            case _:
                total += partial
                partial = 0
                current_operator = "+"

    return total + partial


print(part_1())
print(part_2())
