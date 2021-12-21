from itertools import combinations
from pathlib import Path

import more_itertools

Vector = tuple[int, int, int]

Scanners = dict[int, list[Vector]]


def parse_scanners() -> Scanners:
    scanners: Scanners = Scanners()

    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
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


if __name__ == "__main__":  # noqa: C901
    scanners = parse_scanners()
    print(f"{len(scanners)=}")

    distances = dict[float, tuple[Vector, Vector]]()

    base_beacons = scanners[0]
    known_scanners = {0}
    known_beacons = set(base_beacons)

    for a, b in combinations(base_beacons, 2):
        if distance(a, b) in distances:
            print("not unique distance :/")
        distances[distance(a, b)] = (a, b)

    while len(known_scanners) != len(scanners):
        for scanner, beacons in scanners.items():
            if scanner in known_scanners:
                continue
            current_distances = dict[float, tuple[Vector, Vector]]()

            sample_distance = 0.0
            seen_vectors = dict[Vector, set[Vector]]()
            for a, b in combinations(beacons, 2):
                d = distance(a, b)
                if distances.get(d):
                    aa, bb = distances[d]
                    if a in seen_vectors:
                        seen_vectors[a] &= {aa, bb}
                    else:
                        seen_vectors[a] = {aa, bb}
                    if b in seen_vectors:
                        seen_vectors[b] &= {aa, bb}
                    else:
                        seen_vectors[b] = {aa, bb}

                else:
                    current_distances[d] = (a, b)
            seen_vectors = {k: v for k, v in seen_vectors.items() if v}

            if len(seen_vectors) >= 12:
                for a, _original in seen_vectors.items():
                    b = more_itertools.one(_original)
                    diff = b[0] + a[0], b[1] - a[1], b[2] + a[2]
                for d, (a, b) in current_distances.items():
                    aa = (diff[0] - a[0], diff[1] + a[1], diff[2] - a[2])
                    bb = (diff[0] - b[0], diff[1] + b[1], diff[2] - b[2])
                    known_beacons.add(aa)
                    known_beacons.add(bb)
                    distances[d] = (aa, bb)

    print(len(known_beacons))
