from pathlib import Path

CORRECT_DISPLAY_MAP = dict(
    zip(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        [
            set("abcefg"),
            set("cf"),
            set("acfef"),
            set("acdfg"),
            set("bcdf"),
            set("abdfg"),
            set("abdefg"),
            set("acf"),
            set("abcdefg"),
            set("abcdfg"),
        ],
    )
)

DISPLAY_TO_NUMBER = {frozenset(v): k for k, v in CORRECT_DISPLAY_MAP.items()}

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


HARD_DECODER = {5: [2, 3, 5], 6: [0, 6, 9]}


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        final = 0
        for line in file:
            patterns, outputs = line.strip().split(" | ")
            sized_patterns = {len(s): set(s) for s in patterns.split()}
            n = ""
            for o in outputs.strip().split():
                output = set(o)
                checksum = (
                    len(output),
                    len(output & sized_patterns[4]),
                    len(output & sized_patterns[2]),
                )
                # fmt: off
                match checksum:  # noqa: E501
                    case 2, _, _: n += '1'
                    case 3, _, _: n += '7'
                    case 4, _, _: n += '4'
                    case 7, _, _: n += '8'
                    case 5, 2, _: n += '2'
                    case 5, 3, 1: n += '5'
                    case 5, 3, 2: n += '3'
                    case 6, 4, _: n += '9'
                    case 6, 3, 1: n += '6'
                    case 6, 3, 2: n += "0"
                # fmt: on
            final += int(n)

    return final


if __name__ == "__main__":
    print(part_1())
    print(part_2())
