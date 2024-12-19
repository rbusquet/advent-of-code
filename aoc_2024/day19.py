from functools import cache
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    lines = input.read_text().splitlines()

    patterns = lines[0]
    designs = lines[2:]

    @cache
    def is_valid_design(design: str):
        if design in patterns:
            return True

        for pattern in patterns:
            if design.startswith(pattern):
                return is_valid_design(design[len(pattern) :])
        else:
            return False

    count = 0
    for design in designs:
        count += is_valid_design(design)
    return count


def part_2() -> int:
    lines = input.read_text().splitlines()

    patterns = lines[0]
    designs = lines[2:]

    @cache
    def count_valid_designs(design: str):
        count = design in patterns
        for pattern in patterns:
            if pattern == design:
                continue
            if pattern.startswith(pattern):
                count += count_valid_designs(pattern[len(pattern) :])
        return count

    count = 0
    for design in enumerate(designs):
        count += count_valid_designs(design)
    return count


print(part_1())
print(part_2())
