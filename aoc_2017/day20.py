from collections import defaultdict
from itertools import pairwise
from pathlib import Path
from typing import NamedTuple

input = Path(__file__).parent / "input.txt"


class Vector(NamedTuple):
    x: int
    y: int
    z: int

    def __abs__(self) -> int:
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __repr__(self) -> str:
        return f"<{self.x},{self.y},{self.z}> ({abs(self)})"

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        return self + other * -1

    def __mul__(self, value: int) -> "Vector":
        return Vector(
            value * self.x,
            value * self.y,
            value * self.z,
        )


class Particle(NamedTuple):
    id: int
    p: Vector
    v: Vector
    a: Vector

    def key(self) -> tuple[float, float, float]:
        return (abs(self.a), abs(self.v), abs(self.p))

    def position(self, t: int = 0) -> Vector:
        _, p, v, a = self
        vt = v * t
        t2 = (t * (t + 1)) // 2
        at2 = a * t2
        return p + vt + at2


def part_1() -> int:
    particles = list[Particle]()
    for i, line in enumerate(input.read_text().splitlines()):
        p, v, a = map(
            lambda a: Vector(*map(int, a.strip("avp=<>").split(","))),
            line.split(", "),
        )
        particles.append(Particle(i, p, v, a))

    particles.sort(key=lambda p: abs(p.position(1000)))
    return particles[0].id


def part_2() -> int:
    particles = list[Particle]()
    for i, line in enumerate(input.read_text().splitlines()):
        p, v, a = map(
            lambda a: Vector(*map(int, a.strip("avp=<>").split(","))),
            line.split(", "),
        )
        particles.append(Particle(i, p, v, a))

    dead = set[Particle]()
    counter = defaultdict[int, int](int)
    initial_len = len(particles)
    i = -1
    while True:
        i += 1
        for p1, p2 in pairwise(particles):
            if p1.position(i) == p2.position(i):
                dead.add(p1)
                dead.add(p2)
        particles = [p for p in particles if p not in dead]
        if len(particles) == initial_len:
            continue
        counter[len(particles)] += 1
        if counter[len(particles)] > 2:
            return len(particles)


print(part_1())
print(part_2())
