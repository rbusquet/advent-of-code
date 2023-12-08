from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from itertools import cycle
from math import lcm
from typing import Iterator, TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


node_regex = re.compile(r"^(?P<name>\w+) = \((?P<left>\w+), (?P<right>\w+)\)$")


def part_1(file: TextIO) -> int:
    file.seek(0)
    lines = strip_lines(file)

    INSTRUCTIONS = ["L", "R"]
    instructions = cycle(INSTRUCTIONS.index(i) for i in next(lines))
    next(lines)

    nodes = dict[str, tuple[str, str]]()
    for line in lines:
        match = node_regex.match(line)
        if not match:
            continue
        name = match.group("name")
        left = match.group("left")
        right = match.group("right")
        nodes[name] = (left, right)

    node = nodes["AAA"]
    count = 0
    for instruction in instructions:
        if node[instruction] == "ZZZ":
            return count + 1
        node = nodes[node[instruction]]
        count += 1
    return -1


def part_2(file: TextIO) -> int:
    file.seek(0)
    lines = strip_lines(file)

    INSTRUCTIONS = ["L", "R"]
    instructions = cycle(INSTRUCTIONS.index(i) for i in next(lines))
    next(lines)

    nodes = dict[str, tuple[str, str]]()
    for line in lines:
        match = node_regex.match(line)
        if not match:
            continue
        name = match.group("name")
        left = match.group("left")
        right = match.group("right")
        nodes[name] = (left, right)

    current_nodes = [key for key in nodes if key.endswith("A")]

    counts = defaultdict(int)

    for a_node in current_nodes:
        node = nodes[a_node]
        count = 0
        for instruction in instructions:
            if node[instruction].endswith("Z"):
                counts[a_node] = count + 1
                break
            node = nodes[node[instruction]]
            count += 1

    return lcm(*counts.values())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
