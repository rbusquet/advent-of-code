import re
from dataclasses import dataclass
from math import cos, radians, sin
from typing import Iterable, Tuple


def read_file() -> Iterable[str]:
    with open("./input.txt") as f:
        yield from map(lambda c: c.strip(), f.readlines())


@dataclass
class Ferry:
    position: Tuple[float | int, float | int]
    velocity: Tuple[float | int, float | int]

    def north(self, count: int) -> None:
        x, y = self.position
        self.position = (x, y + count)

    def south(self, count: int) -> None:
        x, y = self.position
        self.position = (x, y - count)

    def east(self, count: int) -> None:
        x, y = self.position
        self.position = (x + count, y)

    def west(self, count: int) -> None:
        x, y = self.position
        self.position = (x - count, y)

    def north_waypoint(self, count: int) -> None:
        vx, vy = self.velocity
        self.velocity = (vx, vy + count)

    def south_waypoint(self, count: int) -> None:
        vx, vy = self.velocity
        self.velocity = (vx, vy - count)

    def east_waypoint(self, count: int) -> None:
        vx, vy = self.velocity
        self.velocity = (vx + count, vy)

    def west_waypoint(self, count: int) -> None:
        vx, vy = self.velocity
        self.velocity = (vx - count, vy)

    def left(self, count: int) -> None:
        rads = radians(count)
        x, y = self.velocity
        xx = x * cos(rads) - y * sin(rads)
        yy = x * sin(rads) + y * cos(rads)
        self.velocity = (xx, yy)

    def right(self, count: int) -> None:
        rads = radians(count)
        x, y = self.velocity
        xx = x * cos(rads) + y * sin(rads)
        yy = -x * sin(rads) + y * cos(rads)
        self.velocity = (xx, yy)

    def forward(self, count: int) -> None:
        x, y = self.position
        self.position = (x + self.velocity[0] * count, y + self.velocity[1] * count)

    def move(self, direction, count: int) -> None:
        return {
            "N": self.north,
            "S": self.south,
            "E": self.east,
            "W": self.west,
            "L": self.left,
            "R": self.right,
            "F": self.forward,
        }[direction](count)

    def move_to_waypoint(self, direction, count: int) -> None:
        return {
            "N": self.north_waypoint,
            "S": self.south_waypoint,
            "E": self.east_waypoint,
            "W": self.west_waypoint,
            "L": self.left,
            "R": self.right,
            "F": self.forward,
        }[direction](count)

    def distance(self):
        return round(abs(self.position[0]) + abs(self.position[1]))


expression = re.compile(r"(\w)(\d+)")
ferry = Ferry((0, 0), (1, 0))
for instruction in read_file():
    if match := expression.match(instruction):
        direction, count = match.groups()
        ferry.move(direction, int(count))
print("--- part 1 ---")
print(ferry.distance())

ferry = Ferry((0, 0), (10, 1))

for instruction in read_file():
    if match := expression.match(instruction):
        direction, count = match.groups()
        ferry.move_to_waypoint(direction, int(count))

print("--- part 2 ---")
print(ferry.distance())
