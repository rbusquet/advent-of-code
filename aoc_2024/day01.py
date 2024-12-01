import argparse
import sys
from collections import Counter
from dataclasses import dataclass
from typing import TextIO

from more_itertools import unzip


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def part_1(file: TextIO) -> int:
    left, right = unzip(a.split() for a in file.readlines())

    sorted_right = sorted(int(x) for x in right)
    sorted_left = sorted(int(x) for x in left)

    total = 0

    for index, r in enumerate(sorted_right):
        l = sorted_left[index]  # noqa: E741
        distance = abs(l - r)
        total += distance
    return total


def part_2(file: TextIO) -> int:
    left, right = unzip(a.split() for a in file.readlines())

    counter = Counter(right)

    total = 0

    for number in left:
        count = counter[number]
        total += int(number) * count

    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    args.file.seek(0)
    print(part_2(args.file))
