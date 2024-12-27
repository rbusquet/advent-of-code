from itertools import permutations
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    diffs = dict[tuple[str, str], int]()
    names = set()

    for line in input.read_text().splitlines():
        match line.split():
            case [left, _, "gain", happiness, *_, right]:
                diffs[left, right[:-1]] = int(happiness)
                names.add(left)
            case [left, _, "lose", happiness, *_, right]:
                diffs[left, right[:-1]] = -int(happiness)
                names.add(left)

    def calculate_happiness(arrangement: tuple[str, ...]) -> int:
        happiness = 0
        for i in range(len(arrangement)):
            left = arrangement[i]
            right = arrangement[(i + 1) % len(arrangement)]
            happiness += diffs[left, right]
            happiness += diffs[right, left]
        return happiness

    max_happiness = 0
    for arrangement in permutations(names):
        current_happiness = calculate_happiness(arrangement)
        if current_happiness > max_happiness:
            max_happiness = current_happiness

    return max_happiness


def part_2() -> int:
    diffs = dict[tuple[str, str], int]()
    names = set()

    for line in input.read_text().splitlines():
        match line.split():
            case [left, _, "gain", happiness, *_, right]:
                diffs[left, right[:-1]] = int(happiness)
                names.add(left)
            case [left, _, "lose", happiness, *_, right]:
                diffs[left, right[:-1]] = -int(happiness)
                names.add(left)

    names.add("MYSELF")

    def calculate_happiness(arrangement: tuple[str, ...]) -> int:
        happiness = 0
        for i in range(len(arrangement)):
            left = arrangement[i]
            right = arrangement[(i + 1) % len(arrangement)]
            if left == "MYSELF" or right == "MYSELF":
                continue
            happiness += diffs[left, right]
            happiness += diffs[right, left]
        return happiness

    max_happiness = 0
    for arrangement in permutations(names):
        current_happiness = calculate_happiness(arrangement)
        if current_happiness > max_happiness:
            max_happiness = current_happiness

    return max_happiness


print(part_1())
print(part_2())
