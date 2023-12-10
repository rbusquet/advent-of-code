from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Iterator, TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


N, S, E, W = (
    (0, -1),
    (0, +1),
    (+1, 0),
    (-1, 0),
)


Position = tuple[int, int]


class Walker:
    PIPES = {
        "|": {N: N, S: S},
        "L": {S: E, W: N},
        "F": {N: E, W: S},
        "7": {E: S, N: W},
        "J": {E: N, S: W},
        "-": {E: E, W: W},
    }

    def __init__(
        self, initial_position: Position, initial_direction: Position, pipes: list[str]
    ) -> None:
        self.loop = [initial_position]
        self.initial_direction = initial_direction
        self.pipes = pipes

    @property
    def position(self) -> Position:
        return self.loop[-1]

    def walk(self, direction) -> Position:
        x, y = self.position[0] + direction[0], self.position[1] + direction[1]
        next_pipe = self.pipes[y][x]

        if next_pipe == "S":
            self.loop.append((x, y))
            return self.initial_direction

        if next_pipe not in self.PIPES:
            raise Exception()
        if direction not in self.PIPES[next_pipe]:
            raise Exception()
        self.loop.append((x, y))
        return self.PIPES[next_pipe][direction]


def part_1(file: TextIO) -> None:
    file.seek(0)

    pipes = []

    initial = (0, 0)
    for y, row in enumerate(strip_lines(file)):
        pipes.append(row)
        if "S" in row:
            initial = (row.index("S"), y)

    for direction in (N, S, E, W):
        walker = Walker(initial, direction, pipes)
        try:
            last_direction = direction
            direction = walker.walk(last_direction)
            next_x, next_y = walker.position
        except Exception:
            continue
        steps = 1

        while pipes[next_y][next_x] != "S":
            try:
                last_direction = direction
                direction = walker.walk(last_direction)
                steps += 1
                next_x, next_y = walker.position
            except Exception:
                break
        else:
            print(steps // 2)
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    part_1(args.file)
