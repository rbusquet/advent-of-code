from pathlib import Path

CORRECT_DISPLAY_MAP = dict(
    zip(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [
            0b1110111,
            0b0010010,
            0b1011101,
            0b1011011,
            0b0111010,
            0b1101011,
            0b1101111,
            0b1010010,
            0b1111111,
            0b1111011,
        ],
    )
)

EASY_DIGITS_LENGTHS = [2, 4, 3, 7]
EASY_DIGITS = [1, 4, 7, 8]
EASY_DECODER = dict(zip(EASY_DIGITS_LENGTHS, EASY_DIGITS))


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        count = 0
        for line in file:
            _, outputs = line.strip().split(" | ")
            for digit in outputs.split(" "):
                count += len(digit) in EASY_DIGITS_LENGTHS

    return count


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841

        for line in file:
            decoded: list[int] = []
            _, outputs = line.strip().split(" | ")
            for digit in outputs.split(" "):
                if len(digit) in EASY_DIGITS_LENGTHS:
                    decoded.append(EASY_DECODER[len(digit)])
                    continue

    return 0


if __name__ == "__main__":
    print(part_1())
    print(part_2())
