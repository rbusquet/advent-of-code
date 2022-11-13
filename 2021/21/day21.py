from collections import Counter
from functools import cache
from itertools import cycle, product
from pathlib import Path
from typing import Iterator, cast

from more_itertools import chunked


def deterministic_die() -> Iterator[int]:
    yield from cycle(range(1, 101))


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        player_1 = int(file.readline().split()[-1])
        player_2 = int(file.readline().split()[-1])

    score_1 = score_2 = 0
    dice = chunked(deterministic_die(), 3)
    dice_rolls = 0
    while score_1 < 1000 and score_2 < 1000:
        player_1 = (player_1 + sum(next(dice)) - 1) % 10 + 1
        player_2 = (player_2 + sum(next(dice)) - 1) % 10 + 1

        dice_rolls += 3
        score_1 += player_1
        if score_1 >= 1000:
            break
        score_2 += player_2
        dice_rolls += 3
        if score_2 >= 1000:
            break

    loser = min([score_1, score_2])
    return loser * dice_rolls


ALL_ROLLS = Counter(cast(list[int], map(sum, product([1, 2, 3], repeat=3))))


@cache
def dirac_dice(
    player_1: int,
    score_1: int,
    player_2: int,
    score_2: int,
) -> tuple[int, int]:
    wins_1 = wins_2 = 0
    p0 = player_1
    s0 = score_1
    for roll, wins in ALL_ROLLS.items():
        player_1 = (p0 + roll - 1) % 10 + 1
        score_1 = s0 + player_1
        if score_1 >= 21:
            wins_1 += wins
        else:
            next_win_2, next_win_1 = dirac_dice(player_2, score_2, player_1, score_1)
            wins_1 += next_win_1 * wins
            wins_2 += next_win_2 * wins
    return wins_1, wins_2


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:
        player_1 = int(file.readline().split()[-1])
        player_2 = int(file.readline().split()[-1])

    return max(dirac_dice(player_1, 0, player_2, 0))


if __name__ == "__main__":
    print(part_1())
    print(part_2())
