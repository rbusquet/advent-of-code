from pathlib import Path


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        floor = 0
        while step := file.read(1):
            floor += step == "(" or -1
        return floor


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        floor = 0
        position = 1
        while step := file.read(1):
            floor += step == "(" or -1
            if floor == -1:
                return position
            position += 1
        raise Exception("Something went wrong")


if __name__ == "__main__":
    print(part_1())
    print(part_2())
