from itertools import combinations
from pathlib import Path
from typing import NamedTuple

input = Path(__file__).parent / "input.txt"


class Position(NamedTuple):
    x: int
    y: int


def distance(a: Position, b: Position) -> int:
    """manhattan distance between two 2D positions"""
    return abs(a.x - b.x) + abs(a.y - b.y)


def part_1() -> int:
    world = [
        Position(*map(int, line.split(","))) for line in input.read_text().splitlines()
    ]

    # pprint([(a, b, distance(a, b)) for a, b in combinations(world, 2)])
    max_distance = max(combinations(world, 2), key=lambda pair: distance(*pair))
    return (abs(max_distance[0].x - max_distance[1].x) + 1) * (
        abs(max_distance[0].y - max_distance[1].y) + 1
    )


def part_2() -> int:
    return 0


print(part_1())
print(part_2())
