import csv
from itertools import combinations
from pathlib import Path

from more_itertools import minmax

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    spreadsheet = csv.reader(input.read_text().splitlines(), delimiter="\t")
    checksum = 0
    for line in spreadsheet:
        smallest, largest = minmax(map(int, line))
        checksum += largest - smallest
    return checksum


def part_2() -> int:
    spreadsheet = csv.reader(input.read_text().splitlines(), delimiter="\t")
    checksum = 0
    for line in spreadsheet:
        for a, b in combinations(map(int, line), 2):
            smallest, largest = minmax(a, b)
            if largest % smallest == 0:
                checksum += largest // smallest

    return checksum


print(part_1())
print(part_2())
