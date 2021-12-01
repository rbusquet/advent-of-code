from pathlib import Path
from collections import deque
from itertools import islice
from typing import TypeVar, Iterable, Iterator

T = TypeVar("T")


def sliding_window(iterable: Iterable[T], n: int) -> Iterator[tuple[T, ...]]:
    it = iter(iterable)
    window = deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        previous = int(file.readline())

        increases = 0
        for value in map(int, file):
            increases += value > previous
            previous = value
        return increases


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:

        it = sliding_window(map(int, file), 3)
        previous = next(it)

        increases = 0
        for window in it:
            increases += sum(window) > sum(previous)
            previous = window
        return increases


print(part_1())
print(part_2())
