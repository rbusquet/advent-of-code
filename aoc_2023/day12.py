from __future__ import annotations

import argparse
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from functools import cache
from typing import TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


@cache
def possible_arrangements(row, *checksum):
    # print("miss")
    if not checksum:
        # do not allow new #
        if "#" not in row:
            return 1
        return 0

    if not row:
        # exhausted the row
        return 0

    def damaged():
        consider = row[: checksum[0]].replace("?", "#")
        remaining = row[checksum[0] :]
        if consider != "#" * checksum[0]:
            # couldn't fit a consecutive count, break
            return 0

        if not remaining:
            # make sure we're dealing with the last group
            return len(checksum) == 1
        if remaining[0] == "#":
            # would cause this group to be larger than the checksum
            return 0

        # print(f"calling with springs={remaining[1:]} checksum={checksum[1:]}")
        return possible_arrangements(remaining[1:], *checksum[1:])

    def operational():
        # possible_arrangements('.###...', [3]) == possible_arrangements('###...', [3])
        # print(f"calling with springs={row[1:]} checksum={checksum}")
        return possible_arrangements(row[1:], *checksum)

    arrangements = 0

    match row[0]:
        case ".":
            arrangements = operational()
        case "#":
            arrangements = damaged()
        case "?":
            arrangements = operational() + damaged()

    return arrangements


def part_1(file: TextIO) -> int:
    file.seek(0)

    total = 0

    for line in strip_lines(file):
        springs, checksum_str = line.split(" ")
        checksum = map(int, checksum_str.split(","))
        # print(f"calling with {springs=} {checksum=}")
        total += possible_arrangements(springs, *checksum)

    return total


def part_2(file: TextIO) -> int:
    file.seek(0)

    total = 0

    for line in strip_lines(file):
        springs, checksum_str = line.split(" ")
        checksum = map(int, checksum_str.split(","))
        # print(f"calling with {springs=} {checksum=}")

        unfolded_springs = "?".join([springs] * 5)
        unfolded_checksum = list(checksum) * 5
        total += possible_arrangements(unfolded_springs, *unfolded_checksum)

    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
