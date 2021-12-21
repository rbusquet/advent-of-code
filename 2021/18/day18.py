from __future__ import annotations

import functools
import math
import re
from itertools import combinations
from pathlib import Path

from more_itertools import last

re_single_number = re.compile(r"\d+")
re_regular_number = re.compile(r"\[(\d+),(\d+)\]")


def add(a: str, b: str) -> str:
    return reduce(f"[{a},{b}]")


def _count_levels(substr: str) -> int:
    brackets = {"[": 1, "]": -1}
    level = 0
    for char in substr:
        level += brackets.get(char, 0)
    return level


def replace_first_number(substr: str, number: int) -> str:
    if found := re_single_number.search(substr):
        value = int(found.group())
        substr = re_single_number.sub(f"{value + number}", substr, 1)
    return substr


def replace_last_number(substr: str, number: int) -> str:
    if found := last(re_single_number.finditer(substr), None):
        value = int(found.group())
        left = substr[0 : found.start()]
        substr = re_single_number.sub(f"{value + number}", substr[found.start() :], 1)
        substr = f"{left}{substr}"
    return substr


def explode(a: str) -> str:
    for found in re_regular_number.finditer(a):
        left = a[0 : found.start()]
        right = a[found.end() :]
        levels = _count_levels(left)
        if levels >= 4:
            x, y = map(int, found.groups())

            right = replace_first_number(right, y)
            left = replace_last_number(left, x)
            return f"{left}0{right}"
    return a


def split_number(a: str) -> str:
    for match in re_single_number.finditer(a):
        value = int(match.group())
        if value >= 10:
            left = a[0 : match.start()]
            right = a[match.end() :]
            x, y = math.floor(value / 2), math.ceil(value / 2)
            return f"{left}[{int(x)},{int(y)}]{right}"
    return a


def reduce(a: str) -> str:
    while True:
        exploded = explode(a)
        if a != exploded:
            a = exploded
            continue
        split = split_number(a)
        if a != split:
            a = split
            continue
        break
    return a


def _magnitude(x: int, y: int) -> int:
    return 3 * x + 2 * y


def magnitude(a: str) -> int:
    while True:
        if full_match := re_regular_number.fullmatch(a):
            x, y = map(int, full_match.groups())
            return _magnitude(x, y)
        for found in re_regular_number.finditer(a):
            x, y = map(int, found.groups())
            left = a[0 : found.start()]
            right = a[found.end() :]
            a = f"{left}{_magnitude(x, y)}{right}"
            break


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        numbers = map(lambda a: a.strip(), file.readlines())
    result = functools.reduce(add, numbers)
    return magnitude(result)


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        numbers = map(lambda a: a.strip(), file.readlines())
    magnitudes = []

    for x, y in combinations(numbers, 2):
        magnitudes.append(magnitude(add(x, y)))
        magnitudes.append(magnitude(add(y, x)))
    return max(magnitudes)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
