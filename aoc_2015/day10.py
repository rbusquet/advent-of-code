from pathlib import Path
from time import time_ns
from typing import Generator, Iterator

from more_itertools import run_length


def look_and_say(look: Iterator[str]) -> Iterator[str]:
    counter = run_length.encode(look)
    for ch, count in counter:
        yield str(count)
        yield ch


def yield_and_count[T](seq: Iterator[T]) -> Generator[T, None, None]:  # type: ignore[misc,name-defined]
    _count = 0
    for _count, x in enumerate(seq):
        yield x
    print(_count)


def part_1() -> None:
    print("start time:", time_ns())
    with open(Path(__file__).parent / "input.txt") as file:
        initial = file.readline().strip()
    print(time_ns())
    word = iter(initial)
    print(time_ns())
    for x in range(50):
        if x == 40:
            print("part 1 result: ", end="")
            word = yield_and_count(word)
        word = look_and_say(word)
        print(f"loop {x}:", time_ns())
    print("part 2 result: ", end="")
    print(len(list(word)))


if __name__ == "__main__":
    part_1()
