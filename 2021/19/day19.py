from pathlib import Path
import numpy as np
import numpy.typing as npt

from itertools import combinations

Scanners = dict[int, list[npt.NDArray[np.int_]]]


def parse_scanners() -> Scanners:
    scanners: Scanners = Scanners()

    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        for line in file:
            data = line.split()
            if len(data) == 4:
                scanner_id = int(data[2])
                scanners[int(scanner_id)] = []
            elif len(data) == 1:
                beacon = np.array(tuple(map(int, data[0].split(","))))
                scanners[scanner_id].append(beacon)
    return scanners


# def part_2():
#     with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
#         pass


if __name__ == "__main__":
    scanners = parse_scanners()

    distances = set()  # type: ignore

    base_beacons = scanners[0]

    for a, b in combinations(base_beacons, 2):
        distances.add(tuple(a - b))

    print(distances)
    for scanner, beacons in scanners.items():
        if scanner == 0:
            continue
        s_distances = set()
        for a, b in combinations(beacons, 2):
            s_distances.add(tuple(a - b))
        # TODO: rotate all vectors
        # compare with distances set
        # if 12 are a match, we found the transformation of this scanner
        # to scanner 0
        # add all distances to the base distances
        # result is the "reverse combination" of the distances.
