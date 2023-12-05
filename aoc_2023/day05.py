import argparse
import sys
from dataclasses import dataclass
from typing import TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def part_1(file: TextIO) -> int:
    file.seek(0)
    seeds = [int(seed) for seed in next(file).strip().split(":")[1].strip().split()]
    mapped = set[int]()

    for line in file:
        if not line.strip():
            mapped = set[int]()
            continue
        if "map" in line:
            continue
        destination, source, length = map(int, line.strip().split())

        for i, seed in enumerate(seeds):
            if i in mapped:
                continue
            if seed >= source and seed <= source + length:
                seeds[i] = destination + seed - source
                mapped.add(i)
    return min(seeds)


def part_2(file: TextIO) -> int:
    return -1


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
