import re
from pathlib import Path

input = Path(__file__).parent / "input.txt"


regexp = re.compile(r"Sue (\d+): ((\w+): (\d+)(,){0,1})+")


def part_1() -> int:
    i = 1
    result = dict(
        children=3,
        cats=7,
        samoyeds=2,
        pomeranians=3,
        akitas=0,
        vizslas=0,
        goldfish=5,
        trees=3,
        cars=2,
        perfumes=1,
    )

    for line in input.read_text().splitlines():
        data = line.split(": ", 1)[1]
        sue = {}
        for property in data.split(", "):
            name, value = property.split(": ")
            sue[name] = int(value)

        if all(value == result[name] for name, value in sue.items()):
            return i
        i += 1

    return 0


def part_2() -> int:
    i = 1
    result = dict(
        children=3,
        cats=7,
        samoyeds=2,
        pomeranians=3,
        akitas=0,
        vizslas=0,
        goldfish=5,
        trees=3,
        cars=2,
        perfumes=1,
    )

    def evaluate(value, name):
        if name in ["cats", "trees"]:
            return value > result[name]
        if name in ["pomeranians", "goldfish"]:
            return value < result[name]
        return value == result[name]

    for line in input.read_text().splitlines():
        data = line.split(": ", 1)[1]
        sue = {}
        for property in data.split(", "):
            name, value = property.split(": ")
            sue[name] = int(value)

        if all(evaluate(value, name) for name, value in sue.items()):
            return i
        i += 1

    return 0


print(part_1())
print(part_2())
