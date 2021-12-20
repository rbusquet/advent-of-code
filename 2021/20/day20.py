from pathlib import Path
from typing import Literal, Sequence, cast
from collections import defaultdict
from progress.spinner import LineSpinner
from PIL import Image, ImageDraw


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
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
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
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        algorithm = cast(Sequence[Value], file.readline())
        file.readline()

        for i, line in enumerate(file):
            for j, char in enumerate(line.strip()):
                image[i, j] = cast(Value, char)

    background = cast(Value, ".")
    gif = list[Image.Image]()
    with LineSpinner() as spinner:
        for i in range(50):
            # print(background)
            image, background = enhance(image, background, algorithm)
            image = trim(image)
            gif.append(save_image(image, i))
            spinner.next()
    gif[0].save(
        Path(__file__).parent / "temp_result.webp",
        save_all=True,
        optimize=False,
        append_images=gif[1:],
        loop=0,
        duration=200,
    )

    assert background == "."

    return len([value for value in image.values() if value == "#"])


def trim(image: dict[Pixel, Value]) -> dict[Pixel, Value]:
    min_x = min(p[0] for p in image if image[p] == "#")
    min_y = min(p[1] for p in image if image[p] == "#")
    max_x = max(p[0] for p in image if image[p] == "#")
    max_y = max(p[1] for p in image if image[p] == "#")

    result = dict[Pixel, Value]()

    for xx in range(min_x, max_x + 1):
        for yy in range(min_y, max_y + 1):
            result[xx, yy] = image[xx, yy]
    return result


def save_image(image: dict[Pixel, Value], count: int) -> Image.Image:
    min_x = min(p[0] for p in image)
    min_y = min(p[1] for p in image)
    max_x = max(p[0] for p in image)
    max_y = max(p[1] for p in image)
    hh, ww = max_x - min_x, max_y - min_y
    im = Image.new("RGB", (hh, ww))
    draw = ImageDraw.Draw(im)

    colors = {".": "black", "#": "white"}
    for (x, y), value in image.items():
        draw.point((x - min_x, y - min_y), fill=colors[value])
    im = im.resize((500, 500), resample=Image.NEAREST)
    return im


if __name__ == "__main__":
    print(part_1())
    print(part_2())
