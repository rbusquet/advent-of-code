import operator
from collections import deque
from functools import cache
from pathlib import Path
from typing import cast

input = Path(__file__).parent / "input.txt"


def mix(secret: int, b: int) -> int:
    return secret ^ b


def prune(secret: int) -> int:
    return secret % 16777216


def step(secret: int, shift: int) -> int:
    op = operator.lshift if shift > 0 else operator.rshift
    return prune(mix(secret, op(secret, abs(shift))))


@cache
def evolve(secret: int) -> int:
    a = step(secret, 6)
    b = step(a, -5)
    return step(b, 11)


def part_1() -> int:
    total = 0
    for line in input.read_text().splitlines():
        secret = int(line)
        for _ in range(2000):
            secret = evolve(secret)
        total += secret
    return total


Sequence = tuple[int, int, int, int]


def part_2() -> int:
    known_sequences = set[Sequence]()
    all_bananas_per_sequences = list[dict[Sequence, int]]()
    for line in input.read_text().splitlines():
        secret = int(line)
        last_price = secret % 10
        last_four = deque[int](maxlen=4)
        bananas_per_sequence = dict[Sequence, int]()
        for _ in range(2000):
            secret = evolve(secret)
            current_price = secret % 10
            diff = current_price - last_price
            last_price = current_price

            last_four.append(diff)
            if len(last_four) == 4:
                sequence = cast(Sequence, tuple(last_four))
                known_sequences.add(sequence)
                if sequence not in bananas_per_sequence:
                    bananas_per_sequence[sequence] = current_price
        all_bananas_per_sequences.append(bananas_per_sequence)

    best = 0
    best_sequence = None
    for sequence in known_sequences:
        wins = sum(monkey.get(sequence, 0) for monkey in all_bananas_per_sequences)
        best = max(best, wins)
        if best == wins:
            best_sequence = sequence
            print(best_sequence)
    print(best_sequence)
    return best


print(part_1())
print(part_2())
