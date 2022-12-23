import argparse
import re
from typing import TextIO


def main(infile: TextIO) -> None:
    fully_contains_count = 0
    overlaps_count = 0

    for line in infile:
        if not line.strip():
            break
        a, b, c, d = [int(x) for x in re.split("[,-]", line.strip())]
        left, right = [(a, b), (c, d)]
        ordered = tuple(sorted([a, b, c, d]))

        fully_contains = ordered in [
            (left[0], right[0], right[1], left[1]),
            (right[0], left[0], left[1], right[1]),
        ]

        # without ordered step
        assert fully_contains == (
            (left[0] <= right[0] and left[1] >= right[1])
            or (right[0] <= left[0] and right[1] >= left[1])
        )

        no_overlaps = (
            ordered == (left[0], left[1], right[0], right[1]) and left[1] != right[0]
        ) or (ordered == (right[0], right[1], left[0], left[1]) and right[1] != left[0])

        # without ordered step
        assert no_overlaps != (left[0] <= right[1] and left[1] >= right[0]) or (
            right[0] <= left[1] and right[1] >= left[0]
        )

        fully_contains_count += fully_contains
        overlaps_count += not no_overlaps

    print("total fully contained:", fully_contains_count)
    print("total overlaps:", overlaps_count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))

    args = parser.parse_args()
    main(args.infile)
