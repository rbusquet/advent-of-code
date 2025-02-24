from collections.abc import Iterator
from pathlib import Path

import progressbar

input = Path(__file__).parent / "input.txt"

lines = input.read_text().splitlines()
INITIAL_A = int(lines[0].split()[-1])
INITIAL_B = int(lines[1].split()[-1])

FACTOR_A = 16807
FACTOR_B = 48271
DENOMINATOR = 2147483647


def generate(
    initial: int, factor: int, denominator: int = DENOMINATOR, criteria: int = 1
) -> Iterator[int]:
    while True:
        initial = (initial * factor) % denominator
        if initial % criteria == 0:
            yield initial


def part_1() -> int:
    gen_a = generate(INITIAL_A, FACTOR_A)
    gen_b = generate(INITIAL_B, FACTOR_B)
    mask = 0xFFFF

    count = 0
    for _ in progressbar.progressbar(range(40_000_000)):
        a = next(gen_a) & mask
        b = next(gen_b) & mask
        count += a == b
    return count


def part_2() -> int:
    gen_a = generate(INITIAL_A, FACTOR_A, criteria=4)
    gen_b = generate(INITIAL_B, FACTOR_B, criteria=8)
    mask = 0xFFFF

    count = 0
    for _ in progressbar.progressbar(range(5_000_000)):
        a = next(gen_a) & mask
        b = next(gen_b) & mask
        count += a == b
    return count


print(part_1())
print(part_2())
