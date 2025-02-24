import argparse
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from typing import TextIO


@dataclass
class Arguments:
    file: TextIO = sys.stdin


def strip_lines(file: TextIO) -> Iterator[str]:
    for line in file:
        yield line.strip()


def area(*vertices: tuple[int, int]) -> int:
    """
    Calculate the area of a polygon given its vertices.
    """
    polygon = [*vertices, vertices[0]]
    area = sum(x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(polygon, polygon[1:]))
    perimeter = sum(
        abs(x1 - x2) + abs(y1 - y2) for (x1, y1), (x2, y2) in zip(polygon, polygon[1:])
    )
    return abs(area) // 2 + perimeter // 2 + 1


def part_1(file: TextIO) -> int:
    file.seek(0)

    vertices = list[tuple[int, int]]()
    x = y = 0
    vertices.append((x, y))
    for line in strip_lines(file):
        match line.split():
            case ["U", count, _]:
                vertices.append((x, y + int(count)))
                y += int(count)
            case ["D", count, _]:
                vertices.append((x, y - int(count)))
                y -= int(count)
            case ["L", count, _]:
                vertices.append((x - int(count), y))
                x -= int(count)
            case ["R", count, _]:
                vertices.append((x + int(count), y))
                x += int(count)
            case _:
                raise ValueError(f"Invalid line: {line}")

    return area(*vertices)


def part_2(file: TextIO) -> int:
    file.seek(0)

    vertices = list[tuple[int, int]]()
    x = y = 0
    vertices.append((x, y))
    for line in strip_lines(file):
        color = line.split()[-1].strip("()#")
        direction = int(color[-1])
        count = int(color[:-1], base=16)

        # 0 means R, 1 means D, 2 means L, and 3 means U.
        if direction == 3:
            vertices.append((x, y + int(count)))
            y += int(count)
        if direction == 1:
            vertices.append((x, y - int(count)))
            y -= int(count)
        if direction == 2:
            vertices.append((x - int(count), y))
            x -= int(count)
        if direction == 0:
            vertices.append((x + int(count), y))
            x += int(count)

    return area(*vertices)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=argparse.FileType("r"))
    args = Arguments()
    parser.parse_args(namespace=args)
    print(part_1(args.file))
    print(part_2(args.file))
