from collections import Counter
from heapq import nlargest, nsmallest
from itertools import pairwise
from operator import itemgetter
from pathlib import Path

Rules = dict[tuple[str, str], str]


def process_file() -> tuple[Rules, str]:
    with open(Path(__file__).parent / "input.txt") as file:
        template = file.readline().strip()
        rules = Rules()
        for line in file:
            if not line.strip():
                continue
            pair, _, value = line.strip().split()
            rules[pair[0], pair[1]] = value
    return rules, template


def generate_polymer_slow(rules: Rules, template: str, steps: int = 10) -> int:
    """
    Solves part 1, hangs on part 2.
    """
    for _ in range(steps):
        next_template = list[str]()
        for left, right in pairwise(template):
            next_template.extend([left, rules[left, right]])
        next_template.append(template[-1])
        template = "".join(next_template)

    counter = Counter(template)
    most_common = nlargest(1, counter.items(), key=itemgetter(1))[0]
    least_common = nsmallest(1, counter.items(), key=itemgetter(1))[0]

    return most_common[1] - least_common[1]


def generate_polymer(rules: Rules, template: str, steps: int = 40) -> int:
    """
    Solves part 2.

    Consider a rule AB -> C. If a polymer has 10 pairs AB, 10 new AC and CB
    pairs are created, and the 10 AB pairs are "broken".
    The resulting 10 C elements are added to the polymer.
    """
    counts = Counter(template)
    pairs = Counter(pairwise(template))
    step = 0
    while step < steps:
        for (left, right), count in Counter(pairs).items():
            result = rules[left, right]
            # These pairs are created in one step
            pairs[left, result] += count
            pairs[result, right] += count
            # The original pair is broken in one step
            pairs[left, right] -= count

            # Add to current count of the new element
            counts[result] += count
        step += 1
    least_common, *_, most_common = sorted(counts.items(), key=itemgetter(1))
    return most_common[1] - least_common[1]


def part_1() -> int:
    rules, template = process_file()
    return generate_polymer_slow(rules, template, steps=10)


def part_2() -> int:
    rules, template = process_file()
    return generate_polymer(rules, template, steps=40)


if __name__ == "__main__":
    print(part_1())
    print(part_2())
