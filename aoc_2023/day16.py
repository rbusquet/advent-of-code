import argparse
import sys
from dataclasses import dataclass
from typing import Iterator, NamedTuple, TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


class Direction(NamedTuple):
    x: int
    y: int


UP = Direction(0, -1)
RIGHT = Direction(1, 0)
DOWN = Direction(0, 1)
LEFT = Direction(-1, 0)

DIRECTION_REPR = {UP: "^", RIGHT: ">", DOWN: "v", LEFT: "<"}


REFLECTIONS = {
    "\\": {UP: LEFT, LEFT: UP, DOWN: RIGHT, RIGHT: DOWN},
    "/": {UP: RIGHT, LEFT: DOWN, DOWN: LEFT, RIGHT: UP},
}

SPLITS = {
    "-": {UP: [LEFT, RIGHT], LEFT: [LEFT], DOWN: [LEFT, RIGHT], RIGHT: [RIGHT]},
    "|": {UP: [UP], LEFT: [UP, DOWN], DOWN: [DOWN], RIGHT: [UP, DOWN]},
}


@dataclass(frozen=True, slots=True)
class LitTile:
    x: int
    y: int
    direction: Direction

    def beam(self, tile: str, size: int) -> Iterator["LitTile"]:
        if tile in ".":
            x, y = self.x + self.direction.x, self.y + self.direction.y
            if 0 <= x < size and 0 <= y < size:
                yield LitTile(x, y, self.direction)
        if tile in "\\/":
            direction = REFLECTIONS[tile][self.direction]
            x, y = self.x + direction.x, self.y + direction.y
            if 0 <= x < size and 0 <= y < size:
                yield LitTile(x, y, direction)

        elif tile in "-|":
            for direction in SPLITS[tile][self.direction]:
                x, y = self.x + direction.x, self.y + direction.y
                if 0 <= x < size and 0 <= y < size:
                    yield LitTile(x, y, direction)


def energize(initial: LitTile, obstacles: tuple[str, ...], size: int) -> int:
    tiles = [initial]
    visited_coords = dict[tuple[int, int], LitTile]()
    visited_tiles = set[LitTile]()
    size = len(obstacles)

    while tiles:
        tile = tiles.pop()
        visited_coords[tile.x, tile.y] = tile
        visited_tiles.add(tile)

        obstacle = obstacles[tile.y][tile.x]
        for next_tile in tile.beam(obstacle, size):
            if next_tile not in visited_tiles:
                tiles.append(next_tile)

    return len(visited_coords)


def part_1(file: TextIO) -> int:
    file.seek(0)
    obstacles = tuple(strip_lines(file))

    return energize(LitTile(0, 0, RIGHT), obstacles, len(obstacles))


def part_2(file: TextIO) -> int:
    file.seek(0)
    obstacles = tuple(strip_lines(file))

    max_energy = 0
    size = len(obstacles)

    max_energy = 0
    for i in range(size):
        max_energy = max(max_energy, energize(LitTile(i, 0, DOWN), obstacles, size))
        # print(f"x={i} y=0 {max_energy=}")
        max_energy = max(
            max_energy, energize(LitTile(i, size - 1, UP), obstacles, size)
        )
        # print(f"x={i} y={size-1} {max_energy=}")
        max_energy = max(max_energy, energize(LitTile(0, i, RIGHT), obstacles, size))
        # print(f"x=0 y={i} {max_energy=}")
        max_energy = max(
            max_energy, energize(LitTile(size - 1, i, LEFT), obstacles, size)
        )
        # print(f"x={size-1} y={i} {max_energy=}")
    return max_energy


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
