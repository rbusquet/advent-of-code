import re
from pathlib import Path

input = Path(__file__).parent / "input.txt"

SPIN = re.compile(r"s(\d+)")
EXCHANGE = re.compile(r"x(\d+)/(\d+)")
PARTNER = re.compile(r"p(.)/(.)")


def part_1() -> str:
    programs = list("abcdefghijklmnop")

    for move in input.read_text().split(","):
        if match := SPIN.match(move):
            count = int(match.group(1))
            programs = programs[-count:] + programs[:-count]
        elif match := EXCHANGE.match(move):
            a, b = int(match.group(1)), int(match.group(2))
            programs[a], programs[b] = programs[b], programs[a]
        elif match := PARTNER.match(move):
            a, b = programs.index(match.group(1)), programs.index(match.group(2))
            programs[a], programs[b] = programs[b], programs[a]

    return "".join(programs)


def part_2() -> str:
    programs = list("abcdefghijklmnop")
    moves = input.read_text().split(",")

    visited = set[str]()

    loop = []
    for i in range(1_000_000_000):
        x = "".join(programs)
        if loop and x == loop[0]:
            break
        elif x in visited:
            loop.append(x)
        visited.add(x)
        for move in moves:
            if match := SPIN.match(move):
                count = int(match.group(1))
                programs = programs[-count:] + programs[:-count]
            elif match := EXCHANGE.match(move):
                a, b = int(match.group(1)), int(match.group(2))
                programs[a], programs[b] = programs[b], programs[a]
            elif match := PARTNER.match(move):
                a, b = programs.index(match.group(1)), programs.index(match.group(2))
                programs[a], programs[b] = programs[b], programs[a]

    return loop[1_000_000_000 % len(loop)]


print(part_1())
print(part_2())
