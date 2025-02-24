from __future__ import annotations

import argparse
import sys
from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass
from typing import TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


def part_1(file: TextIO) -> int:
    file.seek(0)

    total = 0

    for line in strip_lines(file):
        numbers = deque(map(int, line.split()))

        stack = [numbers]

        while set(stack[-1]) != {0}:
            numbers = stack[-1]
            diffs = deque(
                [numbers[i + 1] - numbers[i] for i in range(len(numbers) - 1)]
            )
            stack.append(diffs)
        stack[-1].append(0)

        for i in range(len(stack) - 2, -1, -1):
            last = stack[i][-1]
            result = stack[i + 1][-1]
            # new - last = result => new = result + last
            stack[i].append(last + result)
        total += stack[0].pop()
    return total


def part_2(file: TextIO) -> int:
    file.seek(0)

    total = 0

    for line in strip_lines(file):
        numbers = deque(map(int, line.split()))

        stack = [numbers]

        while set(stack[-1]) != {0}:
            numbers = stack[-1]
            diffs = deque(
                [numbers[i + 1] - numbers[i] for i in range(len(numbers) - 1)]
            )
            stack.append(diffs)

        for i in range(len(stack) - 2, -1, -1):
            first = stack[i][0]
            result = stack[i + 1][0]
            # first - new = result => new = first - result
            stack[i].appendleft(first - result)
        total += stack[0].popleft()
    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
