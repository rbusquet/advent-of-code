import argparse
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator, TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


def part_1(file: TextIO) -> int:
    file.seek(0)

    movable_rocks_in_row = defaultdict(int)
    border_by_col = defaultdict(int)

    rows = 0
    for i, row in enumerate(strip_lines(file)):
        rows += 1
        for j, char in enumerate(row):
            if char == "O":
                # moveable rock
                border = border_by_col[j]
                movable_rocks_in_row[border] += 1
                border_by_col[j] += 1
            elif char == "#":
                # unmovable rock
                border_by_col[j] = i + 1

    return sum((rows - row) * count for row, count in movable_rocks_in_row.items())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
