from collections.abc import Iterator
from pathlib import Path

import numpy as np

input = Path(__file__).parent / "input.txt"


def to_array(line: str) -> np.ndarray:
    return np.array(list(map(lambda a: [int(c == "#") for c in a], line.split("/"))))


def to_bytes(arr: np.ndarray) -> bytes:
    return np.ndarray.tobytes(arr)


def rotates(arr: np.ndarray) -> Iterator[np.ndarray]:
    for i in range(4):
        yield (rotated := np.rot90(arr, k=i))
        yield np.fliplr(rotated)
        yield np.flipud(rotated)


def solve(count: int) -> int:
    rules = dict[bytes, np.ndarray]()
    for line in input.read_text().splitlines():
        left, right = line.split(" => ")
        for m in rotates(to_array(left)):
            rules[to_bytes(m)] = to_array(right)
    start = np.array(
        [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
        ]
    )

    for i in range(count):
        rows, cols = start.shape

        steps = 2 if rows % 2 == 0 else 3
        result = []
        for i in range(0, rows, steps):
            row = []
            for j in range(0, cols, steps):
                square = start[i : i + steps, j : j + steps]
                row.append(rules[to_bytes(square)])
            result.append(np.concat(row, axis=1))
        start = np.concat(result)

    return np.count_nonzero(start)


print(solve(5))
print(solve(18))
