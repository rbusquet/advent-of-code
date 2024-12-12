from functools import cache
from math import floor, log
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def digits(number: int) -> int:
    return floor(log(number, 10) + 1)


def blink_one(stone: int) -> list[int]:
    if stone == 0:
        return [1]
    d = digits(stone)

    if d % 2 == 0:
        half = d // 2
        return [stone // 10**half, stone % 10**half]
    else:
        return [stone * 2024]


@cache
def blink_one_v2(stone: int, count: int) -> int:
    if count == 0:
        return 1

    if stone == 0:
        return blink_one_v2(1, count - 1)

    d = digits(stone)

    if d % 2 == 0:
        half = d // 2
        return blink_one_v2(stone // 10**half, count - 1) + blink_one_v2(
            stone % 10**half, count - 1
        )
    else:
        return blink_one_v2(stone * 2024, count - 1)


def blink(stones: list[int]) -> list[int]:
    result = []

    for stone in stones:
        result.extend(blink_one(stone))
    return result


def part_1() -> int:
    stones = list(map(int, input.read_text().split()))

    for i in range(25):
        stones = blink(stones)

    return len(stones)


def part_2() -> int:
    stones = list(map(int, input.read_text().split()))

    result = 0
    for stone in stones:
        result += blink_one_v2(stone, 75)

    return len(stones)


print(part_1())
print(part_2())
