from collections import deque
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Iterator

input = Path(__file__).parent / "input.txt"


N = (-1, 0)
S = (1, 0)
E = (0, 1)
W = (0, -1)


Position = tuple[int, int]
Plot = tuple[str | None, int, int]

DIRECTIONS = [N, S, E, W]


def neighborhood(i: int, j: int) -> Iterator[Position]:
    for ii, jj in DIRECTIONS:
        yield i + ii, j + jj


@dataclass
class Region:
    crop: str
    plots: list[Position] = field(default_factory=list)
    edges: list[Position] = field(default_factory=list)
    current: Position | None = None

    @property
    def cost(self):
        return self.area * self.perimeter

    @property
    def cost_v2(self):
        return self.area * self.sides

    @property
    def area(self):
        return len(self.plots)

    @property
    def perimeter(self):
        return len(list(self.edges))

    def print(self) -> None:
        min_x = min(a[0] for a in self.plots) - 3
        max_x = max(a[0] for a in self.plots) + 3
        min_y = min(a[1] for a in self.plots) - 3
        max_y = max(a[1] for a in self.plots) + 3

        edges = [(a[0], a[1]) for a in self.edges]

        for x in range(min_x, max_x):
            for y in range(min_y, max_y):
                if (x, y) == self.current:
                    print("*", end="")
                elif (x, y) in edges:
                    print("0", end="")
                elif (x, y) in self.plots:
                    print(self.crop, end="")
                else:
                    print(".", end="")
            print()
        print()

    @cached_property
    def sides(self):
        # self.print()
        edges = sorted(self.edges)

        direction = E
        clock = {N: E, E: S, S: W, W: N}
        counter = {N: W, W: S, S: E, E: N}
        start = current = edges[0]
        corners = set()
        outer_done = False
        while True:
            self.current = current
            # self.print()
            if current in edges:
                edges.remove(current)
            next_step = current[0] + direction[0], current[1] + direction[1]

            if next_step == start:
                # close the loop
                if edges:  # there are holes
                    if not outer_done:
                        # holes run the opposite way
                        counter, clock = clock, counter
                        outer_done = True
                    outer_done = True
                    start = current = edges[0]
                    continue
                else:
                    break
            elif next_step in self.plots:
                # turn counter-clockwise
                direction = counter[direction]
                corners.add(current)
            elif next_step in self.edges:
                # keep walking
                current = next_step
            else:  # outside. walk one as if it was an edge
                corners.add(next_step)
                current = next_step
                direction = clock[direction]
        return len(corners)


def scale(grid: list[list[str]], times: int) -> list[list[str]]:
    scaled = []

    for row in grid:
        new_row = []
        for char in row:
            new_row.extend([char] * times)
        scaled.extend([new_row] * times)

    return scaled


def part_1() -> int:
    grid = [list(line) for line in input.read_text().splitlines()]
    width = len(grid[0])
    height = len(grid)

    regions = list[Region]()
    visited = set[Position]()
    for x, row in enumerate(grid):
        for y, crop in enumerate(row):
            if (x, y) in visited:
                continue
            region = Region(crop)
            queue = deque([(x, y)])
            while queue:
                current = queue.pop()
                if current in visited:
                    continue
                visited.add(current)
                region.plots.append(current)
                for i, j in neighborhood(*current):
                    height_bounds = i >= 0 and i < height
                    width_bounds = j >= 0 and j < width
                    if not height_bounds or not width_bounds:
                        region.edges.append((i, j))
                    elif grid[i][j] != crop:
                        region.edges.append((i, j))
                    else:
                        queue.append((i, j))
            region.print()
            print(
                f"A region of {crop} plants with price "
                f"{region.area} * {region.perimeter} = {region.cost}."
            )
            regions.append(region)

    return sum(region.cost for region in regions)


def part_2() -> int:
    grid = scale([list(line) for line in input.read_text().splitlines()], 3)
    width = len(grid[0])
    height = len(grid)

    regions = list[Region]()
    visited = set[Position]()
    for x, row in enumerate(grid):
        for y, crop in enumerate(row):
            if (x, y) in visited:
                continue
            region = Region(crop)
            queue = deque([(x, y)])
            while queue:
                current = queue.pop()
                if current in visited:
                    continue
                visited.add(current)
                region.plots.append(current)
                for i, j in neighborhood(*current):
                    height_bounds = i >= 0 and i < height
                    width_bounds = j >= 0 and j < width
                    if not height_bounds or not width_bounds:
                        region.edges.append((i, j))
                    elif grid[i][j] != crop:
                        region.edges.append((i, j))
                    else:
                        queue.append((i, j))
            # region.print()
            print(
                f"A region of {crop} plants with price "
                f"{region.area // 9} * {region.sides} = {region.cost_v2 // 9}."
            )
            regions.append(region)

    return sum(region.cost_v2 // 9 for region in regions)


print(part_1())
print("---")
print(part_2())
