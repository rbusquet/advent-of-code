import re

from collections import defaultdict
from typing import List

regex = re.compile(
    r"position=<([\s-]*\d+), ([\s-]*\d+)> velocity=<([\s-]*\d+),([\s-]*\d+)>"
)


class Vector:
    def __init__(
        self,
        px: int,
        py: int,
        vx: int,
        vy: int,
    ):
        self._px = px
        self._py = py
        self.vx = vx
        self.vy = vy

    def move(self, vx=None, vy=None, steps=1):
        self._px += vx or (self.vx * steps)
        self._py += vy or (self.vy * steps)

    @property
    def current_position(self):
        return self._px, self._py


vectors: List[Vector] = []
min_x = min_y = 0

with open("input10.txt") as f:
    for line in f.readlines():
        px, py, vx, vy = map(int, regex.match(line).groups())
        vectors.append(Vector(px, py, vx, vy))
        min_x = min(min_x, px)
        min_y = min(min_y, py)

STEPS = 5
total_seconds = 0
while True:
    matrix = defaultdict(lambda: ".")
    for vector in vectors:
        vector.move(steps=STEPS)
    total_seconds += STEPS

    positions = [v.current_position for v in vectors]
    min_x = min(positions)[0]
    min_y = min(positions, key=lambda n: n[1])[1]

    # normalize vectors
    for vector in vectors:
        vector.move(-min_x, -min_y)
        matrix[vector.current_position] = "#"

    max_x = max(matrix)[0]
    max_y = max(matrix, key=lambda n: n[1])[1]
    if max_x > 200:
        print(f"{max_x} is still large to print")
        continue
    STEPS = 1
    print(f"Sky at {total_seconds}")
    for x in range(-5, max_y + 5):
        row = []
        for y in range(-5, max_x + 5):
            row.append(matrix[y, x])
        print("".join(row))
    # input()

    if total_seconds == 10144:
        break
