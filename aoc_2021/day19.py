from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Iterable, Iterator

from more_itertools import one

Vector = tuple[int, int, int]
Pair = tuple[Vector, Vector]
Scanners = dict[int, list[Vector]]


def parse_scanners() -> Scanners:
    scanners: Scanners = Scanners()

    with open(Path(__file__).parent / "input.txt") as file:
        for line in file:
            data = line.split()
            if len(data) == 4:
                scanner_id = int(data[2])
                scanners[int(scanner_id)] = []
            elif len(data) == 1:
                x, y, z = tuple(map(int, data[0].split(",")))
                scanners[scanner_id].append((x, y, z))
    return scanners


def distance(a: Vector, b: Vector) -> float:
    x1, y1, z1 = a
    x2, y2, z2 = b
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5


def manhattan_distance(a: Vector, b: Vector) -> float:
    x1, y1, z1 = a
    x2, y2, z2 = b
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def roll(v: Vector) -> Vector:
    return v[0], v[2], -v[1]


def turn(v: Vector) -> Vector:
    return -v[1], v[0], v[2]


def generate_rotations(v: Vector) -> Iterator[Vector]:
    for _ in range(2):
        for _ in range(3):  # Yield RTTT 3 times
            v = roll(v)
            yield v  # Yield R
            for _ in range(3):  # Yield TTT
                v = turn(v)
                yield v
        v = roll(turn(roll(v)))  # Do RTR


def find_everything() -> tuple[set[Vector], set[Vector]]:
    scanners = parse_scanners()

    distances = dict[int, dict[float, Pair]]()

    base_beacons = scanners[0]
    known_scanners = {0}
    known_beacons = set(base_beacons)
    distances[0] = {}
    for a, b in combinations(known_beacons, 2):
        distances[0][distance(a, b)] = (a, b)
    known_scanner_locations = {(0, 0, 0)}

    while len(known_scanners) < len(scanners):
        for scanner, beacons in scanners.items():
            if scanner in known_scanners:
                continue
            single_matches = match_to_known_beacons(beacons, distances.values())
            if single_matches is None:
                continue

            rotators = {beacon: generate_rotations(beacon) for beacon in beacons}

            for _ in range(24):
                offsets = set[Vector]()
                rotated_beacons = list[Vector]()

                for beacon, rotator in rotators.items():
                    xx, yy, zz = next(rotator)
                    rotated_beacons.append((xx, yy, zz))
                    if single_matches.get(beacon):
                        x, y, z = single_matches[beacon]
                        offsets.add((x - xx, y - yy, z - zz))

                if len(offsets) == 1:
                    xx, yy, zz = one(offsets)
                    known_scanner_locations.add((xx, yy, zz))
                    known_scanners.add(scanner)
                    new_beacons = {
                        (x + xx, y + yy, z + zz) for (x, y, z) in rotated_beacons
                    }
                    distances[scanner] = {}
                    for a, b in combinations(new_beacons, 2):
                        distances[scanner][distance(a, b)] = (a, b)
                    known_beacons.update(new_beacons)
                    break
    return known_beacons, known_scanner_locations


def match_to_known_beacons(
    beacons: list[Vector], distances: Iterable[dict[float, Pair]]
) -> None | dict[Vector, Vector]:
    current_distances = dict[float, Pair]()
    for a, b in combinations(beacons, 2):
        current_distances[distance(a, b)] = a, b
    for o_distances in distances:
        matches = defaultdict[Vector, set[Vector]](set)
        for d, (a, b) in current_distances.items():
            if o_distances.get(d):
                if not matches[a]:
                    matches[a].update(o_distances[d])
                else:
                    matches[a] = matches[a].intersection(o_distances[d])
                if not matches[b]:
                    matches[b].update(o_distances[d])
                else:
                    matches[b] = matches[b].intersection(o_distances[d])
        single_matches = {k: one(v) for k, v in matches.items() if len(v) == 1}
        if len(single_matches) >= 12:
            return single_matches
    return None


def resolve() -> None:
    beacons, scanners = find_everything()
    print(len(beacons))
    print(max(manhattan_distance(a, b) for a, b in combinations(scanners, 2)))


if __name__ == "__main__":
    resolve()
