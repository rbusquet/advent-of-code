from collections import defaultdict
from itertools import combinations
from operator import itemgetter
from pathlib import Path

input = Path(__file__).parent / "input.txt"


def part_1() -> int:
    containers = [int(line) for line in input.read_text().splitlines()]

    answer = 0
    for i in range(len(containers)):
        for fill in combinations(containers, i):
            answer += sum(fill) == 150
    return answer


def part_2() -> int:
    containers = [int(line) for line in input.read_text().splitlines()]

    sizes = defaultdict[int, int](int)
    for i in range(len(containers)):
        for fill in combinations(containers, i):
            if sum(fill) == 150:
                sizes[len(fill)] += 1
    return min(sizes.items(), key=itemgetter(0))[1]


print(part_1())
print(part_2())
