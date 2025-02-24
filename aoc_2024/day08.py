from collections import defaultdict
from collections.abc import Iterable
from itertools import combinations
from pathlib import Path

input = Path(__file__).parent / "input.txt"

Node = tuple[int, int]


def find_anti_nodes(w: int, h: int, a: Node, b: Node) -> Iterable[Node]:
    x1, y1 = a
    x2, y2 = b

    delta_x = x1 - x2
    delta_y = y1 - y2

    if 0 <= x1 + delta_x < w and 0 <= y1 + delta_y < h:
        yield x1 + delta_x, y1 + delta_y
    if 0 <= x2 - delta_x < w and 0 <= y2 - delta_y < h:
        yield x2 - delta_x, y2 - delta_y


def find_resonant_anti_nodes(w: int, h: int, a: Node, b: Node) -> Iterable[Node]:
    x1, y1 = a
    x2, y2 = b

    delta_x = x1 - x2
    delta_y = y1 - y2

    while 0 <= x1 < w and 0 <= y1 < h:
        yield x1, y1
        x1 += delta_x
        y1 += delta_y

    while 0 <= x2 < w and 0 <= y2 < h:
        yield x2, y2
        x2 -= delta_x
        y2 -= delta_y


def part_1() -> int:
    all_antennas = defaultdict[str, list[Node]](list)
    width = height = 0
    grid = [list(line) for line in input.read_text().splitlines()]
    for x, line in enumerate(grid):
        width = len(line)
        height += 1
        for y, antenna in enumerate(line):
            if antenna == ".":
                continue
            all_antennas[antenna].append((x, y))

    antinodes = set[Node]()
    for label, antennas in all_antennas.items():
        pairs = combinations(antennas, 2)
        for pair in pairs:
            # g = deepcopy(grid)
            anti_nodes = list(find_anti_nodes(width, height, *pair))
            # for node in anti_nodes:
            #     g[node[0]][node[1]] = "#"
            # print("\n".join("".join(line) for line in g))
            # print("------------------")
            antinodes.update(anti_nodes)
    return len(antinodes)


def part_2() -> int:
    all_antennas = defaultdict[str, list[Node]](list)
    width = height = 0
    grid = [list(line) for line in input.read_text().splitlines()]
    for x, line in enumerate(grid):
        width = len(line)
        height += 1
        for y, antenna in enumerate(line):
            if antenna == ".":
                continue
            all_antennas[antenna].append((x, y))

    antinodes = set[Node]()
    for label, antennas in all_antennas.items():
        pairs = combinations(antennas, 2)
        for pair in pairs:
            # g = deepcopy(grid)
            anti_nodes = list(find_resonant_anti_nodes(width, height, *pair))
            # for node in anti_nodes:
            #     g[node[0]][node[1]] = "#"
            # print("\n".join("".join(line) for line in g))
            # print("------------------")
            antinodes.update(anti_nodes)
    return len(antinodes)


print(part_1())
print(part_2())
