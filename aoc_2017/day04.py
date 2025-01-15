from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    valid = 0
    for line in input.read_text().splitlines():
        phrase = line.split()
        unique = set(phrase)
        valid += len(unique) == len(phrase)
    return valid


def part_2() -> int:
    valid = 0
    for line in input.read_text().splitlines():
        phrase = line.split()
        unique = set(frozenset(word) for word in phrase)
        valid += len(unique) == len(phrase)
    return valid


print(part_1())
print(part_2())
