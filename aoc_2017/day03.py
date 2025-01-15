import enum
from itertools import count, product
from pathlib import Path
from typing import Iterator

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    grid = {(0, 0): 1}
    goal = int(input.read_text())

    x = y = 0
    direction = Direction.RIGHT
    for index in count(start=2):
        x += direction.value[0]
        y += direction.value[1]
        grid[x, y] = index
        next_direction = direction.turn()
        left = (x + next_direction.value[0], y + next_direction.value[1])
        if left not in grid:
            direction = next_direction
        if index == goal:
            break
    return abs(x) + abs(y)


def neighborhood(x: int, y: int) -> Iterator[tuple[int, int]]:
    for diff in product([-1, 0, 1], repeat=2):
        neighbor = (x + diff[0], y + diff[1])
        yield neighbor


class Direction(enum.Enum):
    RIGHT = (0, 1)
    UP = (1, 0)
    LEFT = (0, -1)
    DOWN = (-1, 0)

    def turn(self) -> "Direction":
        return {
            Direction.RIGHT: Direction.UP,
            Direction.UP: Direction.LEFT,
            Direction.LEFT: Direction.DOWN,
            Direction.DOWN: Direction.RIGHT,
        }[self]


def part_2() -> int:
    grid = {(0, 0): 1}
    goal = int(input.read_text())

    x = y = 0
    direction = Direction.RIGHT
    for step in count():
        x += direction.value[0]
        y += direction.value[1]
        value = 0
        for n in neighborhood(x, y):
            if n == (x, y):
                continue
            if n in grid:
                value += grid[n]
        grid[x, y] = value
        next_direction = direction.turn()
        left = (x + next_direction.value[0], y + next_direction.value[1])
        if left not in grid:
            direction = next_direction
        if value >= goal:
            break
    return value


print(part_1())
print(part_2())
