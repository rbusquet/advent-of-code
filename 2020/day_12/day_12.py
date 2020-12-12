import re
from dataclasses import dataclass
from math import cos, radians, sin
from typing import Tuple


def read_file():
    with open("./input.txt") as f:
        yield from map(lambda c: c.strip(), f.readlines())


@dataclass
class Ferry:
    position: Tuple[int, int]
    velocity: Tuple[int, int]

    def north(self, count):
        self.position[1] += count

    def south(self, count):
        self.position[1] -= count

    def east(self, count):
        self.position[0] += count

    def west(self, count):
        self.position[0] -= count

    def north_waypoint(self, count):
        self.velocity[1] += count

    def south_waypoint(self, count):
        self.velocity[1] -= count

    def east_waypoint(self, count):
        self.velocity[0] += count

    def west_waypoint(self, count):
        self.velocity[0] -= count

    def left(self, count):
        rads = radians(count)
        x, y = self.velocity
        xx = x * cos(rads) - y * sin(rads)
        yy = x * sin(rads) + y * cos(rads)
        self.velocity = [xx, yy]

    def right(self, count):
        rads = radians(count)
        x, y = self.velocity
        xx = x * cos(rads) + y * sin(rads)
        yy = -x * sin(rads) + y * cos(rads)
        self.velocity = [xx, yy]

    def forward(self, count):
        self.position[0] += self.velocity[0] * count
        self.position[1] += self.velocity[1] * count

    def move(self, direction, count):
        return {
            "N": self.north,
            "S": self.south,
            "E": self.east,
            "W": self.west,
            "L": self.left,
            "R": self.right,
            "F": self.forward,
        }[direction](count)

    def move_to_waypoint(self, direction, count):
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
ferry = Ferry([0, 0], [1, 0])
for instruction in read_file():
    direction, count = expression.match(instruction).groups()
    ferry.move(direction, int(count))
print("--- part 1 ---")
print(ferry.distance())

ferry = Ferry([0, 0], [10, 1])

for instruction in read_file():
    direction, count = expression.match(instruction).groups()
    ferry.move_to_waypoint(direction, int(count))

print("--- part 2 ---")
print(ferry.distance())
