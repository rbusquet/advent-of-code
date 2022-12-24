from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import TextIO

from more_itertools import pairwise

Point = tuple[int, int]


def main(args: Arguments) -> None:
    solids = defaultdict[Point, bool](bool)
    max_y = 0
    for line in args.infile:
        iterator = pairwise(line.strip().split(" -> "))
        for from_rock, to_rock in iterator:
            from_x, from_y = map(int, from_rock.split(","))
            to_x, to_y = map(int, to_rock.split(","))

            from_x, to_x = sorted([from_x, to_x])
            from_y, to_y = sorted([from_y, to_y])
            for i in range(from_x, to_x + 1):
                for j in range(from_y, to_y + 1):
                    solids[i, j] = True
            max_y = max(max_y, int(from_y), int(to_y))

    x, y = 500, 0
    total_sand = 0
    sand = list[Point]()
    while y <= max_y:
        next_x, next_y = x, y + 1
        if not solids[next_x, next_y]:
            # nothing below, fall one
            y = next_y
            continue

        if not solids[next_x - 1, next_y]:
            x = next_x - 1
            y = next_y
            continue

        if not solids[next_x + 1, next_y]:
            x = next_x + 1
            y = next_y
            continue

        # can't move
        solids[x, y] = True
        sand.append((x, y))
        total_sand += 1
        # reset
        x, y = 500, 0

    print(total_sand)

    def is_solid(x, y) -> bool:
        if y == max_y + 2:
            return True
        return solids[x, y]

    while solids[500, 0] is not True:
        next_x, next_y = x, y + 1
        if not is_solid(next_x, next_y):
            # nothing below, fall one
            y = next_y
            continue

        if not is_solid(next_x - 1, next_y):
            x = next_x - 1
            y = next_y
            continue

        if not is_solid(next_x + 1, next_y):
            x = next_x + 1
            y = next_y
            continue

        # can't move
        solids[x, y] = True
        total_sand += 1
        sand.append((x, y))
        # reset
        x, y = 500, 0

    # min_x = min(s[0] for s in solids)
    # min_y = min(s[1] for s in solids)
    # max_x = max(s[0] for s in solids)
    # max_y = max(s[1] for s in solids)

    # for j in range(min_y, max_y + 1):
    #     for i in range(min_x, max_x + 1):
    #         if (i, j) in sand:
    #             print("_", end="")
    #             continue
    #         print([" ", "█"][solids[i, j]], end="")
    #     print()
    print(total_sand)


@dataclass
class Arguments:
    infile: TextIO = sys.stdin


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))

    args = Arguments()
    parser.parse_args(namespace=args)
    main(args)
