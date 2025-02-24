from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from itertools import combinations
from typing import TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return abs(x2 - x1) + abs(y2 - y1)


def solve(file, expansion_rate):
    file.seek(0)
    galaxy_map = []
    for y, line in enumerate(strip_lines(file)):
        for match in re.finditer("#", line):
            galaxy_map.append((match.start(), y))

    xs, ys = zip(*galaxy_map)
    expanded_galaxy_map = []
    dx = dy = 0
    for x, y in galaxy_map:
        dx = (expansion_rate - 1) * len([x for x in range(0, x) if x not in xs])
        dy = (expansion_rate - 1) * len([y for y in range(0, y) if y not in ys])
        expanded_galaxy_map.append((x + dx, y + dy))

    distances = {}
    for pair in combinations(expanded_galaxy_map, 2):
        distances[pair] = manhattan_distance(*pair[0], *pair[1])
    return sum(distances.values())


def part_1(file: TextIO) -> int:
    return solve(file, 2)


def part_2(file: TextIO) -> int:
    return solve(file, 1_000_000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
