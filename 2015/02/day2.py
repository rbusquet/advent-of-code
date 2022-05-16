from pathlib import Path


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        total_area = 0
        for square in file:
            l, w, h = map(int, square.split("x"))

            area = 2 * l * w + 2 * w * h + 2 * h * l + min(l * w, w * h, h * l)
            total_area += area
        return total_area


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        total_ribbon = 0
        for square in file:
            l, w, h = map(int, square.split("x"))
            min_perimeter = min(2 * (l + w), 2 * (w + h), 2 * (h + l))
            bow = l * w * h
            total_ribbon += min_perimeter + bow
        return total_ribbon


if __name__ == "__main__":
    print(part_1())
    print(part_2())
