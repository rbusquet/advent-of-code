import re
from pathlib import Path


def part_1() -> int:
    regex = re.compile(r"(\d)")
    with open(Path(__file__).parent / "input.txt") as file:
        total = 0
        for line in file:
            print(line)
            integers = regex.findall(line)
            value = 10 * int(integers[0]) + int(integers[-1])
            print(integers, value)
            total += value
    return total


def part_2() -> int:
    spelled_out_digits = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    regex = re.compile(rf"^({'|'.join(spelled_out_digits)}|\d)")
    with open(Path(__file__).parent / "input.txt") as file:
        total = 0
        for line in file:
            line = line.strip()
            first = last = 0
            for i in range(len(line)):
                if match := regex.match(line[i:]):
                    found_str = match.group()
                    if found_str in spelled_out_digits:
                        found = spelled_out_digits.index(found_str)
                    else:
                        found = int(found_str)
                    if first == 0:
                        first = found
                    last = found
            value = 10 * first + last
            total += value
    return total


if __name__ == "__main__":
    # print(part_1())
    print(part_2())
