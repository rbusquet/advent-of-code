import re
from pathlib import Path

exp = re.compile(r"\\x([0-9a-f]{2})")


def memory_len(word: str) -> int:
    # print(word, end=" ")
    word = word.strip('"')
    word = word.replace(r"\\", "\\")
    word = word.replace(r"\"", '"')
    if m := exp.findall(word):
        for g in m:
            word = word.replace(rf"\x{g}", chr(int(g, 16)))
    # print("->", word)
    return len(word)


def encoded_len(word: str) -> int:
    # print(word, end=" ")
    word = word.replace("\\", r"\\").replace('"', r"\"")
    word = f'"{word}"'
    # print("->", word)
    return len(word)


def part_1() -> int:
    total = 0
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        for line in file:
            a, b = len(line.strip()), memory_len(line.strip())
            total += a
            total -= b
    return total


def part_2() -> int:
    total = 0
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        for line in file:
            a, b = len(line.strip()), encoded_len(line.strip())
            total -= a
            total += b
    return total


if __name__ == "__main__":
    print(part_1())
    print(part_2())
