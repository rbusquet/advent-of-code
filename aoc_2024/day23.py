from collections import defaultdict
from pathlib import Path
from typing import Callable, Iterator

from more_itertools import first

input = Path(__file__).parent / "input.txt"


def find_maximal_cliques(
    current_clique: set[str],
    candidates: set[str],
    excluded: set[str],
    n: Callable[[str], set[str]],
) -> Iterator[frozenset[str]]:
    if not candidates and not excluded:
        yield frozenset(current_clique)
        return
    pivot = first(candidates, None)
    neighboors = n(pivot) if pivot else set()
    for vertex in candidates - neighboors:
        yield from find_maximal_cliques(
            current_clique | {vertex},
            candidates & n(vertex),
            excluded & n(vertex),
            n,
        )
        excluded.add(vertex)


def part_1() -> int:
    matrix = defaultdict[str, list[str]](list)
    with input.open() as file:
        for line in file:
            a, b = line.strip().split("-")
            matrix[a].append(b)
            matrix[b].append(a)

    seen = set[frozenset]()
    count = 0
    for c1 in matrix:
        if not c1.startswith("t"):
            continue
        for c2 in matrix[c1]:
            for c3 in matrix[c2]:
                trio = frozenset([c1, c2, c3])
                if len(trio) != 3:
                    continue
                if trio in seen:
                    continue
                seen.add(trio)
                if c1 in matrix[c3]:
                    count += 1

    return count


def part_2() -> str:
    matrix = defaultdict[str, set[str]](set)
    with input.open() as file:
        for line in file:
            a, b = line.strip().split("-")
            matrix[a].add(b)
            matrix[b].add(a)

    maximals = list(
        find_maximal_cliques(set(), set(matrix.keys()), set(), lambda x: matrix[x])
    )

    largest = max(maximals, key=len)
    return ",".join(sorted(largest))


print(part_1())
print(part_2())
