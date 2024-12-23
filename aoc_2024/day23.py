from collections import defaultdict
from pathlib import Path

input = Path(__file__).parent / "input.txt"


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
    matrix = defaultdict[str, list[str]](list)
    with input.open() as file:
        for line in file:
            a, b = line.strip().split("-")
            matrix[a].append(b)
            matrix[b].append(a)

    maximals = set[frozenset[str]]()

    def find_maximal_cliques(
        current_clique: set[str], candidates: set[str], excluded: set[str]
    ) -> None:
        if not candidates and not excluded:
            maximals.add(frozenset(current_clique))
        while candidates:
            vertex = candidates.pop()
            new_clique = current_clique.union({vertex})
            new_candidates = candidates.intersection(matrix[vertex])
            new_excluded = excluded.intersection(matrix[vertex])
            find_maximal_cliques(new_clique, new_candidates, new_excluded)
            candidates -= {vertex}
            excluded.add(vertex)

    find_maximal_cliques(set(), set(matrix.keys()), set())

    largest = max(maximals, key=len)
    return ",".join(sorted(largest))


print(part_1())
print(part_2())
