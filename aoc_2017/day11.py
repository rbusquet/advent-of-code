from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    steps = input.read_text().strip().split(",")
    x, y = 0, 0
    for step in steps:
        if step == "n":
            y += 1
        elif step == "ne":
            x += 1
        elif step == "se":
            x += 1
            y -= 1
        elif step == "s":
            y -= 1
        elif step == "sw":
            x -= 1
        elif step == "nw":
            x -= 1
            y += 1
    return max(abs(x), abs(y))


def part_2() -> int:
    steps = input.read_text().strip().split(",")
    x, y = 0, 0
    max_distance = 0
    for step in steps:
        if step == "n":
            y += 1
        elif step == "ne":
            x += 1
        elif step == "se":
            x += 1
            y -= 1
        elif step == "s":
            y -= 1
        elif step == "sw":
            x -= 1
        elif step == "nw":
            x -= 1
            y += 1
        max_distance = max(max_distance, max(abs(x), abs(y)))
    return max_distance


print(part_1())
print(part_2())
