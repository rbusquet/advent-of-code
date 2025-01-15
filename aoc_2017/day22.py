import enum
from pathlib import Path

input = Path(__file__).parent / "input.txt"


class DirectionEnum(enum.Enum):
    N = (-1, 0)
    S = (1, 0)
    E = (0, 1)
    W = (0, -1)


class Direction:
    def __init__(self, initial: DirectionEnum) -> None:
        self.d = initial

    OPPOSITES = {
        DirectionEnum.N: DirectionEnum.S,
        DirectionEnum.E: DirectionEnum.W,
        DirectionEnum.S: DirectionEnum.N,
        DirectionEnum.W: DirectionEnum.E,
    }

    RIGHT_TURNS = {
        DirectionEnum.N: DirectionEnum.E,
        DirectionEnum.E: DirectionEnum.S,
        DirectionEnum.S: DirectionEnum.W,
        DirectionEnum.W: DirectionEnum.N,
    }

    LEFT_TURNS = {
        DirectionEnum.N: DirectionEnum.W,
        DirectionEnum.E: DirectionEnum.N,
        DirectionEnum.S: DirectionEnum.E,
        DirectionEnum.W: DirectionEnum.S,
    }

    def turn_right(self):
        self.d = self.RIGHT_TURNS[self.d]

    def turn_left(self):
        self.d = self.LEFT_TURNS[self.d]

    def turn_around(self):
        self.d = self.OPPOSITES[self.d]

    def update_carrier(
        self, carrier: tuple[int, int], infected: bool
    ) -> tuple[int, int]:
        x, y = carrier
        if infected:
            self.turn_right()
        else:
            self.turn_left()
        return x + self.d.value[0], y + self.d.value[1]

    def update_carrier_v2(
        self, carrier: tuple[int, int], infected: bool, weakened: bool, flagged: bool
    ) -> tuple[int, int]:
        x, y = carrier
        if infected:
            self.turn_right()
        elif weakened:
            pass
        elif flagged:
            self.turn_around()
        else:
            self.turn_left()
        return x + self.d.value[0], y + self.d.value[1]


def part_1() -> int:
    grid = set[tuple[int, int]]()
    width = height = 0
    for x, line in enumerate(input.read_text().splitlines()):
        width = len(line)
        height += 1
        for y, node in enumerate(line):
            if node == "#":
                grid.add((x, y))

    carrier = width // 2, height // 2
    direction = Direction(DirectionEnum.N)

    count = 0
    for i in range(10_000):
        infected = carrier in grid
        next_position = direction.update_carrier(carrier, infected)
        if infected:
            grid.remove(carrier)
        else:
            count += 1
            grid.add(carrier)
        carrier = next_position
    return count


def part_2() -> int:
    infected_nodes = set[tuple[int, int]]()
    weakened_nodes = set[tuple[int, int]]()
    flagged_nodes = set[tuple[int, int]]()
    width = height = 0
    for x, line in enumerate(input.read_text().splitlines()):
        width = len(line)
        height += 1
        for y, node in enumerate(line):
            if node == "#":
                infected_nodes.add((x, y))

    carrier = width // 2, height // 2
    direction = Direction(DirectionEnum.N)

    count = 0
    for i in range(10_000_000):
        infected = carrier in infected_nodes
        weakened = carrier in weakened_nodes
        flagged = carrier in flagged_nodes
        clean = not infected and not weakened and not flagged
        next_position = direction.update_carrier_v2(
            carrier, infected, weakened, flagged
        )
        if clean:
            weakened_nodes.add(carrier)
        elif weakened:
            count += 1
            infected_nodes.add(carrier)
            weakened_nodes.remove(carrier)
        elif infected:
            infected_nodes.remove(carrier)
            flagged_nodes.add(carrier)
        elif flagged:
            flagged_nodes.remove(carrier)
        carrier = next_position
    return count


print(part_1())
print(part_2())
