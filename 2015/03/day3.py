from itertools import cycle
from pathlib import Path


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        x, y = 0, 0
        visited = set[tuple[int, int]]()
        visited.add((x, y))
        while direction := file.read(1):
            match direction:
                case "^":
                    x += 1
                case "v":
                    x -= 1
                case ">":
                    y += 1
                case "<":
                    y -= 1

            visited.add((x, y))
        return len(visited)


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        positions = [0, 0, 0, 0]
        visited = set[tuple[int, int]]()
        visited.add((0, 0))
        flipper = cycle([0, 2])
        while direction := file.read(1):
            pointer = next(flipper)
            match direction:
                case "^":
                    positions[pointer] += 1
                case "v":
                    positions[pointer] -= 1
                case ">":
                    positions[pointer + 1] += 1
                case "<":
                    positions[pointer + 1] -= 1

            visited.add((positions[pointer], positions[pointer + 1]))
        return len(visited)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
