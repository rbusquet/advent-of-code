from pathlib import Path
from typing import Counter, TextIO


def parse(file: TextIO):
    for line in file:
        yield tuple(line.strip())


def list_of_bits_to_int(x: list[str]) -> int:
    word = "".join(x)
    return int(word, 2)


# LENGTH = 5
# INPUT = "test_input.txt"

LENGTH = 12
INPUT = "input.txt"


def part_1():

    with open(Path(__file__).parent / INPUT) as file:  # noqa: F841
        counters = [Counter[str]() for _ in range(LENGTH)]
        for value in parse(file):
            for i, bit in enumerate(value):
                counters[i][bit] += 1

        gamma = [counter.most_common()[0][0] for counter in counters]
        epsilon = [counter.most_common(2)[1][0] for counter in counters]
        return list_of_bits_to_int(gamma) * list_of_bits_to_int(epsilon)


def count(report: list[tuple[str, ...]], position: int) -> Counter[str]:
    return Counter([value[position] for value in report])


def part_2():
    with open(Path(__file__).parent / INPUT) as file:  # noqa: F841
        report = list(parse(file))

    oxygen_report = co2_report = report
    for position in range(LENGTH):
        counter = count(oxygen_report, position)
        most_common, total = counter.most_common()[0]
        if len(oxygen_report) % 2 == 0 and total == len(oxygen_report) / 2:
            most_common = "1"

        if len(oxygen_report) != 1:
            oxygen_report = [
                value for value in oxygen_report if value[position] == most_common
            ]
    for position in range(LENGTH):
        counter = count(co2_report, position)
        most_common, total = counter.most_common()[0]
        if len(co2_report) % 2 == 0 and total == len(co2_report) / 2:
            most_common = "1"

        if len(co2_report) != 1:
            co2_report = [
                value for value in co2_report if value[position] != most_common
            ]
    return list_of_bits_to_int(oxygen_report[0]) * list_of_bits_to_int(co2_report[0])


if __name__ == "__main__":
    print(part_1())
    print(part_2())
