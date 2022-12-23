import argparse
import string
from functools import reduce
from operator import and_
from typing import Iterable, TextIO

from more_itertools import chunked


def find_common(*iterables: str) -> str:
    common: set[str] = reduce(and_, [set(it.strip()) for it in iterables])
    common.discard("\n")
    return common.pop()


def find_misplaced_item(rucksack: str) -> str:
    """
    finds the missing item and returns it
    """
    count = len(rucksack)
    compartment1, compartment2 = rucksack[: count // 2], rucksack[count // 2 :]
    return find_common(compartment1, compartment2)


def find_misplaced_priorities(rucksacks: Iterable[str]) -> int:
    priorities = 0

    for rucksack in rucksacks:
        misplaced = find_misplaced_item(rucksack)
        priorities += ord(misplaced) - ord("a")
    return priorities


def main(file: TextIO) -> None:
    misplaced_priority = 0
    badges_priority = 0
    letters = string.ascii_letters
    ended = False
    for group in chunked(file, 3):
        for line in group:
            if not line.strip():
                ended = True
                break
            misplaced = find_misplaced_item(line)
            misplaced_priority += letters.index(misplaced) + 1
        if ended:
            break

        badge = find_common(*group)
        badges_priority += letters.index(badge) + 1

    print("misplaced priority:", misplaced_priority)
    print("badges priority:", badges_priority)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=argparse.FileType("r"))

    args = parser.parse_args()
    main(args.infile)
