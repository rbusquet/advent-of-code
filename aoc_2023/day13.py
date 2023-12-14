from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from itertools import pairwise
from typing import Iterator, TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


def diff_by_one_bit(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    diff = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            diff += 1
            if diff > 1:
                return False
    return True


def find_mirror(rows: list[str]) -> tuple[bool, int]:
    potential_mirror = -1
    for i, pair in enumerate(pairwise(rows)):
        if pair[0] == pair[1]:
            potential_mirror = i
            found_nudge = False

            left = potential_mirror
            right = potential_mirror + 1

            while left >= 0 and right < len(rows):
                if rows[left] != rows[right]:
                    if found_nudge:
                        break
                    found_nudge = diff_by_one_bit(rows[left], rows[right])
                    if not found_nudge:
                        break
                left -= 1
                right += 1
            else:
                if not found_nudge:
                    continue
                return found_nudge, potential_mirror + 1
        elif diff_by_one_bit(pair[0], pair[1]):
            potential_mirror = i

            left = potential_mirror - 1
            right = potential_mirror + 2

            while left >= 0 and right < len(rows):
                if rows[left] != rows[right]:
                    break
                left -= 1
                right += 1
            else:
                return True, potential_mirror + 1

    return False, 0


def part_1(file: TextIO) -> int:
    file.seek(0)

    rows = list[str]()
    total = 0
    maps = list[list[str]]()
    for line in strip_lines(file):
        if not line:
            maps.append(rows)
            rows = []
            continue
        rows.append(line)
    maps.append(rows)

    for pattern in maps:
        columns = ["".join(column) for column in zip(*pattern)]

        found_nudge, top_count = find_mirror(pattern)
        if not found_nudge:
            found_nudge, left_count = find_mirror(columns)
        else:
            left_count = 0
        assert found_nudge

        total += top_count * 100 + left_count

    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
