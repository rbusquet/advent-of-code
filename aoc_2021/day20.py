from collections import defaultdict
from collections.abc import Sequence
from pathlib import Path
from typing import Literal, cast

from progress.spinner import (  # type: ignore[import-not-found,import-untyped]
    LineSpinner,
)

Pixel = tuple[int, int]
Value = Literal[".", "#"]

POWER_MAP = {
    (-1, -1): 0,
    (-1, 0): 1,
    (-1, 1): 2,
    (0, -1): 3,
    (0, 0): 4,
    (0, 1): 5,
    (1, -1): 6,
    (1, 0): 7,
    (1, 1): 8,
}

"""
X X X X X
X 9 8 7 X  if I'm looking at how a pixel    1 2 3
X 6 5 4 X ------------------------------->  4 5 6
X 3 2 1 X      affects its neighboors       7 8 9
X X X X X
"""


def enhance(
    known_pixels: dict[Pixel, Value],
    background: Value,
    algorithm: Sequence[Value],
) -> tuple[dict[Pixel, Value], Value]:
    pixels_to_update = defaultdict[Pixel, int](int)

    for (x1, y1), value in known_pixels.items():
        for (x2, y2), power in POWER_MAP.items():
            x, y = x1 + x2, y1 + y2
            pixels_to_update[x, y] += (value == "#") * pow(2, power)

    result_image = dict[Pixel, Value]()
    for x1, y1 in pixels_to_update:
        # for all pixels to update, check if we know all their neighboors
        for (x2, y2), power in POWER_MAP.items():
            x, y = x1 + x2, y1 + y2
            if (x, y) not in known_pixels:
                revert_effect = 8 - power
                if background == "#":
                    pixels_to_update[x1, y1] += pow(2, revert_effect)
        result_image[x1, y1] = algorithm[pixels_to_update[x1, y1]]

    if background == ".":
        background = algorithm[0]
    else:
        background = algorithm[pow(2, 9) - 1]
    return result_image, background


def part_1() -> int:
    image = dict[Pixel, Value]()
    with open(Path(__file__).parent / "input.txt") as file:
        algorithm = cast(Sequence[Value], file.readline())
        file.readline()

        for i, line in enumerate(file):
            for j, char in enumerate(line.strip()):
                image[i, j] = cast(Value, char)

    image, background = enhance(image, ".", algorithm)
    image, background = enhance(image, background, algorithm)

    return len([value for value in image.values() if value == "#"])


def part_2() -> int:
    image = dict[Pixel, Value]()
    with open(Path(__file__).parent / "input.txt") as file:
        algorithm = cast(Sequence[Value], file.readline())
        file.readline()

        for i, line in enumerate(file):
            for j, char in enumerate(line.strip()):
                image[i, j] = cast(Value, char)

    background = cast(Value, ".")
    with LineSpinner() as spinner:
        for _ in range(50):
            # print(background)
            image, background = enhance(image, background, algorithm)
            spinner.next()

    assert background == "."
    return len([value for value in image.values() if value == "#"])


if __name__ == "__main__":
    print(part_1())
    print(part_2())
