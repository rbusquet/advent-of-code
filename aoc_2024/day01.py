from collections import Counter
from pathlib import Path

from more_itertools import unzip

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    with input.open() as file:
        left, right = unzip(a.split() for a in file.readlines())

    sorted_right = sorted(int(x) for x in right)
    sorted_left = sorted(int(x) for x in left)

    total = 0

    for index, r in enumerate(sorted_right):
        l = sorted_left[index]  # noqa: E741
        distance = abs(l - r)
        total += distance
    return total


def part_2() -> int:
    with input.open() as file:
        left, right = unzip(a.split() for a in file.readlines())

    counter = Counter(right)

    total = 0

    for number in left:
        count = counter[number]
        total += int(number) * count

    return total


print(part_1())
print(part_2())
