import time
from itertools import combinations
from operator import mul
from functools import reduce


def time_it(fn):
    def timed(*args, **kwargs):
        before = time.process_time_ns()
        result = fn(*args, **kwargs)
        after = time.process_time_ns()
        diff = after - before
        print(f"{fn.__name__} ran in {diff}ns")
        return result

    return timed


def read_file():
    with open("./input.txt") as f:
        return f.readlines()


@time_it
def with_combinations(lst, n):
    for test in combinations(lst, n):
        if sum(test) == 2020:
            return reduce(mul, test)


@time_it
def best_performance_part_1(lst):
    for number in lst:
        if 2020 - number in lst:
            return number * (2020 - number)


@time_it
def best_performance_part_2(lst):
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
