from collections import Counter, defaultdict
from pathlib import Path

DAYS = 80


def grow_slow(fishes: list[int], max_days: int) -> int:
    days = 0
    while days < max_days:
        new_fishes = []

        for i, fish in enumerate(fishes):
            if fish == 0:
                fishes[i] = 6
                new_fishes.append(8)
                continue
            fishes[i] -= 1
        fishes.extend(new_fishes)
        days += 1

    return len(fishes)


def grow_fast(initial: list[int], max_days: int) -> int:
    same_age = Counter(initial)
    fishes_by_age = same_age.most_common()
    days = 0

    while days < max_days:
        next_fishes = defaultdict[int, int](int, fishes_by_age)

        for age, total_fishes in fishes_by_age:
            week_ended = age == 0
            new_age = 6 if week_ended else (age - 1)
            next_fishes[new_age] += total_fishes
            next_fishes[age] -= total_fishes

            if week_ended:
                next_fishes[8] += total_fishes
        fishes_by_age = list(next_fishes.items())
        # print(fishes_by_age)

        days += 1
    return sum(f[1] for f in fishes_by_age)


def part_1() -> int:
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        fishes = list(map(int, file.readline().split(",")))
    return grow_slow(fishes, 80)


def part_2() -> int:
    with open(Path(__file__).parent / "input.txt") as file:  # noqa: F841
        fishes = list(map(int, file.readline().split(",")))
    return grow_fast(fishes, 256)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
