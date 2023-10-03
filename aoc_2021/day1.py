from collections import deque
from itertools import islice
from pathlib import Path
from typing import Iterable, Iterator


def sliding_window[T](iterable: Iterable[T], n: int) -> Iterator[tuple[T, ...]]:
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


if __name__ == "__main__":
    print(part_1())
    print(part_2())
