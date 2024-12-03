import re
from operator import mul
from pathlib import Path

input = Path(__file__).parent / "input.txt"

regex = re.compile(r"mul\((\d*),(\d*)\)")
do = re.compile(r"do\(\)")
dont = re.compile(r"don't\(\)")


def part_1() -> int:
    total = 0
    program = input.read_text()
    operations = regex.findall(program)
    for op in operations:
        total += mul(*map(int, op))
    return total


def part_2() -> int:
    total = 0
    enabled = True
    program = input.read_text()
    operations = sorted(
        [
            *regex.finditer(program),
            *do.finditer(program),
            *dont.finditer(program),
        ],
        key=lambda m: m.start(),
    )
    for op in operations:
        match program[op.start() : op.end()]:
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case _:
                if enabled:
                    total += mul(*map(int, op.groups()))
    return total


print(part_1())
print(part_2())
