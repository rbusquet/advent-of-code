from __future__ import annotations

import functools
import time
from collections import Counter, defaultdict
from heapq import heapify, heappop, heappush
from pathlib import Path
from typing import Callable, cast

DAYS = 80


def time_it[**P, T](fn: Callable[P, T]) -> Callable[P, T]:
    @functools.wraps(fn)
    def timed(*args: P.args, **kwargs: P.kwargs) -> T:
        before = time.process_time_ns()
        result = fn(*args, **kwargs)
        after = time.process_time_ns()
        diff = after - before
        print(f"{fn.__name__} ran in {diff}ns")
        return cast(T, result)

    return timed


@time_it
def grow_slow(fishes: list[int], max_days: int) -> int:
    """
    Naive implementation, solves for part 1 but can't do part 2.
    """
    days = 0
    while days < max_days:
        new_fishes = []

        for i, fish in enumerate(fishes):
            if fish == 0:
                fishes[i] = 6
                new_fishes.append(8)
                continue
            fishes[i] -= 1
        fishes.extend(new_fishes)
        days += 1

    return len(fishes)


@time_it
def grow_fast(initial: list[int], max_days: int) -> int:
    """
    Got the right answer with this solution.
    """
    same_age = Counter(initial)
    fishes_by_age = same_age.most_common()
    days = 0

    while days < max_days:
        next_fishes = defaultdict[int, int](int, fishes_by_age)

        for age, total_fishes in fishes_by_age:
            week_ended = age == 0
            new_age = 6 if week_ended else (age - 1)
            next_fishes[new_age] += total_fishes
            next_fishes[age] -= total_fishes

            if week_ended:
                next_fishes[8] += total_fishes
        fishes_by_age = list(next_fishes.items())

        days += 1
    return sum(f[1] for f in fishes_by_age)


@time_it
def grow_faster(initial: list[int], max_days: int) -> int:
    """
    Similar solution to above, but avoids creating new lists.
    Takes about half the time as the above.
    """
    same_age = Counter(initial)
    days = 0

    while days < max_days:
        spawning = same_age.pop(0, 0)
        for age in range(8):
            same_age[age] = same_age[age + 1]
        same_age[6] += spawning
        same_age[8] = spawning

        days += 1
    return sum(same_age.values())


@time_it
def grow_fastest(initial: list[int], max_days: int) -> int:
    """
    Fastest implementation by using a heapq and just popping items, not shifting.

    The real fastes solution uses algebra / matrices I don't know how to do that
    """
    same_age = Counter(initial)
    fishes_by_age = same_age.most_common()

    heapify(fishes_by_age)
    days = 0

    while days < max_days:
        day_spawn = 0
        while fishes_by_age[0][0] == days:
            _, spawn = heappop(fishes_by_age)
            day_spawn += spawn

        seven = days + 7
        nine = days + 9

        heappush(fishes_by_age, (seven, day_spawn))
        heappush(fishes_by_age, (nine, day_spawn))

        days += 1
    return sum(f[1] for f in fishes_by_age)


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        fishes = list(map(int, file.readline().split(",")))
    return grow_slow(fishes, max_days=80)


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        fishes = list(map(int, file.readline().split(",")))
    return grow_fast(fishes, 256)


def part_2_faster() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        fishes = list(map(int, file.readline().split(",")))
    return grow_faster(fishes, 256)


def part_2_fastest() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        fishes = list(map(int, file.readline().split(",")))
    return grow_fastest(fishes, 256)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
    print(part_2_faster())
    print(part_2_fastest())
