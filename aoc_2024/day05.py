from functools import cmp_to_key
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    rules = list[tuple[str, str]]()
    updates = list[list[str]]()
    with input.open() as file:
        for line in file:
            if not line.strip():
                break
            a, b = line.strip().split("|")
            rules.append((a, b))
        for line in file:
            updates.append(line.strip().split(","))

    def compare(a: str, b: str) -> int:
        if (a, b) in rules:
            return -1
        if (b, a) in rules:
            return 1
        return int(a) - int(b)

    middles = 0
    for update in updates:
        corrected = sorted(update, key=cmp_to_key(compare))
        if update == corrected:
            print(update)
            middles += int(update[len(update) // 2])
    return middles


def part_2() -> int:
    rules = list[tuple[str, str]]()
    updates = list[list[str]]()
    with input.open() as file:
        for line in file:
            if not line.strip():
                break
            a, b = line.strip().split("|")
            rules.append((a, b))
        for line in file:
            updates.append(line.strip().split(","))

    def compare(a: str, b: str) -> int:
        if (a, b) in rules:
            return -1
        if (b, a) in rules:
            return 1
        return int(a) - int(b)

    middles = 0
    for update in updates:
        corrected = sorted(update, key=cmp_to_key(compare))
        if update != corrected:
            print(update, "->", corrected)
            middles += int(corrected[len(corrected) // 2])
    return middles


print(part_1())
print(part_2())
