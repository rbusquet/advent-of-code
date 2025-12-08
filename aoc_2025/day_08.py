from collections import Counter
from itertools import combinations, count
from pathlib import Path
from typing import NamedTuple

input = Path(__file__).parent / "input.txt"


class Position(NamedTuple):
    x: int
    y: int
    z: int


def distance(a: Position, b: Position) -> int:
    """straight-line distance between two 3D positions"""
    return sum((a[i] - b[i]) ** 2 for i in range(3)) ** 0.5


def part_1() -> int:
    world = [
        Position(*map(int, line.split(","))) for line in input.read_text().splitlines()
    ]

    gen = count(1)

    pairs = sorted(combinations(world, 2), key=lambda pair: distance(*pair))
    circuits = dict[Position, int]()

    for pair in pairs[:10]:
        if pair[0] in circuits or pair[1] in circuits:
            circuit_id1 = circuits.get(pair[0]) or next(gen)
            circuit_id2 = circuits.get(pair[1]) or next(gen)
            # update all positions with the higher circuit id to the lower one
            lower_id = min(circuit_id1, circuit_id2)
            for pos, cid in circuits.items():
                if cid == circuit_id1 or cid == circuit_id2:
                    circuits[pos] = lower_id
            circuits[pair[0]] = lower_id
            circuits[pair[1]] = lower_id
            continue
        circuit_id = next(gen)
        circuits[pair[0]] = circuit_id
        circuits[pair[1]] = circuit_id
    c1, c2, c3 = Counter(circuits.values()).most_common(3)
    return c1[1] * c2[1] * c3[1]


def part_2() -> int:
    world = [
        Position(*map(int, line.split(","))) for line in input.read_text().splitlines()
    ]

    pairs = sorted(combinations(world, 2), key=lambda pair: distance(*pair))
    circuits = dict[Position, set[Position]]()

    for pair in pairs:
        if pair[0] in circuits or pair[1] in circuits:
            set1 = circuits.get(pair[0], {pair[0]})
            set2 = circuits.get(pair[1], {pair[1]})
            merged = set1 | set2
            for pos in merged:
                circuits[pos] = merged
            print(f"Merged circuit with {pair[0]} and {pair[1]}", len(merged))
            if len(merged) == 1000:
                print("Found circuit with 1000 positions!")
                return pair[0].x * pair[1].x
            continue
        circuits[pair[0]] = circuits[pair[1]] = {pair[0], pair[1]}
        print(f"New circuit with {pair[0]} and {pair[1]}")

    return 0


print(part_1())
print(part_2())
