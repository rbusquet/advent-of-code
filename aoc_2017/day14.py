from collections import defaultdict
from pathlib import Path
from typing import Iterator

from knot_hash import knot_hash

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    key = "flqrgnkx"

    grid = list[str]()
    for i in range(128):
        hash = knot_hash(f"{key}-{i}")
        grid.append("".join(f"{int(h, 16):0>4b}" for h in hash))

    return sum(row.count("1") for row in grid)


N = (-1, 0)
S = (1, 0)
E = (0, 1)
W = (0, -1)


def neighborhood(i: int, j: int) -> Iterator[tuple[int, int]]:
    for ii, jj in (N, S, E, W):
        yield i + ii, j + jj


def part_2() -> int:
    key = "flqrgnkx"

    squares = set[tuple[int, int]]()

    for i in range(128):
        hash = knot_hash(f"{key}-{i}")
        row = "".join(f"{int(h, 16):0>4b}" for h in hash)
        for j, bit in enumerate(row):
            if bit == "0":
                continue
            squares.add((i, j))

    regions = 0
    visited = set()
    region_counts = defaultdict[int, int](int)
    for square in sorted(squares):
        if square not in visited:
            regions += 1
            queue = [square]
            while queue:
                current_square = queue.pop()
                region_counts[regions] += 1
                visited.add(current_square)
                for child in neighborhood(*current_square):
                    if child not in squares:
                        continue
                    if child not in visited:
                        queue.append(child)
    print(max(region_counts.items(), key=lambda a: a[1]))
    return regions


print(part_1())
print(part_2())
