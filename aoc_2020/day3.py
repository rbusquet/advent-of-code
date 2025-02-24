from collections.abc import Iterator
from functools import reduce
from itertools import count
from operator import mul


def read_file() -> Iterator[str]:
    with open("./input.txt") as f:
        yield from f.readlines()


def count_trees(right: int, down: int) -> int:
    counter = count(step=right)
    total_trees = 0
    for i, line in enumerate(read_file()):
        if i % down != 0:
            continue
        line = line.strip()
        position = next(counter) % len(line)
        total_trees += line[position] == "#"
    return total_trees


print("--- part 1 ---")
print(count_trees(3, 1))
print("-- part 2 ---")
vals = [
    count_trees(1, 1),
    count_trees(3, 1),
    count_trees(5, 1),
    count_trees(7, 1),
    count_trees(1, 2),
]
print(reduce(mul, vals))
