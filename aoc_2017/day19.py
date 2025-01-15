import enum
from functools import cached_property
from pathlib import Path

input = Path(__file__).parent / "input.txt"


class Direction(enum.Enum):
    RIGHT = (0, 1)
    UP = (-1, 0)
    LEFT = (0, -1)
    DOWN = (1, 0)

    @cached_property
    def turns(self) -> list["Direction"]:
        up_down = [Direction.UP, Direction.DOWN]
        left_right = [Direction.LEFT, Direction.RIGHT]
        if self in up_down:
            return left_right
        return up_down


def part_1() -> tuple[str, int]:
    grid = input.read_text().splitlines()

    y = grid[0].index("|")
    x = 0

    direction = Direction.DOWN
    letters = list[str]()

    steps = 0
    while (tile := grid[x][y]) != " ":
        steps += 1
        if tile.isalpha():
            letters.append(tile)
        if tile == "+":
            # turn
            turns = direction.turns
            for turn in turns:
                maybe_x = x + turn.value[0]
                maybe_y = y + turn.value[1]
                if grid[maybe_x][maybe_y] != " ":
                    x, y = maybe_x, maybe_y
                    direction = turn
                    break
            continue

        x += direction.value[0]
        y += direction.value[1]

    return "".join(letters), steps


print(part_1())
