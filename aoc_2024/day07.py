from functools import reduce
from itertools import product
from math import floor, log
from operator import add, mul
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def parse(equation: str) -> tuple[int, tuple[int, ...]]:
    test, operands = equation.split(":")

    return (int(test), tuple(map(int, operands.split())))


def part_1() -> int:
    total = 0
    operators = ["*", "+"]

    for line in input.read_text().splitlines():
        test, operands = parse(line)

        operations = product(operators, repeat=len(operands) - 1)
        for operation in operations:
            it = iter(operation)

            def func(a: int, b: int) -> int:
                op = next(it)
                return eval(f"{a}{op}{b}")

            result = reduce(func, operands)
            if result == test:
                total += result
                break
    return total


def concat(a: int, b: int) -> int:
    digits_b = floor(log(b, 10) + 1)
    return int(a * (10**digits_b) + b)


def part_2() -> int:
    total = 0
    operators = ["*", "+", "||"]

    o_to_f = {"*": mul, "+": add, "||": concat}

    for line in input.read_text().splitlines():
        test, operands = parse(line)

        operations = product(operators, repeat=len(operands) - 1)
        for operation in operations:
            it = iter(operation)

            def func(a: int, b: int) -> int:
                op = next(it)
                result = o_to_f[op](a, b)
                if result > test:
                    raise Exception("wont work")
                return result

            try:
                result = reduce(func, operands)
            except Exception:
                continue
            if result == test:
                total += result
                break
    return total


print(part_1())
print(part_2())
