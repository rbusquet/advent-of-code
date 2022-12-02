import functools
import time
from functools import reduce
from itertools import combinations
from operator import mul
from typing import Callable, ParamSpec, TypeVar, cast

P = ParamSpec("P")
T = TypeVar("T")


def time_it(fn: Callable[P, T]) -> Callable[P, T]:
    @functools.wraps(fn)
    def timed(*args: P.args, **kwargs: P.kwargs) -> T:
        before = time.process_time_ns()
        result = fn(*args, **kwargs)
        after = time.process_time_ns()
        diff = after - before
        print(f"{fn.__name__} ran in {diff}ns")
        return cast(T, result)

    return timed


def read_file() -> list[str]:
    with open("./input.txt") as f:
        return f.readlines()


@time_it
def with_combinations(lst: list[int], n: int) -> int | None:
    for test in combinations(lst, n):
        if sum(test) == 2020:
            return reduce(mul, test)
    return None


@time_it
def best_performance_part_1(lst: list[int]) -> int | None:
    for number in lst:
        if 2020 - number in lst:
            return number * (2020 - number)
    return None


@time_it
def best_performance_part_2(lst: list[int]) -> int:
    n = len(lst)
    for i in range(n):
        left = i + 1
        right = n - 1
        while left < right:
            result = lst[i] + lst[left] + lst[right]
            if result == 2020:
                return lst[i] * lst[left] * lst[right]
            if result < 2020:
                left += 1
            else:
                right -= 1
    raise Exception("something bad happened")


if __name__ == "__main__":
    # sort ahead of time, doesn't hurt
    in_ = sorted(map(int, read_file()))

    print(with_combinations(in_, 2))
    print(with_combinations(in_, 3))
    print(best_performance_part_1(in_))
    print(best_performance_part_2(in_))
