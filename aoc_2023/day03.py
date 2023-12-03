import argparse
import re
import sys
from dataclasses import dataclass
from typing import TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


@dataclass
class Part:
    number: int
    x: int
    y: int
    length: int = 1


@dataclass
class Symbol:
    symbol: str
    x: int
    y: int

    def adjacent_to(self, other: "Part") -> bool:
        """Check if the symbol is adjacent to this part
        in all directions."""
        y_adjacent = other.y - 1 <= self.y <= other.y + 1
        x_adjacent = other.x - 1 <= self.x <= other.x + other.length
        return y_adjacent and x_adjacent


NUMBER_REGEX = re.compile(r"(\d+)")
SYMBOLS_REGEX = re.compile(r"([^\d\.])")


def process_file(file: TextIO) -> tuple[list[Part], list[Symbol]]:
    file.seek(0)
    parts = []
    symbols = []
    for y, line in enumerate(line.strip() for line in file):
        for match in NUMBER_REGEX.finditer(line):
            number = int(match.group())
            x = match.start()
            parts.append(Part(number, x, y, len(match.group())))
        for match in SYMBOLS_REGEX.finditer(line):
            x = match.start()
            symbols.append(Symbol(match.group(), x, y))

    return parts, symbols


def part_1(file: TextIO) -> int:
    parts, symbols = process_file(file)
    total = 0
    for symbol in symbols:
        for part in parts:
            if symbol.adjacent_to(part):
                total += part.number
    return total


def part_2(file: TextIO) -> int:
    parts, symbols = process_file(file)
    total = 0
    for symbol in symbols:
        if symbol.symbol != "*":
            continue
        adjacent_parts = [part for part in parts if symbol.adjacent_to(part)]
        if len(adjacent_parts) == 2:
            p1, p2 = adjacent_parts
            total += p1.number * p2.number
    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
