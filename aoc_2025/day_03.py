from functools import cache
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def max_joltage(bank: str) -> int:
    max_joltage = 0
    for left in range(len(bank) - 1):
        for right in range(left + 1, len(bank)):
            joltage = int(bank[left]) * 10 + int(bank[right])
            if joltage > max_joltage:
                max_joltage = joltage
    return max_joltage


def max_joltage_12(bank: str) -> int:
    @cache
    def dp(index: int, remaining: int) -> str:
        if remaining == 0:
            return ""
        if len(bank) - index == remaining:
            return bank[index:]

        # Take current digit or skip it
        take = bank[index] + dp(index + 1, remaining - 1)
        skip = dp(index + 1, remaining)
        return max(take, skip)

    return int(dp(0, 12))


def part_1() -> int:
    lines = input.read_text().splitlines()
    joltage = 0
    for line in lines:
        joltage += max_joltage(line)
    return joltage


def part_2() -> int:
    lines = input.read_text().splitlines()
    joltage = 0
    for line in lines:
        joltage += max_joltage_12(line)
    return joltage


print(part_1())
print(part_2())
