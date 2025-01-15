from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    digits = input.read_text()

    last = int(digits[-1]) if digits[-1] == digits[0] else 0
    return (
        sum(
            int(digits[i]) for i in range(len(digits) - 1) if digits[i] == digits[i + 1]
        )
        + last
    )


def part_2() -> int:
    digits = input.read_text()
    steps = len(digits) // 2

    total = 0
    for i, digit in enumerate(digits):
        j = i + steps
        if digit == digits[j % len(digits)]:
            total += int(digit)

    return total


print(part_1())
print(part_2())
