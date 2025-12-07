from collections.abc import Iterator
from functools import cache
from pathlib import Path

input = Path(__file__).parent / "input.txt"


@cache
def beam(
    world: tuple[tuple[str, ...], ...], x: int, y: int
) -> Iterator[tuple[int, int]]:
    height = len(world)

    while x < height:
        if world[x][y] == "^":
            yield (x, y)
            yield from beam(world, x, y - 1)
            yield from beam(world, x, y + 1)
            break
        x += 1


def part_1() -> int:
    world = tuple(tuple(line) for line in input.read_text().splitlines())

    start = (0, world[0].index("S"))

    return len(set(beam(world, *start)))


@cache
def quantum_beam(world: tuple[tuple[str, ...]], x: int, y: int) -> int:
    height = len(world)

    while x < height:
        if world[x][y] == "^":
            return quantum_beam(world, x, y - 1) + quantum_beam(world, x, y + 1)
        x += 1
    return 1


def part_2() -> int:
    world = tuple(tuple(line) for line in input.read_text().splitlines())

    start = (0, world[0].index("S"))

    return quantum_beam(world, *start)


print(part_1())
print(part_2())
