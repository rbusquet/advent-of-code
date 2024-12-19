from functools import cache
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    lines = input.read_text().splitlines()

    patterns = lines[0].split(", ")
    designs = lines[2:]

    @cache
    def count_valid_designs(design: str):
        if design == "":
            return True
        for pattern in patterns:
            if design.startswith(pattern):
                if count_valid_designs(design[len(pattern) :]):
                    return True
        return False

    count = 0
    for design in designs:
        count += count_valid_designs(design)
    return count


def part_2() -> int:
    lines = input.read_text().splitlines()

    patterns = lines[0].split(", ")
    designs = lines[2:]

    @cache
    def count_valid_designs(design: str):
        if design == "":
            return 1
        count = 0
        for pattern in patterns:
            if design.startswith(pattern):
                count += count_valid_designs(design[len(pattern) :])
        return count

    count = 0
    for design in designs:
        count += count_valid_designs(design)
    return count


print(part_1())
print(part_2())
