from pathlib import Path


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        total_area = 0
        for square in file:
            length, width, height = map(int, square.split("x"))

            area = (
                2 * length * width
                + 2 * width * height
                + 2 * height * length
                + min(length * width, width * height, height * length)
            )
            total_area += area
        return total_area


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        total_ribbon = 0
        for square in file:
            length, width, height = map(int, square.split("x"))
            min_perimeter = min(
                2 * (length + width), 2 * (width + height), 2 * (height + length)
            )
            bow = length * width * height
            total_ribbon += min_perimeter + bow
        return total_ribbon


if __name__ == "__main__":
    print(part_1())
    print(part_2())
