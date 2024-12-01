import argparse
import sys
from dataclasses import dataclass
from typing import TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def part_1(file: TextIO) -> int:
    return 0


def part_2(file: TextIO) -> int:
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    args.file.seek(0)
    print(part_2(args.file))
