from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    """count how many times we land on 0"""
    start = 50
    at_zero = 0
    for line in input.read_text().splitlines():
        direction = line[0]
        count = int(line[1:])
        if direction == "L":
            start -= count
            start %= 100
        elif direction == "R":
            start += count
            start %= 100
        if start == 0:
            at_zero += 1

    return at_zero


def part_2() -> int:
    """count how many times we pass through 0"""
    start = 50
    passes_zero = 0
    for line in input.read_text().splitlines():
        direction = line[0]
        count = int(line[1:])
        if direction == "L":
            for _ in range(count):
                start -= 1
                start %= 100
                if start == 0:
                    passes_zero += 1
        elif direction == "R":
            for _ in range(count):
                start += 1
                start %= 100
                if start == 0:
                    passes_zero += 1

    return passes_zero


print(part_1())
print(part_2())
