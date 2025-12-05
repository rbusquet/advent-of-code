from collections.abc import Iterator
from itertools import count, product
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def neighborhood(x: int, y: int) -> Iterator[tuple[int, int]]:
    for diff in product([-1, 0, 1], repeat=2):
        neighbor = (x + diff[0], y + diff[1])
        yield neighbor


def part_1() -> int:
    lines = [list(line) for line in input.read_text().splitlines()]
    valid_rolls = 0
    for x in range(len(lines)):
        for y in range(len(lines[x])):
            # count neighbors equal to "@"
            count_at = 0
            if lines[x][y] == ".":
                continue
            for n in neighborhood(x, y):
                if n == (x, y):
                    continue
                if 0 <= n[0] < len(lines) and 0 <= n[1] < len(lines[x]):
                    if lines[n[0]][n[1]] == "@" or lines[n[0]][n[1]] == "x":
                        count_at += 1
            if count_at < 4:
                valid_rolls += 1
                lines[x][y] = "x"
    # print("\n".join("".join(line) for line in lines))
    return valid_rolls


def part_2() -> int:
    lines = [list(line) for line in input.read_text().splitlines()]
    existing_ats = sum(line.count("@") for line in lines)
    for run in count():
        print("---------")
        print("\n".join("".join(line) for line in lines))
        valid_rolls = 0
        for x in range(len(lines)):
            for y in range(len(lines[x])):
                # count neighbors equal to "@"
                count_at = 0
                if lines[x][y] != "@":
                    continue
                for n in neighborhood(x, y):
                    if n == (x, y):
                        continue
                    if 0 <= n[0] < len(lines) and 0 <= n[1] < len(lines[x]):
                        if lines[n[0]][n[1]] == "@" or lines[n[0]][n[1]] == str(run):
                            count_at += 1
                if count_at < 4:
                    valid_rolls += 1
                    lines[x][y] = str(run)
        if valid_rolls == 0:
            # count remaining "@"
            for x in range(len(lines)):
                for y in range(len(lines[x])):
                    if lines[x][y] == "@":
                        valid_rolls += 1
            return existing_ats - valid_rolls
    return -1


print(part_1())
print(part_2())
