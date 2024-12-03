from pathlib import Path

from more_itertools import pairwise


def sign(n: int) -> int:
    return (n > 0) - (n < 0)


def validate_v1(levels: list[int]) -> int:
    slope = None

    for a, b in pairwise(levels):
        if a == b:
            return 0

        if slope is None:
            slope = sign(b - a)

        if slope == 0:
            return 0

        if sign(b - a) != slope:
            return 0

        if abs(b - a) > 3:
            return 0

    return 1


def validate_v2(levels: list[int], max_violations=0) -> int:
    violations = {}
    slope = None

    for i, (a, b) in enumerate(pairwise(levels)):
        if a == b:
            violations[i] = (a, b)
            continue

        if slope is None:
            slope = sign(b - a)

        if slope == 0:
            violations[i] = (a, b)
            continue

        if sign(b - a) != slope:
            violations[i] = (a, b)
            continue

        if abs(b - a) > 3:
            violations[i] = (a, b)

    if not violations:
        return 1

    if len(violations) and max_violations == 0:
        return 0

    # try removing the first item
    if v := validate_v2(levels[1:], max_violations - 1):
        return v

    for i in violations:
        if v := validate_v2(levels[:i] + levels[i + 1 :], max_violations - 1):
            return v
        if v := validate_v2(levels[: i + 1] + levels[i + 2 :], max_violations - 1):
            return v
    return 0


input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    with input.open() as file:
        valid = 0
        for line in file:
            levels = list(map(int, line.split()))
            if v := validate_v1(levels):
                valid += v
            # print(line, v)
        return valid


def part_2() -> int:
    with input.open() as file:
        valid = 0
        for line in file:
            levels = list(map(int, line.split()))
            valid += validate_v2(levels, 1)
        return valid


print(part_1())
print(part_2())
