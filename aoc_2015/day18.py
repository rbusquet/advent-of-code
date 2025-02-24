from collections import defaultdict
from collections.abc import Iterator
from itertools import product
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def neighborhood(x: int, y: int) -> Iterator[tuple[int, int]]:
    for diff in product([-1, 0, 1], repeat=2):
        neighbor = (x + diff[0], y + diff[1])
        yield neighbor


def full_cycle(initial: str, count: int = 100, part_2: bool = False) -> int:
    space = set[tuple[int, int]]()
    size = 0
    for x, line in enumerate(initial.splitlines()):
        size = len(line)
        for y, state in enumerate(line):
            cube = (x, y)
            if state == "#":
                space.add(cube)

    corners = (
        [(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)] if part_2 else []
    )

    for _ in range(count):
        space.update(corners)
        cube_to_active_count = defaultdict[tuple[int, int], int](int)

        for x, y in space:
            for i, j in neighborhood(x, y):
                if 0 <= i < size and 0 <= j < size:
                    cube_to_active_count[i, j] += (i, j) != (x, y)
        for n, count in cube_to_active_count.items():
            if n in space:
                if count in [2, 3]:
                    pass
                else:
                    space.remove(n)
            elif count == 3:
                space.add(n)

    space.update(corners)
    return len(space)


def part_1() -> int:
    return full_cycle(input.read_text())


def part_2() -> int:
    return full_cycle(input.read_text(), part_2=True)


print(part_1())
print(part_2())
